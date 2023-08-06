import importlib

def get_dotted_path(val):
    module, _, attr = val.rpartition('.')

    return getattr(importlib.import_module(module), attr)

def render(filename):
    # A default render method
    with open(filename) as f:
        return f.read()
