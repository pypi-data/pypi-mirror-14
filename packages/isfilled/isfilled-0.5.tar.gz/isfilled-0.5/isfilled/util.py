import os, importlib

def import_string(dotted_path):
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except (ValueError, AttributeError) as e:
        module_path = dotted_path
    try:
        return importlib.import_module(dotted_path)
    except ImportError, e:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
