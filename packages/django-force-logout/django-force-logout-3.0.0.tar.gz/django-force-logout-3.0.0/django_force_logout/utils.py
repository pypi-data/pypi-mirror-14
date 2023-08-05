import importlib

from django.core.urlresolvers import get_mod_func

def from_dotted_path(fullpath):
    """
    Returns the specified attribute of a module, specified by a string.

    ``from_dotted_path('a.b.c.d')`` is roughly equivalent to::

        from a.b.c import d

    except that ``d`` is returned and not entered into the current namespace.
    """

    module_name, fn_name = get_mod_func(fullpath)

    return getattr(importlib.import_module(module_name), fn_name)
