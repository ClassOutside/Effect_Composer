import bpy
import ntpath
from ..operations.GridDefs import set_sequencer_head_to_frame_zero, getSequenceEditorArea, fillListToGridSize, set_clip_position, keyframe_transform_strips, swap_item_to_first_position, set_render_end_frame_to_first_channel_length

class EffectComposerPopupOperator(bpy.types.Operator):
    bl_idname = "wm.effect_composer_popup"
    bl_label = "Video Grid Popup"
    
    grid_sizes = [
        ('2x2', '2x2', '2x2'),
        ('3x3', '3x3', '3x3'),
        ('4x4', '4x4', '4x4'),
        ('5x5', '5x5', '5x5'),
        ('6x6', '6x6', '6x6'),
        ('7x7', '7x7', '7x7'),
        ('8x8', '8x8', '8x8'),
    ]

    grid_size: bpy.props.EnumProperty(items=grid_sizes, name="Grid Size")
    startZoom: bpy.props.IntProperty (name="Start Zoom", default=30)
    endZoom: bpy.props.IntProperty (name="End Zoom", default=180)

    def execute(self, context):
        if context.scene.effect_composer_items:
            self.load_movie_to_sequencer(context, context.scene.effect_composer_items)
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

        layout.prop(self, "grid_size", text="Grid Size")
        layout.prop(self, "startZoom", text="Start Zoom")
        layout.prop(self, "endZoom", text="End Zoom")

        layout.operator("effect_composer.load_movie", text="OK")

        row = layout.row()
        row.template_list("EffectComposerUIList", "", context.scene, "effect_composer_items", context.scene, "active_effect_composer_index")
        col = row.column(align=True)
        col.operator("effect_composer.remove_item", icon='REMOVE', text="")

    @property
    def selected_files(self):
        return [(f, f, '') for f in [ntpath.basename(item.name) for item in bpy.context.scene.effect_composer_items]]

    def load_movie_to_sequencer(self, context, path_list):
        grid_size = int(self.grid_size[0])
        sequenceEditorArea = getSequenceEditorArea()

        with bpy.context.temp_override(area=sequenceEditorArea):
            set_sequencer_head_to_frame_zero()
            bpy.ops.sequencer.select_all(action='SELECT')
            bpy.ops.sequencer.delete()

            zoom_target_full_path = context.scene.get('ZoomTargetFullPath', '')
            swap_item_to_first_position(context.scene, zoom_target_full_path)
            items = fillListToGridSize(list(context.scene.effect_composer_items), grid_size)

            for i, item in enumerate(items):
                frame_start = 0
                channel = i + 1
                path = item.name

                if path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                    bpy.ops.sequencer.movie_strip_add(filepath=path, frame_start=frame_start, channel=channel, sound=False)
                    strip = bpy.context.scene.sequence_editor.active_strip
                    bpy.ops.sequencer.effect_strip_add(type='TRANSFORM')
                    transform_strip = bpy.context.scene.sequence_editor.active_strip
                    transform_strip.scale_start_x = transform_strip.scale_start_x / grid_size
                    transform_strip.scale_start_y = transform_strip.scale_start_y / grid_size
                    set_clip_position(transform_strip, grid_size)
                else:
                    self.report({'WARNING'}, f"Unsupported file format for {item.name}. Please select a valid movie file.")

        keyframe_transform_strips(grid_size, self.startZoom, self.endZoom)
        set_render_end_frame_to_first_channel_length()

