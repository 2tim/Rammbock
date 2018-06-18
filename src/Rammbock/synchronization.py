import threading

from .decorator import decorator
import collections


LOCK = threading.RLock()


@decorator
def synchronized(f, *args, **kw):
    """ Synchronization decorator """
    with LOCK:
        return f(*args, **kw)


class SynchronizedType(type):

    def __new__(cls, clsname, bases, local):
        for name, item in list(local.items()):
            if isinstance(item, collections.Callable) and not name.startswith("_"):
                local[name] = synchronized(item)
        return type.__new__(cls, clsname, bases, local)
