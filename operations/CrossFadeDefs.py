import bpy

from ..operations.GridDefs import set_sequencer_head_to_frame_zero, getSequenceEditorArea, fillListToGridSize, set_clip_position, keyframe_transform_strips, swap_item_to_first_position, set_render_end_frame_to_first_channel_length

def load_strips_to_sequencer(self, context, fadeDuration):
    currentFrameEnd = 0
    sequenceEditorArea = getSequenceEditorArea()

    with bpy.context.temp_override(area=sequenceEditorArea):
        sequence_editor = context.scene.sequence_editor
        set_sequencer_head_to_frame_zero()
        bpy.ops.sequencer.select_all(action='SELECT')
        bpy.ops.sequencer.delete()

        zoom_target_full_path = context.scene.get('ZoomTargetFullPath', '')
        swap_item_to_first_position(context.scene, zoom_target_full_path)
        items = list(context.scene.effect_composer_items)

        frame_start = 0

        for i, item in enumerate(items):
            channel = i + 1
            path = item.name

            if path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                if currentFrameEnd != 0:
                    frame_start = currentFrameEnd - fadeDuration

                # Add the movie strip
                movie_sequence = sequence_editor.sequences.new_movie(
                    name=f"Movie_{i}",
                    filepath=path,
                    channel=channel,
                    frame_start=frame_start
                )
            
                currentFrameEnd = movie_sequence.frame_final_end

                # Ensure the strip is set correctly
                movie_sequence.frame_start = frame_start
                movie_sequence.frame_final_start = frame_start
                movie_sequence.frame_final_end = frame_start + movie_sequence.frame_duration

                currentFrameEnd = movie_sequence.frame_final_end

                # Force update the strip
                bpy.context.view_layer.update()

            else:
                self.report({'WARNING'}, f"Unsupported file format for {item.name}. Please select a valid movie file.")

        # Update scene frame range after all strips are added
        if items:
            context.scene.frame_start = 0
            context.scene.frame_end = currentFrameEnd

        # Force update the view layer at the end
        bpy.context.view_layer.update()


def add_gamma_cross_transitions(scene):
    sequences = scene.sequence_editor.sequences_all
    num_sequences = len(sequences)
    
    # Ensure sequences are sorted by their start frame
    sorted_sequences = sorted(sequences, key=lambda seq: seq.frame_final_start)
    
    # Get the area that is a sequencer
    sequence_editor_area = None
    for area in bpy.context.screen.areas:
        if area.type == 'SEQUENCE_EDITOR':
            sequence_editor_area = area
            break
    
    if not sequence_editor_area:
        raise RuntimeError("No sequence editor area found")
    
    for i in range(num_sequences - 1):
        strip1 = sorted_sequences[i]
        strip2 = sorted_sequences[i + 1]
        
        # Select the two strips
        bpy.ops.sequencer.select_all(action='DESELECT')
        strip1.select = True
        strip2.select = True
        
        # Set the active strip to the second strip
        scene.sequence_editor.active_strip = strip2
        
        # Override context
        with bpy.context.temp_override(area=sequence_editor_area):
            # Add a Gamma Cross transition
            bpy.ops.sequencer.effect_strip_add(type='GAMMA_CROSS')

def set_sequence_end_frame_to_max(scene):
    sequences = scene.sequence_editor.sequences_all
    
    if not sequences:
        return
    
    # Find the maximum end frame of all sequences
    max_end_frame = max(seq.frame_final_end for seq in sequences)
    
    bpy.context.scene.frame_end = max_end_frame

    print("MAX END FRAME", max_end_frame)

