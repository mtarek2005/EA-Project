import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject

@Gtk.Template(filename="settings.ui")
class SettingsWidget(Gtk.Box):
    __gtype_name__ = "SettingsWidget"

    # label = Gtk.Template.Child()
    run_button = Gtk.Template.Child()
    nodes_spinbutton = Gtk.Template.Child()
    edge_probability_spinbutton = Gtk.Template.Child()
    min_traffic_spinbutton = Gtk.Template.Child()
    max_traffic_spinbutton = Gtk.Template.Child()
    n_cities_spinbutton = Gtk.Template.Child()
    map_seed_entry = Gtk.Template.Child()
    train_seed_entry = Gtk.Template.Child()
    type_dropdown = Gtk.Template.Child()
    options_stack = Gtk.Template.Child()
    progress = Gtk.Template.Child()

    aco_i_spinbutton = Gtk.Template.Child()
    aco_n_ants_spinbutton = Gtk.Template.Child()
    aco_alpha_spinbutton = Gtk.Template.Child()
    aco_beta_spinbutton = Gtk.Template.Child()
    aco_evaporation_spinbutton = Gtk.Template.Child()
    ga_i_spinbutton = Gtk.Template.Child()
    ga_n_pop_spinbutton = Gtk.Template.Child()
    ga_mutation_rate_spinbutton = Gtk.Template.Child()
    ga_i_spinbutton_2 = Gtk.Template.Child()
    ga_n_pop_spinbutton_2 = Gtk.Template.Child()
    ga_mutation_rate_spinbutton_2 = Gtk.Template.Child()
    aco_i_spinbutton_2 = Gtk.Template.Child()
    aco_n_ants_spinbutton_2 = Gtk.Template.Child()
    aco_alpha_spinbutton_2 = Gtk.Template.Child()
    aco_beta_spinbutton_2 = Gtk.Template.Child()
    aco_evaporation_spinbutton_2 = Gtk.Template.Child()
    aco_i_spinbutton_3 = Gtk.Template.Child()
    aco_n_ants_spinbutton_3 = Gtk.Template.Child()
    aco_alpha_spinbutton_3 = Gtk.Template.Child()
    aco_beta_spinbutton_3 = Gtk.Template.Child()
    aco_evaporation_spinbutton_3 = Gtk.Template.Child()
    ga_i_spinbutton_3 = Gtk.Template.Child()
    ga_n_pop_spinbutton_3 = Gtk.Template.Child()
    ga_mutation_rate_spinbutton_3 = Gtk.Template.Child()



    def __init__(self):
        super().__init__()
        self.types={"ACO":0,"GA":1,"HYBGA":2,"HYBAG":2}
        self.settings={'nodes':[25,self.nodes_spinbutton,self.nodes_spinbutton.get_value_as_int,self.nodes_spinbutton.set_value],
                       'edge_probability':[0.05,self.edge_probability_spinbutton,self.edge_probability_spinbutton.get_value,self.edge_probability_spinbutton.set_value],
                       'min_traffic':[1.0,self.min_traffic_spinbutton,self.min_traffic_spinbutton.get_value,self.min_traffic_spinbutton.set_value],
                       'max_traffic':[2.0,self.max_traffic_spinbutton,self.max_traffic_spinbutton.get_value,self.max_traffic_spinbutton.set_value],
                       'n_cities':[5,self.n_cities_spinbutton,self.n_cities_spinbutton.get_value_as_int,self.n_cities_spinbutton.set_value],
                       'seed':["0",self.map_seed_entry,self.map_seed_entry.get_text,self.map_seed_entry.set_text],
                       'training_seed':["0",self.train_seed_entry,self.train_seed_entry.get_text,self.train_seed_entry.set_text],
                       'type':["ACO",self.type_dropdown,lambda: list(self.types)[self.type_dropdown.get_selected()],lambda x:self.type_dropdown.set_selected(self.types[x])],
                       'aco_i':[5,self.aco_i_spinbutton,self.aco_i_spinbutton.get_value_as_int,self.aco_i_spinbutton.set_value],
                       'aco_n_ants':[5,self.aco_n_ants_spinbutton,self.aco_n_ants_spinbutton.get_value_as_int,self.aco_n_ants_spinbutton.set_value],
                       'aco_alpha':[0.5,self.aco_alpha_spinbutton,self.aco_alpha_spinbutton.get_value,self.aco_alpha_spinbutton.set_value],
                       'aco_beta':[0.5,self.aco_beta_spinbutton,self.aco_beta_spinbutton.get_value,self.aco_beta_spinbutton.set_value],
                       'aco_evaporation':[0.5,self.aco_evaporation_spinbutton,self.aco_evaporation_spinbutton.get_value,self.aco_evaporation_spinbutton.set_value],
                       'ga_i':[5,self.ga_i_spinbutton,self.ga_i_spinbutton.get_value_as_int,self.ga_i_spinbutton.set_value],
                       'ga_n_pop':[5,self.ga_n_pop_spinbutton,self.ga_n_pop_spinbutton.get_value_as_int,self.ga_n_pop_spinbutton.set_value],
                       'ga_mutation_rate':[0.5,self.ga_mutation_rate_spinbutton,self.ga_mutation_rate_spinbutton.get_value,self.ga_mutation_rate_spinbutton.set_value],
                       'ga_i_2':[5,self.ga_i_spinbutton_2,self.ga_i_spinbutton_2.get_value_as_int,self.ga_i_spinbutton_2.set_value],
                       'ga_n_pop_2':[5,self.ga_n_pop_spinbutton_2,self.ga_n_pop_spinbutton_2.get_value_as_int,self.ga_n_pop_spinbutton_2.set_value],
                       'ga_mutation_rate_2':[0.5,self.ga_mutation_rate_spinbutton_2,self.ga_mutation_rate_spinbutton_2.get_value,self.ga_mutation_rate_spinbutton_2.set_value],
                       'aco_i_2':[5,self.aco_i_spinbutton_2,self.aco_i_spinbutton_2.get_value_as_int,self.aco_i_spinbutton_2.set_value],
                       'aco_n_ants_2':[5,self.aco_n_ants_spinbutton_2,self.aco_n_ants_spinbutton_2.get_value_as_int,self.aco_n_ants_spinbutton_2.set_value],
                       'aco_alpha_2':[0.5,self.aco_alpha_spinbutton_2,self.aco_alpha_spinbutton_2.get_value,self.aco_alpha_spinbutton_2.set_value],
                       'aco_beta_2':[0.5,self.aco_beta_spinbutton_2,self.aco_beta_spinbutton_2.get_value,self.aco_beta_spinbutton_2.set_value],
                       'aco_evaporation_2':[0.5,self.aco_evaporation_spinbutton_2,self.aco_evaporation_spinbutton_2.get_value,self.aco_evaporation_spinbutton_2.set_value],
                       'aco_i_3':[5,self.aco_i_spinbutton_3,self.aco_i_spinbutton_3.get_value_as_int,self.aco_i_spinbutton_3.set_value],
                       'aco_n_ants_3':[5,self.aco_n_ants_spinbutton_3,self.aco_n_ants_spinbutton_3.get_value_as_int,self.aco_n_ants_spinbutton_3.set_value],
                       'aco_alpha_3':[0.5,self.aco_alpha_spinbutton_3,self.aco_alpha_spinbutton_3.get_value,self.aco_alpha_spinbutton_3.set_value],
                       'aco_beta_3':[0.5,self.aco_beta_spinbutton_3,self.aco_beta_spinbutton_3.get_value,self.aco_beta_spinbutton_3.set_value],
                       'aco_evaporation_3':[0.5,self.aco_evaporation_spinbutton_3,self.aco_evaporation_spinbutton_3.get_value,self.aco_evaporation_spinbutton_3.set_value],
                       'ga_i_3':[5,self.ga_i_spinbutton_3,self.ga_i_spinbutton_3.get_value_as_int,self.ga_i_spinbutton_3.set_value],
                       'ga_n_pop_3':[5,self.ga_n_pop_spinbutton_3,self.ga_n_pop_spinbutton_3.get_value_as_int,self.ga_n_pop_spinbutton_3.set_value],
                       'ga_mutation_rate_3':[0.5,self.ga_mutation_rate_spinbutton_3,self.ga_mutation_rate_spinbutton_3.get_value,self.ga_mutation_rate_spinbutton_3.set_value],
                       'aco_i':[5000,self.aco_i_spinbutton,self.aco_i_spinbutton.get_value_as_int,self.aco_i_spinbutton.set_value],
                       'aco_n_ants':[25,self.aco_n_ants_spinbutton,self.aco_n_ants_spinbutton.get_value_as_int,self.aco_n_ants_spinbutton.set_value],
                       'aco_alpha':[1,self.aco_alpha_spinbutton,self.aco_alpha_spinbutton.get_value,self.aco_alpha_spinbutton.set_value],
                       'aco_beta':[2,self.aco_beta_spinbutton,self.aco_beta_spinbutton.get_value,self.aco_beta_spinbutton.set_value],
                       'aco_evaporation':[0.5,self.aco_evaporation_spinbutton,self.aco_evaporation_spinbutton.get_value,self.aco_evaporation_spinbutton.set_value],
                       'ga_i':[50,self.ga_i_spinbutton,self.ga_i_spinbutton.get_value_as_int,self.ga_i_spinbutton.set_value],
                       'ga_n_pop':[50,self.ga_n_pop_spinbutton,self.ga_n_pop_spinbutton.get_value_as_int,self.ga_n_pop_spinbutton.set_value],
                       'ga_mutation_rate':[0.02,self.ga_mutation_rate_spinbutton,self.ga_mutation_rate_spinbutton.get_value,self.ga_mutation_rate_spinbutton.set_value],
                       'ga_i_2':[50,self.ga_i_spinbutton_2,self.ga_i_spinbutton_2.get_value_as_int,self.ga_i_spinbutton_2.set_value],
                       'ga_n_pop_2':[50,self.ga_n_pop_spinbutton_2,self.ga_n_pop_spinbutton_2.get_value_as_int,self.ga_n_pop_spinbutton_2.set_value],
                       'ga_mutation_rate_2':[0.02,self.ga_mutation_rate_spinbutton_2,self.ga_mutation_rate_spinbutton_2.get_value,self.ga_mutation_rate_spinbutton_2.set_value],
                       'aco_i_2':[5000,self.aco_i_spinbutton_2,self.aco_i_spinbutton_2.get_value_as_int,self.aco_i_spinbutton_2.set_value],
                       'aco_n_ants_2':[25,self.aco_n_ants_spinbutton_2,self.aco_n_ants_spinbutton_2.get_value_as_int,self.aco_n_ants_spinbutton_2.set_value],
                       'aco_alpha_2':[1,self.aco_alpha_spinbutton_2,self.aco_alpha_spinbutton_2.get_value,self.aco_alpha_spinbutton_2.set_value],
                       'aco_beta_2':[2,self.aco_beta_spinbutton_2,self.aco_beta_spinbutton_2.get_value,self.aco_beta_spinbutton_2.set_value],
                       'aco_evaporation_2':[0.5,self.aco_evaporation_spinbutton_2,self.aco_evaporation_spinbutton_2.get_value,self.aco_evaporation_spinbutton_2.set_value],
                       'aco_i_3':[500,self.aco_i_spinbutton_3,self.aco_i_spinbutton_3.get_value_as_int,self.aco_i_spinbutton_3.set_value],
                       'aco_n_ants_3':[25,self.aco_n_ants_spinbutton_3,self.aco_n_ants_spinbutton_3.get_value_as_int,self.aco_n_ants_spinbutton_3.set_value],
                       'aco_alpha_3':[1,self.aco_alpha_spinbutton_3,self.aco_alpha_spinbutton_3.get_value,self.aco_alpha_spinbutton_3.set_value],
                       'aco_beta_3':[2,self.aco_beta_spinbutton_3,self.aco_beta_spinbutton_3.get_value,self.aco_beta_spinbutton_3.set_value],
                       'aco_evaporation_3':[0.5,self.aco_evaporation_spinbutton_3,self.aco_evaporation_spinbutton_3.get_value,self.aco_evaporation_spinbutton_3.set_value],
                       'ga_i_3':[50,self.ga_i_spinbutton_3,self.ga_i_spinbutton_3.get_value_as_int,self.ga_i_spinbutton_3.set_value],
                       'ga_n_pop_3':[50,self.ga_n_pop_spinbutton_3,self.ga_n_pop_spinbutton_3.get_value_as_int,self.ga_n_pop_spinbutton_3.set_value],
                       'ga_mutation_rate_3':[0.02,self.ga_mutation_rate_spinbutton_3,self.ga_mutation_rate_spinbutton_3.get_value,self.ga_mutation_rate_spinbutton_3.set_value],
                       }
        for value in self.settings.values():
            value[3](value[0])

    @Gtk.Template.Callback()
    def on_run_button_clicked(self, button):
        # self.label.set_text("Button clicked!")
        self.run_button.set_sensitive(False)
        self.run_button.set_label("Processing...")
        for value in self.settings.values():
            value[0]=value[2]()
        self.emit("run",self.settings)

    @Gtk.Template.Callback()
    def on_type_dropdown_selected(self, dropdown, data):
        # self.label.set_text("Button clicked!")
        print(dropdown.get_selected())
        self.options_stack.set_visible_child(self.options_stack.get_pages().get_item(dropdown.get_selected()).get_child())

    @GObject.Signal(arg_types=(GObject.TYPE_PYOBJECT,))
    def run(self, data):
        pass

    def progress_update(self,frac:float):
        self.progress.set_fraction(frac)
