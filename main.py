#!/usr/bin/python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import networkx as nx
from mplt import Gtk4MpltNx
from settings import SettingsWidget

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Hello GTK")
        self.set_default_size(300, 100)
        self.set_icon_name("org.artemis.ea")

        button = SettingsWidget()
        button.connect("run", self.on_button_clicked)
        self.set_child(button)

    def on_button_clicked(self, button, data:dict):
        print("Button clicked!")
        self.set_default_size(900,600)
        G = nx.DiGraph()
        G.add_nodes_from(eval(data['nodes'][0]))
        G.add_edges_from(eval(data['edges'][0]))
        route=eval(data['route'][0])
        mpltnx = Gtk4MpltNx(G,False,False,route)
        self.set_child(mpltnx)


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.artemis.ea")

    def do_activate(self):
        win = MyWindow(self)
        win.present()

app = MyApp()
app.run()
