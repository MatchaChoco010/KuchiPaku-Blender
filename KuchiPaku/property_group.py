from typing import List, Tuple, Union

import bpy


def register_props() -> None:
    bpy.types.Scene.kuchipaku = bpy.props.PointerProperty(type=KUCHIPAKU_Props)


def unregister_props() -> None:
    del bpy.types.Scene.kuchipaku


def SetUpCurveData() -> None:
    props = bpy.context.scene.kuchipaku
    if "CurveData" not in bpy.data.node_groups:
        node_group = bpy.data.node_groups.new("CurveData", "ShaderNodeTree")
        node_group.use_fake_user = True
    if bpy.data.node_groups["CurveData"].nodes.get("KuchiPakuCurve") is None:
        curve = bpy.data.node_groups["CurveData"].nodes.new("ShaderNodeRGBCurve")
        curve.name = "KuchiPakuCurve"
    curve = bpy.data.node_groups["CurveData"].nodes["KuchiPakuCurve"]
    curve.mapping.clip_max_x = props.max_db
    curve.mapping.clip_min_x = props.threshold_db
    curve.mapping.clip_max_y = 1
    curve.mapping.clip_min_y = 0
    curve.mapping.use_clip = True
    curve.mapping.curves[3].points[0].location[0] = curve.mapping.clip_min_x
    curve.mapping.curves[3].points[1].location[0] = curve.mapping.clip_max_x
    curve.mapping.update()
    curve.mapping.reset_view()


def CurveData() -> Union[None, bpy.types.ShaderNodeRGBCurve]:
    if bpy.data.node_groups.get("CurveData") is None:
        return None
    if bpy.data.node_groups["CurveData"].nodes.get("KuchiPakuCurve") is None:
        return None
    return bpy.data.node_groups["CurveData"].nodes["KuchiPakuCurve"]


class KUCHIPAKU_Props(bpy.types.PropertyGroup):
    bl_idname = "KUCHIPAKU_Props"

    a_file: bpy.props.StringProperty()  # type: ignore
    i_file: bpy.props.StringProperty()  # type: ignore
    u_file: bpy.props.StringProperty()  # type: ignore
    e_file: bpy.props.StringProperty()  # type: ignore
    o_file: bpy.props.StringProperty()  # type: ignore
    n_file: bpy.props.StringProperty()  # type: ignore

    def update_curve_data(self, context: bpy.types.Context) -> None:
        props = context.scene.kuchipaku
        curve = CurveData()
        if curve is None:
            return
        old_max = curve.mapping.clip_max_x
        old_min = curve.mapping.clip_min_x
        curve.mapping.clip_max_x = max(props.max_db, props.threshold_db + 1)
        curve.mapping.clip_min_x = props.threshold_db
        for p in curve.mapping.curves[3].points:
            p.location[0] = (p.location[0] - old_min) / (old_max - old_min) * (
                curve.mapping.clip_max_x - curve.mapping.clip_min_x
            ) + curve.mapping.clip_min_x
        curve.mapping.update()
        curve.mapping.reset_view()

    threshold_db: bpy.props.IntProperty(  # type: ignore
        default=-50,
        update=update_curve_data,
        min=-100,
        max=50,
    )
    max_db: bpy.props.IntProperty(  # type: ignore
        default=50,
        update=update_curve_data,
        min=-100,
        max=100,
    )

    mesh: bpy.props.PointerProperty(type=bpy.types.Mesh)  # type: ignore

    def shape_keys(self, context: bpy.types.Context) -> List[Tuple[str, str, str]]:
        props = context.scene.kuchipaku
        ret: List[Tuple[str, str, str]] = []
        if props.mesh.shape_keys is None or props.mesh.shape_keys.key_blocks is None:
            return ret
        for key_block in props.mesh.shape_keys.key_blocks:
            ret.append((key_block.name, key_block.name, ""))
        return ret

    a_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore
    i_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore
    u_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore
    e_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore
    o_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore
    n_shape_key: bpy.props.EnumProperty(items=shape_keys)  # type: ignore

    action_name: bpy.props.StringProperty(default="lip-sync")  # type: ignore
