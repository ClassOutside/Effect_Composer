import bpy

class EffectComposerPanel(bpy.types.Panel):
    bl_label = "Effect Composer"
    bl_idname = "FILE_PT_effect_composer"
    bl_space_type = 'FILE_BROWSER'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.template_list("EffectComposerUIList", "", context.scene, "effect_composer_items", context.scene, "active_effect_composer_index")

        col = row.column(align=True)
        col.operator("effect_composer.add_item", icon='ADD', text="")
        col.operator("effect_composer.remove_item", icon='REMOVE', text="")

        layout.prop(context.scene, "effect_composer_dropdown", text="Choose Effect")

        layout.operator("effect_composer.generate_effect", text="Generate Effect")
