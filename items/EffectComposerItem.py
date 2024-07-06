import bpy

class EffectComposerItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name", description="File path", default="")
