import random
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

from agarnet.client import Client
from agarnet.utils import special_names, get_party_address, find_server
from .draw_hud import *
from .draw_cells import *
from .draw_background import *
from .drawutils import *
from .skins import CellSkins
from .subscriber import MultiSubscriber, Subscriber
from .window import WorldViewer


class NativeControl(Subscriber):
    def __init__(self, client):
        self.client = client
        self.movement_delta = Vec()

    def send_mouse(self):
        target = self.client.player.center + self.movement_delta
        self.client.send_target(*target)

    def on_world_update_post(self):
        # keep cells moving even when mouse stands still
        self.send_mouse()

    def on_mouse_moved(self, pos, pos_world):
        self.movement_delta = pos_world - self.client.player.center
        self.send_mouse()

    def on_mouse_pressed(self, button):
        if button == 2: # Middle click
            self.send_mouse()
            self.client.send_shoot()
        elif button == 3: # Right click
            self.send_mouse()
            self.client.send_split()

    def on_key_pressed(self, val, char):
        if char == 's':
            self.client.send_spectate()
        elif char == 'q':
            self.client.send_spectate_toggle()
        elif char == 'r' or val == Gdk.KEY_Return:
            self.client.send_respawn()
        elif char == 'w':
            self.send_mouse()
            self.client.send_shoot()
        elif val == Gdk.KEY_space:
            self.send_mouse()
            self.client.send_split()
        elif char == 'k':
            self.client.send_explode()


def format_log(lines, width, indent='  '):
    width = int(width)
    for l in lines:
        ind = ''
        while len(l) > len(ind):
            yield l[:width]
            ind = indent
            l = ind + l[width:]


class Logger(Subscriber):
    def __init__(self, client):
        self.client = client
        self.log_msgs = []
        self.leader_best = 11 # outside leaderboard, to show first msg on >=10

    def on_log_msg(self, msg, update=0, tag='[LOG]'):
        """
        Updates last `update` msgs with new data.
        Compares first 5 chars or up to first space.
        Set update=0 for no updating.
        """
        first_space = msg.index(' ') if ' ' in msg else 5
        for i, log_msg in enumerate(reversed(
                self.log_msgs[-update:] if update else [])):
            if msg[:first_space] == log_msg[:first_space]:
                self.log_msgs[-i - 1] = msg
                break
        else:
            self.log_msgs.append(msg)
            try:
                print(tag, msg)
            except UnicodeEncodeError:
                pass

    def on_update_msg(self, msg, update=9):
        self.on_log_msg(msg=msg, update=update)

    def on_connect_error(self, msg):
        self.on_log_msg(msg, tag='[ERROR]')

    on_message_error = on_connect_error

    def on_sock_open(self):
        self.on_update_msg('Connected to %s' % self.client.address)
        self.on_update_msg('Token: %s' % self.client.server_token)

    def on_world_rect(self, **kwargs):
        self.on_update_msg('World is from %(left)i:%(top)i to %(right)i:%(bottom)i' % kwargs)

    def on_server_version(self, number, text):
        self.on_log_msg('Server version %s from %s' % (number, text))

    def on_cell_eaten(self, eater_id, eaten_id):
        player = self.client.player
        if eaten_id in player.own_ids:
            name = 'Someone'
            if eater_id in player.world.cells:
                name = '"%s"' % player.world.cells[eater_id].name
            what = 'killed' if len(player.own_ids) <= 1 else 'ate'
            msg = '%s %s me!' % (name, what)
            self.on_update_msg(msg)

    def on_world_update_post(self):
        player = self.client.player
        x, y = player.center
        self.on_update_msg('Mass: %i Pos: (%.2f %.2f)' % (player.total_mass, x, y))

    def on_own_id(self, cid):
        if len(self.client.player.own_ids) == 1:
            self.on_log_msg('Respawned as %s' % self.client.player.nick)
        else:
            self.on_update_msg('Split into %i cells' % len(self.client.player.own_ids))

    def on_leaderboard_names(self, leaderboard):
        if not self.client.player.own_ids:
            return
        our_cid = min(c.cid for c in self.client.player.own_cells)
        for rank, (cid, name) in enumerate(leaderboard):
            if cid == our_cid:
                rank += 1  # start at rank 1
                self.leader_best = min(rank, self.leader_best)
                msg = 'Leaderboard: %i. (best: %i.)' % (rank, self.leader_best)
                self.on_update_msg(msg)

    def on_draw_hud(self, c, w):
        # scrolling log
        log_line_h = 12
        log_char_w = 6  # seems to work with my font

        log = list(format_log(self.log_msgs, w.INFO_SIZE / log_char_w))
        num_log_lines = min(len(log), int(w.INFO_SIZE / log_line_h))

        y_start = w.win_size.y - num_log_lines*log_line_h + 9

        c.fill_rect((0, w.win_size.y - num_log_lines*log_line_h),
                    size=(w.INFO_SIZE, num_log_lines*log_line_h),
                    color=to_rgba(BLACK, .3))

        for i, text in enumerate(log[-num_log_lines:]):
            c.draw_text((0, y_start + i*log_line_h), text,
                        align='left', size=10, face='monospace')


