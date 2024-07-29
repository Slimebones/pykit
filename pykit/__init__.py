import importlib.metadata as _import_meta

# We don't intend to export modules here since it would be cleaner due to
# different modules to have them all expose themselves.

__version__ = _import_meta.version("sb-pykit")
