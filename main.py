#!/usr/bin/python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib
import networkx as nx
import threading
import sys
import random
from mplt import Gtk4MpltNx, Gtk4Mplt
from settings import SettingsWidget
from gen_graph import make_graph
from ga import GA
from aco import ACO
from HybridGAACO import HybridGAACO


class MyWindow(Gtk.ApplicationWindow):
    anim=False
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Hello GTK")
        self.set_default_size(300, 100)
        self.set_icon_name("org.artemis.ea")

        self.settings = SettingsWidget()
        self.settings.connect("run", self.on_run_clicked)
        self.set_child(self.settings)
        self.mplts=[]
        self.mpltsbox=None

    def on_run_clicked(self, settings, data:dict):
        print("Button clicked!")
        self.n_cities=data["n_cities"][0]
        for i in range(self.n_cities):
            G = make_graph(data["nodes"][0],data["edge_probability"][0],data["min_traffic"][0],data["max_traffic"][0],data["seed"][0]+str(i) if not data["seed"][0]=="None" else None)
            threading.Thread(target=self.run_task,args=(data,G,i),daemon=True).start()
            if self.anim:
                self.show_mpltnx(G,True,False,None,f'Iteration:  (Distance: )')
                self.update_i=0;


    def run_task(self,data:dict,G:nx.DiGraph,iteration:int):
        random.seed(data["training_seed"][0]+str(iteration) if not data["training_seed"][0]=="None" else None)
        print(data["type"][0])
        route=[]
        distance=0
        history=tuple()
        update_callback=lambda i,r,d,t: self.update_cb(i,r,d,t,iteration)
        if data["type"][0]=="GA":
            ga=GA(G,pop_size=data["ga_n_pop"][0],mutation_rate=data["ga_mutation_rate"][0],update_callback=update_callback)
            routes,history=ga.create_solution(data["ga_i"][0])
            route = routes[0]
            distance=ga.route_distance(route)
        elif data["type"][0]=="ACO":
            aco = ACO(G, n_ants=data["aco_n_ants"][0], alpha=data["aco_alpha"][0], beta=data["aco_beta"][0], evaporation=data["aco_evaporation"][0],update_callback=update_callback)
            route, distance, history = aco.run_aco(iterations=data["aco_i"][0])
        elif data["type"][0]=="HYBGA":
            HybridGAACO_TEST= HybridGAACO(G,pop_size=data["ga_n_pop_2"][0],mutation_rate=data["ga_mutation_rate_2"][0], n_ants=data["aco_n_ants_2"][0], alpha=data["aco_alpha_2"][0], beta=data["aco_beta_2"][0], evaporation=data["aco_evaporation_2"][0],update_callback=update_callback)
            route,distance,history=HybridGAACO_TEST.run_ga_plus_aco(ga_generations=data["ga_i_2"][0], aco_iterations=data["aco_i_2"][0], cycles=5)
        elif data["type"][0]=="HYBAG":
            HybridGAACO_TEST= HybridGAACO(G,pop_size=data["ga_n_pop_3"][0],mutation_rate=data["ga_mutation_rate_3"][0], n_ants=data["aco_n_ants_3"][0], alpha=data["aco_alpha_3"][0], beta=data["aco_beta_3"][0], evaporation=data["aco_evaporation_3"][0],update_callback=update_callback)
            route,distance,history=HybridGAACO_TEST.run_aco_plus_ga(ga_generations=data["ga_i_3"][0], aco_iterations=data["aco_i_3"][0], cycles=5)
        route_edges=[(route[i],route[i+1]) for i in range(len(route)-1)]
        GLib.idle_add(self.show_mpltnx,G,True,False,route_edges,f'Solution (Distance: {distance:.2f})', history, iteration, priority=-200)

    def show_mpltnx(self,graph: nx.DiGraph, pos_available: bool=True, write_weights: bool=True, route: list=None, title: str="", history=tuple(), i:int=0):
        if not self.mpltsbox:
            self.mpltsboxscroll=Gtk.ScrolledWindow()
            self.mpltsbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            self.mpltsboxscroll.set_child(self.mpltsbox)
            self.set_child(self.mpltsboxscroll)
            self.set_default_size(1800,600)

        mpltnx=Gtk4MpltNx(graph,pos_available,write_weights,route,title)
        mplthist_abs=Gtk4Mplt()
        mplthist_abs.ax.plot(history[1],label='average')
        mplthist_abs.ax.plot(history[0],label='best')
        mplthist_abs.ax.legend()
        mplthist_abs.ax.set_title('Distance per iteration')
        mplthist_d=Gtk4Mplt()
        best_d=[i-j for i,j in zip(history[0][:-1],history[0][1:])]
        avg_d=[i-j for i,j in zip(history[1][:-1],history[1][1:])]
        mplthist_d.ax.plot(avg_d,label='average')
        mplthist_d.ax.plot(best_d,label='best')
        mplthist_d.ax.legend()
        mplthist_d.ax.set_title('Distance decrease per iteration')
        info_label_box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        route_str="Route: "
        for edge in route:
            route_str+=f'{edge[0]}→{edge[1]}(weight={graph.get_edge_data(edge[0],edge[1])["weight"]:.1f}), '
        route_str=route_str[:-2]
        graph_str="Nodes: "
        for node in list(graph.nodes):
            graph_str+=f'{node}, '
        graph_str=graph_str[:-2]+"\n\n"
        graph_str+="Edges: "
        for edge in graph.edges:
            graph_str+=f'{edge[0]}→{edge[1]}(weight={graph.get_edge_data(edge[0],edge[1])["weight"]:.1f}), '
        graph_str=graph_str[:-2]
        route_scroll_label=Gtk.ScrolledWindow(min_content_width=300,min_content_height=200,margin_bottom=30,child=Gtk.Label(wrap=True,label=route_str,vexpand=True))
        graph_scroll_label=Gtk.ScrolledWindow(min_content_width=300,min_content_height=200,margin_bottom=30,child=Gtk.Label(wrap=True,label=graph_str,vexpand=True))
        info_label_box.append(route_scroll_label)
        info_label_box.append(graph_scroll_label)
        currentbox=Gtk.Box()
        currentbox.append(mpltnx)
        currentbox.append(mplthist_abs)
        currentbox.append(mplthist_d)
        currentbox.append(info_label_box)
        self.mplts.append(mpltnx)
        self.mpltsbox.append(currentbox)
        return False

    def update_cb(self,i,r,d,t,run):
        # print(i)
        # print(t)
        # print(i/t)
        if self.anim and (i%100==0):
            self.update_mpltnx(r,f'Iteration: {i} (Distance: {d:.2f})',i)
        else:
            if run==0:
                GLib.idle_add(self.settings.progress_update,i/t, priority=-50)
        return None
    def update_mpltnx(self,route:list,title,i):
        if i>self.update_i:
            self.update_i=i;
            print(f'{title} Route(start): {route}',file=sys.stderr)
            route_edges=[(route[i],route[i+1]) for i in range(len(route)-1)]
            self.mpltnx.update(route_edges,title)
        return False


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.artemis.ea")

    def do_activate(self):
        win = MyWindow(self)
        win.present()

app = MyApp()
app.run()
