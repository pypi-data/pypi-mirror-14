import pkgutil
import importlib

# __path__ = pkgutil.extend_path(__path__, __name__)
packages = pkgutil.walk_packages(path=__path__, prefix=__name__+'.')
for importer, modname, ispkg in packages:
    mod = importlib.import_module(modname)
    for name in dir(mod):
        if not name.startswith('__'):
            globals()[name] = getattr(mod, name)
    del importer, modname, ispkg, mod, name
del packages, pkgutil, importlib
