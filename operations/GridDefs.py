import bpy
import os

index_offset_x_modifier = 0
index_offset_y_modifier = 0
keyframe_offset_x_modifier = 0
keyframe_offset_y_modifier = 0

def getSequenceEditorArea():
    if bpy.context.area.type != 'SEQUENCE_EDITOR':
        for area in bpy.context.screen.areas:
            if area.type == 'SEQUENCE_EDITOR':
                return area
    return bpy.context.area

def set_sequencer_head_to_frame_zero():
    if bpy.context.area.type == 'SEQUENCE_EDITOR':
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_current = 0
    else:
        print("Please switch to the Video Sequence Editor.")

def swap_item_to_first_position(scene, path):
    items = scene.effect_composer_items
    for i, item in enumerate(items):
        if item.name == path:
            items.move(i, 0)
            break

def set_render_end_frame_to_first_channel_length():
    sequences = bpy.context.scene.sequence_editor.sequences
    first_channel_strip = sequences[0]
    bpy.context.scene.frame_end = first_channel_strip.frame_final_end

def set_clip_position(strip, grid_size):
    global index_offset_x_modifier
    global index_offset_y_modifier
    
    scene = bpy.context.scene
    
    # Iterate through all sequences in the sequence editor
    for strip in scene.sequence_editor.sequences_all:
        if strip.type == 'TRANSFORM':
            
            channel_number = strip.channel
            channel_number = channel_number / 2 - 1
    
            render = scene.render
            canvas_width = render.resolution_x
            canvas_height = render.resolution_y

            # Get top left value
            topLeft_width = (canvas_width / 2) / canvas_width * 100
            topLeft_height = (canvas_height / 2) / canvas_height * 100
            
            # Get offset value
            base_offset = ( 100 / grid_size ) / 2 
            
            # Update grid index offsets
            if (channel_number != 0) and (channel_number % grid_size == 0):
                index_offset_x_modifier = 0
            elif channel_number == 0:
                index_offset_x_modifier = 0
            else:
                index_offset_x_modifier += 2

            # Update grid index offsets
            if (channel_number != 0) and (channel_number % grid_size == 0):
                index_offset_y_modifier += 2
            elif channel_number == 0:
                index_offset_y_modifier = 0


            index_offset_x = base_offset + (index_offset_x_modifier * base_offset)
            index_offset_y = base_offset + (index_offset_y_modifier * base_offset)
            
            # Calculate the new position to clamp top-left corner of the strip to the top-left corner of the canvas
            strip.translate_start_x = - topLeft_width + index_offset_x
            strip.translate_start_y = topLeft_height - index_offset_y
    
    bpy.context.view_layer.update()

