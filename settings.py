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
    map_seed_entry = Gtk.Template.Child()
    train_seed_entry = Gtk.Template.Child()
    type_dropdown = Gtk.Template.Child()
    progress = Gtk.Template.Child()



    def __init__(self):
        super().__init__()
        types={"ACO":0,"GA":1,"HYBGA":2,"HYBAG":2}
        self.settings={'nodes':[25,self.nodes_spinbutton,self.nodes_spinbutton.get_value_as_int,self.nodes_spinbutton.set_value],
                       'edge_probability':[0.05,self.edge_probability_spinbutton,self.edge_probability_spinbutton.get_value,self.edge_probability_spinbutton.set_value],
                       'min_traffic':[1.0,self.min_traffic_spinbutton,self.min_traffic_spinbutton.get_value,self.min_traffic_spinbutton.set_value],
                       'max_traffic':[2.0,self.max_traffic_spinbutton,self.max_traffic_spinbutton.get_value,self.max_traffic_spinbutton.set_value],
                       'seed':["0",self.map_seed_entry,self.map_seed_entry.get_text,self.map_seed_entry.set_text],
                       'training_seed':["0",self.train_seed_entry,self.train_seed_entry.get_text,self.train_seed_entry.set_text],
                       'type':["HYBGA",self.type_dropdown,lambda: list(types)[self.type_dropdown.get_selected()],lambda x:self.type_dropdown.set_selected(types[x])],
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

    @GObject.Signal(arg_types=(GObject.TYPE_PYOBJECT,))
    def run(self, data):
        pass

    def progress_update(self,frac:float):
        self.progress.set_fraction(frac)
