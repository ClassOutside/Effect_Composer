import bpy

class EffectComposerGenerateEffectOperator(bpy.types.Operator):
    bl_idname = "effect_composer.generate_effect"
    bl_label = "Generate Effect"

    def execute(self, context):
        effect = context.scene.effect_composer_dropdown
        if effect == 'VIDEO_GRID':
            bpy.ops.wm.effect_composer_popup('INVOKE_DEFAULT')
        elif effect == 'CROSS_FADE':
            bpy.ops.wm.effect_composer_cross_fade_popup('INVOKE_DEFAULT')
        return {'FINISHED'}