def keyframe_transform_strips(grid_size, startZoom, endZoom):
    # Get the current scene
    scene = bpy.context.scene
    global keyframe_offset_x_modifier
    global keyframe_offset_y_modifier

    print("Editor Sequence")
    
    # Iterate through all sequences in the sequence editor
    for strip in scene.sequence_editor.sequences_all:
        
        if strip.type == 'TRANSFORM':
            # Store initial position
            
            channel_number = strip.channel
            channel_number = channel_number / 2 - 1
            
            initial_translate_x = strip.translate_start_x
            initial_translate_y = strip.translate_start_y
            
            # Set keyframe at frame with current position
            strip.translate_start_x = initial_translate_x
            strip.translate_start_y = initial_translate_y
            strip.keyframe_insert(data_path='translate_start_x', frame=0)
            strip.keyframe_insert(data_path='translate_start_y', frame=0)
            strip.keyframe_insert(data_path='translate_start_x', frame=startZoom)
            strip.keyframe_insert(data_path='translate_start_y', frame=startZoom)
            
             # Store initial scale
            initial_scale_x = strip.scale_start_x
            initial_scale_y = strip.scale_start_y
            
            # Set keyframe at frame with current scale
            strip.scale_start_x = initial_scale_x
            strip.scale_start_y = initial_scale_y
            strip.keyframe_insert(data_path='scale_start_x', frame=0)
            strip.keyframe_insert(data_path='scale_start_y', frame=0)
            strip.keyframe_insert(data_path='scale_start_x', frame=startZoom)
            strip.keyframe_insert(data_path='scale_start_y', frame=startZoom)
            
            # Get offset value
            base_offset = ( 100 / grid_size ) / 2 
            
            # Update grid index offsets
            if (channel_number != 0) and (channel_number % grid_size == 0):
                keyframe_offset_x_modifier = 0
            elif channel_number == 0:
                keyframe_offset_x_modifier = 0
            else:
                keyframe_offset_x_modifier += grid_size * 2
                
            # Update grid index offsets
            if (channel_number != 0) and (channel_number % grid_size == 0):
                keyframe_offset_y_modifier += grid_size * 2
            elif channel_number == 0:
                keyframe_offset_y_modifier = 0
            
            # Calculate scaled position for frame 45 (modify as per your requirements)
            scaled_translate_x = base_offset * keyframe_offset_x_modifier
            scaled_translate_y = 1 - base_offset * keyframe_offset_y_modifier
            
            # Set keyframe at frame 45 with scaled position
            strip.translate_start_x = scaled_translate_x
            strip.translate_start_y = scaled_translate_y
            strip.keyframe_insert(data_path='translate_start_x', frame=endZoom)
            strip.keyframe_insert(data_path='translate_start_y', frame=endZoom)
            
            # Calculate scaled scale for frame 45 (modify as per your requirements)
            scaled_scale_x = initial_scale_x * grid_size
            scaled_scale_y = initial_scale_y * grid_size
            
            # Set keyframe at frame 45 with scaled scale
            strip.scale_start_x = scaled_scale_x
            strip.scale_start_y = scaled_scale_y
            strip.keyframe_insert(data_path='scale_start_x', frame=endZoom)
            strip.keyframe_insert(data_path='scale_start_y', frame=endZoom)

def keyframe_transform_grid(grid_size, strip, startZoom, endZoom):
    frame_start = strip.frame_final_start
    frame_end = strip.frame_final_end

    frame_range = frame_end - frame_start

    keyframe_offset_x_modifier = (strip.channel - 1) % grid_size
    keyframe_offset_y_modifier = (strip.channel - 1) // grid_size

    strip.keyframe_insert(data_path="scale_start_x", frame=frame_start)
    strip.scale_start_x = 1.0 / grid_size
    strip.keyframe_insert(data_path="scale_start_x", frame=frame_start)

    strip.keyframe_insert(data_path="scale_start_y", frame=frame_start)
    strip.scale_start_y = 1.0 / grid_size
    strip.keyframe_insert(data_path="scale_start_y", frame=frame_start)

    strip.keyframe_insert(data_path="translate_start_x", frame=frame_start)
    strip.translate_start_x = keyframe_offset_x_modifier
    strip.keyframe_insert(data_path="translate_start_x", frame=frame_start)

    strip.keyframe_insert(data_path="translate_start_y", frame=frame_start)
    strip.translate_start_y = keyframe_offset_y_modifier
    strip.keyframe_insert(data_path="translate_start_y", frame=frame_start)

    keyframe_index_offset_x_modifier = (strip.channel - 1) % grid_size
    keyframe_index_offset_y_modifier = (strip.channel - 1) // grid_size

    strip.scale_start_x = 1.0
    strip.keyframe_insert(data_path="scale_start_x", frame=frame_start + frame_range)

    strip.scale_start_y = 1.0
    strip.keyframe_insert(data_path="scale_start_y", frame=frame_start + frame_range)

    strip.translate_start_x = keyframe_index_offset_x_modifier
    strip.keyframe_insert(data_path="translate_start_x", frame=frame_start + frame_range)

    strip.translate_start_y = keyframe_index_offset_y_modifier
    strip.keyframe_insert(data_path="translate_start_y", frame=frame_start + frame_range)

def fillListToGridSize(list, grid_size):
    grid_count = grid_size * grid_size

    if len(list) < grid_count:
        needed_items = grid_count - len(list)
        
        for i in range(needed_items):
            list.append(list[i % len(list)])
            
    return list