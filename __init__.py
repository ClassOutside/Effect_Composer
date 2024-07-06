from .module_loader import refresh
refresh()

bl_info = {
    "name": "Effect Composer",
    "blender": (4, 1, 1),
    "category": "Sequencer",
}


import bpy
from .operations.ZoomToTarget import *
from .interface.GridPopup import *
from .interface.CrossFadePopup import *
from .operations.GenerateEffect import *
from .operations.AddRemoveListItems import *
from .interface.EffectComposerPanel import *
from .interface.EffectComposerUIList import *
from .operations.GridDefs import *
from .operations.CrossFadeDefs import *
from .items.EffectComposerItem import *  

classes = [
    EffectComposerItem,  
    EffectComposerUIList,
    EffectComposerPanel,
    EffectComposerAddOperator,
    EffectComposerRemoveOperator,
    EffectComposerGenerateEffectOperator,
    EffectComposerPopupOperator,
    EffectComposerCrossFadePopupOperator,
    EffectComposerSetZoomTargetOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.effect_composer_items = bpy.props.CollectionProperty(type=EffectComposerItem)
    bpy.types.Scene.active_effect_composer_index = bpy.props.IntProperty()
    bpy.types.Scene.effect_composer_dropdown = bpy.props.EnumProperty(
        items=[
            ('NONE', 'None', ''),
            ('VIDEO_GRID', 'Video Grid', ''),
            ('CROSS_FADE', 'Cross Fade', ''),
        ]
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.effect_composer_items
    del bpy.types.Scene.active_effect_composer_index
    del bpy.types.Scene.effect_composer_dropdown
    del bpy.types.Scene['ZoomTargetPath']

if __name__ == "__main__":
    register()