def gtk_watch_client(client):
    # watch client's websocket in GTK main loop
    # `or True` is for always returning True to keep watching
    GLib.io_add_watch(client.ws, GLib.IO_IN, lambda ws, _: client.on_message() or True)
    GLib.io_add_watch(client.ws, GLib.IO_ERR, lambda ws, _: client.subscriber.on_sock_error() or True)
    GLib.io_add_watch(client.ws, GLib.IO_HUP, lambda ws, _: client.disconnect() or True)


def gtk_main_loop():
    # Gtk.main() swallows exceptions, get them back
    sys.excepthook = lambda *args: sys.__excepthook__(*args) or sys.exit()

    Gtk.main()


class KeyToggler(MultiSubscriber):
    def __init__(self, key, *subs, disabled=False):
        super(KeyToggler, self).__init__(*subs)
        self.toggle_key = key
        self.enabled = not disabled

    def __getattr__(self, func_name):
        if self.enabled and func_name[:3] == 'on_':
            return MultiSubscriber.__getattr__(self, func_name)
        return lambda *_, **__: None

    def on_key_pressed(self, val, char):
        if val == self.toggle_key:
            self.enabled = not self.enabled
        self.__getattr__('on_key_pressed')(val, char)


class GtkControl(Subscriber):
    def __init__(self, address, token=None, nick=None):
        if nick is None: nick = random.choice(special_names)

        # connect the subscribers
        # order is important, first subscriber gets called first

        self.multi_sub = MultiSubscriber(self)

        def key(keycode, *subs, disabled=False):
            # subscribe all these subscribers, toggle them when key is pressed
            if isinstance(keycode, str): keycode = ord(keycode)
            self.multi_sub.sub(KeyToggler(keycode, *subs, disabled=disabled))

        self.client = client = Client(self.multi_sub)

        self.multi_sub.sub(NativeControl(client))

        # background
        key(Gdk.KEY_F2, SolidBackground())
        key(Gdk.KEY_F2, SolidBackground(WHITE), disabled=True)
        # key('b', WorldBorderDrawer())
        # key('g', GridDrawer())

        self.multi_sub.sub(CellsDrawer())

        # cell overlay
        key('k', CellSkins())
        key('n', CellNames())
        key('i',
            CellHostility(),
            CellMasses(),
            RemergeTimes(client),
            ForceFields(),
        )
        key('m', MovementLines())

        # HUD
        key(Gdk.KEY_F1,
            # Minimap(),
            Leaderboard(),
            # ExperienceMeter(),
            Logger(client),
            MassGraph(client),
        )
        key(Gdk.KEY_F3, FpsMeter(50), disabled=True)

        client.player.nick = nick

        try:
            client.connect(address, token)
        except ConnectionResetError:
            # sometimes connection gets closed on first attempt
            print('Connection got closed on first attempt, retrying')
            client.connect(address, token)

        gtk_watch_client(client)

        self.world_viewer = wv = WorldViewer(client.world)
        wv.draw_subscriber = wv.input_subscriber = self.multi_sub
        wv.focus_player(client.player)

    def on_world_update_post(self):
        self.world_viewer.drawing_area.queue_draw()

    def on_key_pressed(self, val, char):
        if val == Gdk.KEY_Escape:
            self.client.disconnect()
            Gtk.main_quit()
        elif char == 'c':  # reconnect to any server
            self.client.disconnect()
            address, token = find_server()
            self.client.connect(address, token)
            self.world_viewer.focus_player(self.client.player)


def main():
    print("Copyright (C) 2015  Gjum  <code.gjum@gmail.com>\n"
          "This program comes with ABSOLUTELY NO WARRANTY.\n"
          "This is free software, and you are welcome to redistribute it\n"
          "under certain conditions; see LICENSE.txt for details.\n"
          "Project homepage: https://github.com/Gjum/gagar\n"
          "Version: 0.1.4\n")

    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        print("Usage: %s [nick]" % sys.argv[0])
        print("       %s party <token> [nick]" % sys.argv[0])
        print("       %s <IP:port> <token> [nick]" % sys.argv[0])
        return

    address, token, nick, *_ = sys.argv[1:] + ([None] * 3)

    if token is None:
        nick = address
        address = None

    if address and address[0] in 'Pp':
        address = get_party_address(token)

    if not address:
        address, token = find_server()

    #address, token = find_server(mode='experimental')

    #token = 'Q4DNB'
    address2, token = find_server(mode='party', region='TK-Turkey')
    address = get_party_address(token)
    assert address2 == address, '%s %s' % (address, address2)
    print('addr', address, 'token', token)

    GtkControl(address, token, nick)
    gtk_main_loop()
