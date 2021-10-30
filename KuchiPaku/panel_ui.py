from typing import List, Optional

import bpy

from . import property_group


def update_panel(
    self: Optional[bpy.props.StringProperty], context: bpy.types.Context
) -> None:
    panels: List[bpy.types.Panel] = [KUCHIPAKU_PT_MainPanel]

    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)
            panel.bl_category = context.preferences.addons[
                __package__
            ].preferences.category
            bpy.utils.register_class(panel)
    except Exception:
        pass


class KUCHIPAKU_PT_MainPanel(bpy.types.Panel):
    bl_label = "KuchiPaku"
    bl_idname = "KUCHIPAKU_PT_MainPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bpy.types.Context) -> None:
        layout = self.layout
        props = context.scene.kuchipaku

        box = layout.box()
        box.label(text="Calibration '*.wav' files")
        row = box.row(align=True)
        row.prop(props, "a_file", text="'A' .wav")
        row.operator("orito_itsuki.kuchipaku_select_a", icon="FILE_FOLDER", text="")
        row = box.row(align=True)
        row.prop(props, "i_file", text="'I' .wav")
        row.operator("orito_itsuki.kuchipaku_select_i", icon="FILE_FOLDER", text="")
        row = box.row(align=True)
        row.prop(props, "u_file", text="'U' .wav")
        row.operator("orito_itsuki.kuchipaku_select_u", icon="FILE_FOLDER", text="")
        row = box.row(align=True)
        row.prop(props, "e_file", text="'E' .wav")
        row.operator("orito_itsuki.kuchipaku_select_e", icon="FILE_FOLDER", text="")
        row = box.row(align=True)
        row.prop(props, "o_file", text="'O' .wav")
        row.operator("orito_itsuki.kuchipaku_select_o", icon="FILE_FOLDER", text="")
        row = box.row(align=True)
        row.prop(props, "n_file", text="'N' .wav")
        row.operator("orito_itsuki.kuchipaku_select_n", icon="FILE_FOLDER", text="")

        box = layout.box()
        col = box.column()
        col.prop(props, "mesh")
        if props.mesh is not None:
            col.prop(props, "a_shape_key", text="'A' ShapeKey")
            col.prop(props, "i_shape_key", text="'I' ShapeKey")
            col.prop(props, "u_shape_key", text="'U' ShapeKey")
            col.prop(props, "e_shape_key", text="'E' ShapeKey")
            col.prop(props, "o_shape_key", text="'O' ShapeKey")
            col.prop(props, "n_shape_key", text="'N' ShapeKey")

        col = box.column()
        col.prop(props, "threshold_db", text="Threshold dB")
        col.prop(props, "max_db", text="Max dB")

        col = box.column()
        if property_group.CurveData() is None:
            col.operator(
                "orito_itsuki.kuchipaku_setup_curve", text="SetUp Mouth Open Curve"
            )
        else:
            col.template_curve_mapping(property_group.CurveData(), "mapping")

        col = layout.column()
        col.prop(props, "action_name", text="Action Name")
        col.operator("orito_itsuki.kuchipaku_main", text="Create LipSync Action")
