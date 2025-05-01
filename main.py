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
        G = nx.DiGraph()
        G.add_edges_from(eval(data['edges'][0]))
        mpltnx = Gtk4MpltNx(G,False,False,[('A', 'B'), ('B', 'C'), ('C', 'A')])
        self.set_child(mpltnx)


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.artemis.ea")

    def do_activate(self):
        win = MyWindow(self)
        win.present()

app = MyApp()
app.run()
