#!/usr/bin/python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import networkx as nx
from mplt import Gtk4MpltNx
from settings import SettingsWidget
from gen_graph import make_graph
from ga import GA
from aco import ACO
from 'hybride GAACO' import HybridGAACO


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
        G = make_graph(data["nodes"][0],data["edge_probability"][0],data["min_traffic"][0],data["max_traffic"][0],data["seed"][0] if not data["seed"][0]=="None" else None)
        print(data["type"][0])
        route=[]
        distance=0
        if data["type"][0]=="GA":
            ga=GA(G)
            route=ga.create_solution(50)[0]
            distance=ga.route_distance(route)
        elif data["type"][0]=="ACO":
            aco = ACO(G, n_ants=25, alpha=1, beta=2, evaporation=0.5)
            route, distance = aco.run_aco(iterations=500)
        elif data["type"][0]=="HYB":
            HybridGAACO_TEST= HybridGAACO(G)
            route,distance=HybridGAACO_TEST.run(ga_generations=20, aco_iterations=10, cycles=5)
        route_edges=[(route[i],route[i+1]) for i in range(len(route)-1)]
        mpltnx = Gtk4MpltNx(G,True,False,route_edges,f'Solution (Distance: {distance:.2f})')
        self.set_child(mpltnx)


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.artemis.ea")

    def do_activate(self):
        win = MyWindow(self)
        win.present()

app = MyApp()
app.run()
