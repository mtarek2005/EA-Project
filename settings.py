import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject

@Gtk.Template(filename="settings.ui")
class SettingsWidget(Gtk.Box):
    __gtype_name__ = "SettingsWidget"

    label = Gtk.Template.Child()
    run_button = Gtk.Template.Child()
    edges_entry = Gtk.Template.Child()



    def __init__(self):
        super().__init__()
        self.settings={'edges':["[('A', 'B'), ('B', 'C'), ('C', 'A'), ('C', 'D')]",self.edges_entry,self.edges_entry.get_text]}

    @Gtk.Template.Callback()
    def on_run_button_clicked(self, button):
        self.label.set_text("Button clicked!")
        for value in self.settings.values():
            value[0]=value[2]()
        self.emit("run",self.settings)

    @GObject.Signal(arg_types=(GObject.TYPE_PYOBJECT,))
    def run(self, data):
        pass
