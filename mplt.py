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
    def __init__(self, graph: nx.DiGraph, pos_available:bool=True, write_weights:bool=True, route:list=None, title:str=""):
        # # Create the main application window
        # win = Gtk.ApplicationWindow(application=app)
        # win.set_default_size(600, 400)
        # win.set_title("NetworkX DiGraph in GTK4")
        # Create a scrolled window and add the Matplotlib canvas
        super().__init__(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        self.set_min_content_height(600)

        # Create a Matplotlib figure and axes
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot()
        self.ax.title.set_text(title)
        self.route_lines=[]
        # Create a directed graph
        # G = nx.DiGraph()
        # G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D')])
        self.G=graph

        # Compute positions for the nodes
        self.pos = nx.get_node_attributes(self.G,"pos") if pos_available else nx.spring_layout(G)

        # Draw the graph
        nx.draw_networkx(self.G, pos=self.pos, ax=self.ax, arrows=True, with_labels=True, width=4)
        if write_weights:
            nx.draw_networkx_edge_labels(self.G, pos=self.pos, ax=self.ax, edge_labels={k: f"{v:.2f}" for k, v in nx.get_edge_attributes(G, 'weight').items()})
        self.route=route
        if route != None:
            self.route_lines=nx.draw_networkx_edges(self.G, pos=self.pos, ax=self.ax, arrows=True, edgelist=route, edge_color="red", style="dashed", width=2)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(self.vbox)

        self.canvas = FigureCanvas(self.fig)  # A Gtk.DrawingArea
        #canvas.set_size_request(800, 600)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)
        self.vbox.append(self.canvas)

        # Create toolbar
        self.toolbar = NavigationToolbar(self.canvas)
        self.vbox.append(self.toolbar)

        # Route
        # route_str="Route:"
        # for edge in self.route:
        #     route_str+=f'{edge[0]}→{edge[1]}(weight={self.G.get_edge_data(edge[0],edge[1])["weight"]:.1f}), '
        # route_str=route_str[:-2]
        # self.route_scroll=Gtk.ScrolledWindow()
        # self.route_scroll.max_content_height=50
        # self.route_label = Gtk.Label()
        # self.route_label.set_wrap(True)
        # self.route_label.set_label(route_str)
        # self.route_scroll.set_child(self.route_label)
        # self.vbox.append(self.route_scroll)


    def update(self,route:list=None, title:str=""):
        self.ax.title.set_text(title)
        if self.route != route:
            self.route=route
            for line in self.route_lines:
                line.remove()
            self.route_lines.clear()
            self.route_lines=nx.draw_networkx_edges(self.G, pos=self.pos, ax=self.ax, arrows=True, edgelist=route, edge_color="red", style="dashed", width=2)
        self.canvas.draw()




class Gtk4Mplt(Gtk.ScrolledWindow):
    __gtype_name__ = 'Gtk4Mplt'
    def __init__(self,figsize=(5, 4), dpi=100):
        # # Create the main application window
        # win = Gtk.ApplicationWindow(application=app)
        # win.set_default_size(600, 400)
        # win.set_title("NetworkX DiGraph in GTK4")
        # Create a scrolled window and add the Matplotlib canvas
        super().__init__(margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)

        # Create a Matplotlib figure and axes
        self.fig = Figure(figsize=figsize, dpi=dpi)
        self.ax = self.fig.add_subplot()


        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_child(vbox)

        self.canvas = FigureCanvas(self.fig)  # A Gtk.DrawingArea
        #canvas.set_size_request(800, 600)
        self.canvas.set_hexpand(True)
        self.canvas.set_vexpand(True)
        vbox.append(self.canvas)

        # Create toolbar
        self.toolbar = NavigationToolbar(self.canvas)
        vbox.append(self.toolbar)

