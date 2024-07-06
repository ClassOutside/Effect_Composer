import bpy
import ntpath
from ..operations.GridDefs import set_sequencer_head_to_frame_zero, getSequenceEditorArea, fillListToGridSize, set_clip_position, keyframe_transform_strips, swap_item_to_first_position, set_render_end_frame_to_first_channel_length
from ..operations.CrossFadeDefs import load_strips_to_sequencer, add_gamma_cross_transitions, set_sequence_end_frame_to_max

class EffectComposerCrossFadePopupOperator(bpy.types.Operator):
    bl_idname = "wm.effect_composer_cross_fade_popup"
    bl_label = "Cross Fade Popup"

    fadeDuration: bpy.props.IntProperty (name="Fade Duration", default=30)

    def execute(self, context):
        if context.scene.effect_composer_items:
            load_strips_to_sequencer(self, context, self.fadeDuration)
            add_gamma_cross_transitions(bpy.context.scene)
            set_sequence_end_frame_to_max(bpy.context.scene)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        layout.label(text="Selected Files:")
        files = [ntpath.basename(item.name) for item in context.scene.effect_composer_items]
        layout.prop_menu_enum(self, "selected_files", text="Files", icon='FILE')

        layout.label(text="Target:")
        zoom_target_path = context.scene.get('ZoomTargetPath', '')
        if zoom_target_path:
            filename = ntpath.basename(zoom_target_path)
            layout.label(text=filename)
            
        row = layout.row()
        row.operator("effect_composer.set_zoom_target", text="Set Target")

        layout.prop(self, "fadeDuration", text="Fade Duration")

        layout.operator("effect_composer.load_movie", text="OK")

        row = layout.row()
        row.template_list("EffectComposerUIList", "", context.scene, "effect_composer_items", context.scene, "active_effect_composer_index")
        col = row.column(align=True)
        col.operator("effect_composer.remove_item", icon='REMOVE', text="")

    @property
    def selected_files(self):
        return [(f, f, '') for f in [ntpath.basename(item.name) for item in bpy.context.scene.effect_composer_items]]
