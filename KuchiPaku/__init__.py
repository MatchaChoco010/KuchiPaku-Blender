import os
import sys

import bpy

sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

__all__ = ["auto_load", "operators", "panel_ui", "preferences", "property_group"]
from . import auto_load, operators, panel_ui, preferences, property_group  # noqa: E402

bl_info = {
    "name": "KuchiPaku",
    "author": "Orito Itsuki",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Animation",
}

auto_load.init()


def register() -> None:
    sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
    auto_load.register()
    property_group.register_props()
    panel_ui.update_panel(None, bpy.context)


def unregister() -> None:
    sys.path.remove(os.path.join(os.path.dirname(__file__), "lib"))
    auto_load.unregister()
    property_group.unregister_props()
