from __future__ import absolute_import

try:
    import gobject
    idle_add = gobject.idle_add
except (ImportError, AttributeError):
    try:
        from gi.repository import GLib
        idle_add = GLib.idle_add
    except ImportError:
        pass

from zaguan.constants import WEBKIT


def get_implementation():
    try:
        import webkit
        have_webkit = True
    except:
        have_webkit = False

    if have_webkit:
        implementation = WEBKIT
    else:
        raise Exception('Failed to import webkit module')
    return implementation


def asynchronous_gtk_message(fun):
    def worker(xxx_todo_changeme):
        (function, args, kwargs) = xxx_todo_changeme
        function(*args, **kwargs)

    def fun2(*args, **kwargs):
        idle_add(worker, (fun, args, kwargs))

    return fun2
