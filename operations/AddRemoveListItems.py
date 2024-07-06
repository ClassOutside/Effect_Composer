import bpy
import os

class EffectComposerAddOperator(bpy.types.Operator):
    bl_idname = "effect_composer.add_item"
    bl_label = "Add Selected Items"

    def execute(self, context):
        space = context.space_data

        if isinstance(space, bpy.types.SpaceFileBrowser):
            directory = space.params.directory.decode('utf-8')
            files = bpy.context.selected_files

            for file in files:
                filename = file.name
                path = bpy.path.abspath(os.path.join(directory, filename))

                if not self.path_exists_in_list(context.scene.effect_composer_items, path):
                    item = context.scene.effect_composer_items.add()
                    item.name = path
        return {'FINISHED'}
    
    def path_exists_in_list(self, items_list, path):
        for item in items_list:
            if item.name == path:
                return True
        return False

class EffectComposerRemoveOperator(bpy.types.Operator):
    bl_idname = "effect_composer.remove_item"
    bl_label = "Remove an item"

    def execute(self, context):
        context.scene.effect_composer_items.remove(context.scene.active_effect_composer_index)
        return {'FINISHED'}
