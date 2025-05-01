import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.backends.backend_gtk4 import NavigationToolbar2GTK4 as NavigationToolbar
from matplotlib.figure import Figure

class Gtk4MpltNx(Gtk.ScrolledWindow):
    __gtype_name__ = 'Gtk4MpltNx'
    def __init__(self, graph: nx.DiGraph, pos_available:bool=True, weight_available:bool=True, route:list=None):
        # # Create the main application window
        # win = Gtk.ApplicationWindow(application=app)
        # win.set_default_size(600, 400)
        # win.set_title("NetworkX DiGraph in GTK4")
        # Create a scrolled window and add the Matplotlib canvas
        super().__init__(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)

        # Create a Matplotlib figure and axes
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot()

        # Create a directed graph
        # G = nx.DiGraph()
        # G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D')])
        G=graph

        # Compute positions for the nodes
        pos = nx.get_node_attributes(G,"pos") if pos_available else nx.spring_layout(G)

        # Draw the graph
        nx.draw_networkx(G, pos=pos, ax=ax, arrows=True, with_labels=True, width=4)
        if weight_available:
            nx.draw_networkx_edge_labels(G, pos=pos, ax=ax, edge_labels={k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, 'weight').items()})
        if route != None:
            nx.draw_networkx_edges(G, pos=pos, ax=ax, arrows=True, edgelist=route, edge_color="red", style="dashed", width=2)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(vbox)

        canvas = FigureCanvas(fig)  # A Gtk.DrawingArea
        #canvas.set_size_request(800, 600)
        canvas.set_hexpand(True)
        canvas.set_vexpand(True)
        vbox.append(canvas)

        # Create toolbar
        toolbar = NavigationToolbar(canvas)
        vbox.append(toolbar)

#     win.show()
#
# app = Gtk.Application(application_id='org.example.NetworkXGTK4')
# app.connect('activate', on_activate)
# app.run(None)
