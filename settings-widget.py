from dataclasses import dataclass
from typing import Optional, List, Union, Any

@dataclass
class Parameters:
    options: Optional[List[str]] = None        # For dropdown options
    custom_allowed: bool = False               # Allow custom input in dropdown
    min: Optional[Union[int, float]] = None    # Minimum value for int/float
    max: Optional[Union[int, float]] = None    # Maximum value for int/float

@dataclass
class Setting:
    name: str
    type: str                 # 'bool', 'int', 'float', 'str'
    default: Any
    value: Any
    parameters: Optional[Parameters] = None

class CustomDropDown(Gtk.Box):
    """ Composite widget combining a DropDown with an Entry for custom values. Only appends "Other" option when custom_allowed=True. """
    gtype_name = 'CustomDropDown'

def __init__(self,
             options: List[str],
             default_value: Optional[str] = None,
             custom_allowed: bool = False):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
    self.options = options.copy()
    self.custom_allowed = custom_allowed

    if self.custom_allowed:
        self.options.append("Other")

    # Create a ListStore for the dropdown
    self.store = Gio.ListStore.new(GObject.TYPE_STRING)
    for opt in self.options:
        self.store.append(opt)

    # Dropdown
    self.dropdown = Gtk.DropDown(model=self.store)
    self.dropdown.connect("notify::selected", self._on_selection_changed)
    self.append(self.dropdown)

    # Text entry for custom input
    self.entry = Gtk.Entry(placeholder_text="Enter custom value")
    self.entry.connect("changed", self._on_entry_changed)
    self.entry.set_visible(False)
    self.append(self.entry)

    # Initialize default selection
    if default_value in options:
        self.dropdown.set_selected(options.index(default_value))
    elif default_value and self.custom_allowed:
        self.dropdown.set_selected(len(self.options) - 1)
        self.entry.set_text(default_value)
        self.entry.set_visible(True)
    else:
        self.dropdown.set_selected(0)

def _on_selection_changed(self, dropdown, _):
    idx = dropdown.get_selected()
    visible = self.custom_allowed and idx == len(self.options) - 1
    self.entry.set_visible(visible)

def _on_entry_changed(self, entry):
    # Placeholder: called when custom entry text changes
    pass

def get_value(self) -> str:
    idx = self.dropdown.get_selected()
    if self.custom_allowed and idx == len(self.options) - 1:
        return self.entry.get_text()
    return self.options[idx]

class SettingsPage(Gtk.ScrolledWindow):
    """ A GTK4 widget that displays a list of settings in a ListView. Can be embedded in any container. """
    gtype_name = 'SettingsPage'

def __init__(self, settings: List[Setting]):
    super().__init__()
    self.settings = settings

    # Create model and ListView
    self.listview = Gtk.ListView(model=self._create_list_model())
    self.listview.set_activate_on_single_click(True)
    self.listview.set_selection_mode(Gtk.SelectionMode.NONE)

    # Create factory for items
    factory = Gtk.SignalListItemFactory()
    factory.connect("bind", self._on_bind_item)
    self.listview.set_factory(factory)

    # Add ListView to the scrolled window
    self.set_child(self.listview)
    self.set_vexpand(True)
    self.set_hexpand(True)

def _create_list_model(self) -> Gtk.ListStore:
    # Columns: name, type, default, value, parameters
    types = [str, str, object, object, object]
    store = Gtk.ListStore.new(types, *[
        (s.name, s.type, s.default, s.value, s.parameters)
        for s in self.settings
    ])
    return store

def _on_bind_item(self, factory, item):
    widget = item.get_child()
    if widget:
        widget.remove_all()
    else:
        widget = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        item.set_child(widget)

    name, type_, default, value, params = item.get_item()

    # Name label
    lbl = Gtk.Label(label=name)
    lbl.set_xalign(0)
    widget.append(lbl)

    # Control widget based on setting type
    if type_ == 'bool':
        ctrl = Gtk.Switch()
        ctrl.set_active(bool(value))
        ctrl.connect('state-set', self._on_switch_changed, item.get_position())
        widget.append(ctrl)

    elif type_ in ('int', 'float'):
        ctrl = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        # apply limits only when both present
        if params and params.min is not None and params.max is not None:
            ctrl.set_range(params.min, params.max)
        ctrl.set_value(value)
        if type_ == 'float':
            ctrl.set_digits(2)
            ctrl.connect('value-changed', self._on_float_changed, item.get_position())
        else:
            ctrl.connect('value-changed', self._on_int_changed, item.get_position())
        widget.append(ctrl)

    elif type_ == 'str':
        if params and params.options:
            opts = params.options
            if params.custom_allowed:
                ctrl = CustomDropDown(opts,
                                      default_value=value,
                                      custom_allowed=True)
                ctrl.dropdown.connect('notify::selected',
                                      self._on_custom_dropdown_changed,
                                      item.get_position(), ctrl)
                ctrl.entry.connect('changed',
                                   self._on_custom_dropdown_changed,
                                   item.get_position(), ctrl)
            else:
                store = Gio.ListStore.new(GObject.TYPE_STRING)
                for opt in opts:
                    store.append(opt)
                ctrl = Gtk.DropDown(model=store)
                if value in opts:
                    ctrl.set_selected(opts.index(value))
                ctrl.connect('notify::selected',
                              self._on_dropdown_changed,
                              item.get_position(), opts)
            widget.append(ctrl)
        else:
            ctrl = Gtk.Entry()
            ctrl.set_text(str(value))
            ctrl.connect('changed', self._on_text_changed, item.get_position())
            widget.append(ctrl)

    # Default label
    default_lbl = Gtk.Label(label=f"Default: {default}")
    default_lbl.set_xalign(1)
    widget.append(default_lbl)

# Signal handlers updating the model
def _on_switch_changed(self, switch, state, pos):
    model = self.listview.get_model()
    model[pos][3] = bool(state)
    model.row_changed(pos)

def _on_int_changed(self, scale, pos):
    model = self.listview.get_model()
    model[pos][3] = int(scale.get_value())
    model.row_changed(pos)

def _on_float_changed(self, scale, pos):
    model = self.listview.get_model()
    model[pos][3] = float(scale.get_value())
    model.row_changed(pos)

def _on_text_changed(self, entry, pos):
    model = self.listview.get_model()
    model[pos][3] = entry.get_text()
    model.row_changed(pos)

def _on_dropdown_changed(self, dropdown, _, pos, opts):
    model = self.listview.get_model()
    idx = dropdown.get_selected()
    model[pos][3] = opts[idx]
    model.row_changed(pos)

def _on_custom_dropdown_changed(self, widget, _, pos, custom_ctrl):
    model = self.listview.get_model()
    model[pos][3] = custom_ctrl.get_value()
    model.row_changed(pos)

def get_setting_value(self, name: str) -> Any:
    model = self.listview.get_model()
    for row in model:
        if row[0] == name:
            return row[3]
    return None

#Example usage (to be embedded in your application):



from gi.repository import Gtk



settings = [

Setting("Enable Feature X", "bool", True, True),

Setting("Volume Level", "int", 50, 75, Parameters(min=0, max=100)),

Setting("Theme", "str", "Light", "Dark",

Parameters(options=["Light","Dark","System"], custom_allowed=True)),

Setting("Username", "str", "", ""),

Setting("Opacity", "float", 1.0, 0.85, Parameters(min=0.0, max=1.0)),

Setting("Threshold", "int", 10, 15)  # No limits

]



page = SettingsPage(settings)



window = Gtk.Window()

window.set_child(page)

window.show()

