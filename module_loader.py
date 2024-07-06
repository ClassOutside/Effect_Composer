import importlib
import os

def reload_modules(module_names):
    for name in module_names:
        if name in globals():
            importlib.reload(globals()[name])
        else:
            globals()[name] = importlib.import_module(name)

def get_module_names():
    directory = os.path.dirname(os.path.realpath(__file__))
    module_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and file != os.path.basename(__file__):
                module_name = os.path.splitext(file)[0]
                module_path = os.path.join(root, module_name).replace(directory+os.sep, '').replace(os.sep, '.')
                module_names.append(__name__.split('.')[0] + '.' + module_path)
    return module_names

def refresh():
    importFiles = get_module_names()
    reload_modules(importFiles)

