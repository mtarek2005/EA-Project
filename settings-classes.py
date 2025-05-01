from dataclasses import dataclass
from typing import Optional, List, Union, Any

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject

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