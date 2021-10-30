import bpy

from . import panel_ui


class KUCHIPAKU_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    category: bpy.props.StringProperty(  # type: ignore
        default="KuchiPaku", name="Addon Tab", update=panel_ui.update_panel
    )

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        col = layout.column()
        col.prop(self, "category")
