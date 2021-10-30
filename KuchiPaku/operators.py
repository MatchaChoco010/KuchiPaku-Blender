import os
from typing import Set

import bpy
import librosa
import numpy as np
from bpy_extras.io_utils import ImportHelper
from numpy import dot
from numpy.linalg import norm

from . import property_group


class KUCHIPAKU_OT_SelectA(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_a"
    bl_label = "select 'A' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.a_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SelectI(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_i"
    bl_label = "select 'I' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.i_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SelectU(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_u"
    bl_label = "select 'U' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.u_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SelectE(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_e"
    bl_label = "select 'E' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.e_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SelectO(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_o"
    bl_label = "select 'O' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.o_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SelectN(bpy.types.Operator, ImportHelper):
    bl_idname = "orito_itsuki.kuchipaku_select_n"
    bl_label = "select 'N' file"
    bl_options = {"REGISTER", "UNDO"}

    directory: bpy.props.StringProperty(subtype="DIR_PATH")  # type: ignore
    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)  # type: ignore
    filter_glob: bpy.props.StringProperty(default="*.wav")  # type: ignore

    def execute(self, context: bpy.types.Context) -> Set[str]:
        dirname = os.path.dirname(self.filepath)
        context.scene.kuchipaku.n_file = os.path.join(dirname, self.files[0].name)
        return {"FINISHED"}


class KUCHIPAKU_OT_SetUpCurve(bpy.types.Operator):
    bl_idname = "orito_itsuki.kuchipaku_setup_curve"
    bl_label = "SetUp curve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context) -> Set[str]:
        property_group.SetUpCurveData()
        return {"FINISHED"}


