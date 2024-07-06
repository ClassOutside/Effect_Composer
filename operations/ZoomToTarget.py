import bpy

class EffectComposerSetZoomTargetOperator(bpy.types.Operator):
    bl_idname = "effect_composer.set_zoom_target"
    bl_label = "Set Target"

    def execute(self, context):
        selected_index = context.scene.active_effect_composer_index
        if selected_index >= 0 and selected_index < len(context.scene.effect_composer_items):
            selected_item = context.scene.effect_composer_items[selected_index]
            context.scene['ZoomTargetPath'] = selected_item.name
            context.scene['ZoomTargetFullPath'] = selected_item.name
        return {'FINISHED'}