class KUCHIPAKU_OT_Main(bpy.types.Operator):
    bl_idname = "orito_itsuki.kuchipaku_main"
    bl_label = "Create NLA"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        props = context.scene.kuchipaku
        return (
            props.a_file != ""
            and props.i_file != ""
            and props.u_file != ""
            and props.e_file != ""
            and props.o_file != ""
            and props.mesh is not None
            and props.a_shape_key != ""
            and props.i_shape_key != ""
            and props.u_shape_key != ""
            and props.e_shape_key != ""
            and props.o_shape_key != ""
            and props.n_shape_key != ""
            and props.action_name != ""
            and property_group.CurveData() is not None
        )

    def execute(self, context: bpy.types.Context) -> Set[str]:
        props = context.scene.kuchipaku

        a_audio, sr = librosa.load(props.a_file, sr=None)
        a_mfccs = librosa.feature.mfcc(
            y=a_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        i_audio, sr = librosa.load(props.i_file, sr=None)
        i_mfccs = librosa.feature.mfcc(
            y=i_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        u_audio, sr = librosa.load(props.u_file, sr=None)
        u_mfccs = librosa.feature.mfcc(
            y=u_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        e_audio, sr = librosa.load(props.e_file, sr=None)
        e_mfccs = librosa.feature.mfcc(
            y=e_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        o_audio, sr = librosa.load(props.o_file, sr=None)
        o_mfccs = librosa.feature.mfcc(
            y=o_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        n_audio, sr = librosa.load(props.n_file, sr=None)
        n_mfccs = librosa.feature.mfcc(
            y=n_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=2400,
            window="hann",
            lifter=60,
        )

        tmp_file = os.path.join(bpy.app.tempdir, "tmp_audio.flac")
        bpy.ops.sound.mixdown(filepath=tmp_file, container="FLAC")
        mixdown_audio, sr = librosa.load(tmp_file, sr=None)
        mixdown_mfccs = librosa.feature.mfcc(
            y=mixdown_audio,
            sr=sr,
            n_mfcc=20,
            dct_type=3,
            hop_length=sr // (context.scene.render.fps * 8),
            window="hann",
            lifter=60,
        )
        mixdown_dbs = librosa.amplitude_to_db(
            librosa.feature.rms(
                y=mixdown_audio,
                hop_length=sr // (context.scene.render.fps * 8),
            ),
        )

        inferences = np.zeros((7, mixdown_dbs.shape[1]))
        for i, (mfcc, db) in enumerate(zip(mixdown_mfccs.T, mixdown_dbs.T)):
            a_norm = dot(a_mfccs.T, mfcc) / (norm(a_mfccs.T, axis=1) * norm(mfcc))
            a_norm = np.average(a_norm)

            i_norm = dot(i_mfccs.T, mfcc) / (norm(i_mfccs.T, axis=1) * norm(mfcc))
            i_norm = np.average(i_norm)

            u_norm = dot(u_mfccs.T, mfcc) / (norm(u_mfccs.T, axis=1) * norm(mfcc))
            u_norm = np.average(u_norm)

            e_norm = dot(e_mfccs.T, mfcc) / (norm(e_mfccs.T, axis=1) * norm(mfcc))
            e_norm = np.average(e_norm)

            o_norm = dot(o_mfccs.T, mfcc) / (norm(o_mfccs.T, axis=1) * norm(mfcc))
            o_norm = np.average(o_norm)

            n_norm = dot(n_mfccs.T, mfcc) / (norm(n_mfccs.T, axis=1) * norm(mfcc))
            n_norm = np.average(n_norm)

            if db >= props.threshold_db:
                inferences[
                    np.argmax([a_norm, i_norm, u_norm, e_norm, o_norm, n_norm]), i
                ] = 1
            inferences[6, i] = db

        for _ in range(8 - inferences.shape[1] % 8):
            inferences = np.insert(inferences, -1, 0, axis=1)
        inferences = np.stack(np.split(inferences, inferences.shape[1] // 8, axis=1))
        inferences = np.average(inferences, axis=2)

        action = bpy.data.actions.get(props.action_name)
        if action is None:
            action = bpy.data.actions.new(props.action_name)
        action.use_fake_user = True

        a_curve = action.fcurves.find(f'key_blocks["{props.a_shape_key}"].value')
        if a_curve is not None:
            action.fcurves.remove(a_curve)
        a_curve = action.fcurves.new(f'key_blocks["{props.a_shape_key}"].value')

        i_curve = action.fcurves.find(f'key_blocks["{props.i_shape_key}"].value')
        if i_curve is not None:
            action.fcurves.remove(i_curve)
        i_curve = action.fcurves.new(f'key_blocks["{props.i_shape_key}"].value')

        u_curve = action.fcurves.find(f'key_blocks["{props.u_shape_key}"].value')
        if u_curve is not None:
            action.fcurves.remove(u_curve)
        u_curve = action.fcurves.new(f'key_blocks["{props.u_shape_key}"].value')

        e_curve = action.fcurves.find(f'key_blocks["{props.e_shape_key}"].value')
        if e_curve is not None:
            action.fcurves.remove(e_curve)
        e_curve = action.fcurves.new(f'key_blocks["{props.e_shape_key}"].value')

        o_curve = action.fcurves.find(f'key_blocks["{props.o_shape_key}"].value')
        if o_curve is not None:
            action.fcurves.remove(o_curve)
        o_curve = action.fcurves.new(f'key_blocks["{props.o_shape_key}"].value')

        n_curve = action.fcurves.find(f'key_blocks["{props.n_shape_key}"].value')
        if n_curve is not None:
            action.fcurves.remove(n_curve)
        n_curve = action.fcurves.new(f'key_blocks["{props.n_shape_key}"].value')

        curve: bpy.types.ShaderNodeRGBCurve = property_group.CurveData()
        for i, inference in enumerate(inferences):
            scale = curve.mapping.evaluate(curve.mapping.curves[3], inference[6])
            a_curve.keyframe_points.insert(frame=i + 1, value=inference[0] * scale)
            i_curve.keyframe_points.insert(frame=i + 1, value=inference[1] * scale)
            u_curve.keyframe_points.insert(frame=i + 1, value=inference[2] * scale)
            e_curve.keyframe_points.insert(frame=i + 1, value=inference[3] * scale)
            o_curve.keyframe_points.insert(frame=i + 1, value=inference[4] * scale)
            n_curve.keyframe_points.insert(frame=i + 1, value=inference[5] * scale)

        return {"FINISHED"}
