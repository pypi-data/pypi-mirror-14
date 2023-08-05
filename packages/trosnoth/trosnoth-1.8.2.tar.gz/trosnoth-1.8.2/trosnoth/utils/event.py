import inspect
import logging
import types
import weakref

log = logging.getLogger(__name__)


class Event(object):
    def __init__(self, listener=None):
        self.listeners = {}
        if listener is not None:
            self.addListener(listener)

    def addListener(self, obj):
        assert callable(obj)
        if isinstance(obj, types.MethodType):
            if getattr(obj.im_self, obj.im_func.__name__, None) == obj:
                obj = WeakMethod(self, obj)
            else:
                log.warning(
                    'Cannot create weak reference for %s.%s()',
                    obj.im_self, obj.im_func.__name__)
        self.listeners[obj] = obj

    def removeListener(self, obj):
        try:
            value = self.listeners.pop(obj)
        except KeyError:
            return
        if WeakMethod is None:
            # Final garbage collection during process termination
            return
        if isinstance(value, WeakMethod):
            value.done()

    def clear(self):
        self.listeners.clear()

    def execute(self, *args, **kwargs):
        for call in list(self.listeners):
            try:
                call(*args, **kwargs)
            except Exception:
                caller = inspect.currentframe().f_back
                log.exception(
                    'Error in event callback (from %s:%s)',
                    caller.f_code.co_filename, caller.f_lineno)

    __call__ = execute


class WeakMethod(object):
    def __init__(self, event, method):
        self.event = event
        self.obj = weakref.ref(method.im_self, self.collect)
        self.attr = method.im_func.__name__
        self._hash = hash(method)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        if other is self:
            return True
        if not isinstance(other, (types.MethodType, WeakMethod)):
            return False
        return other == self.get_method()

    def get_method(self):
        if self.obj is None:
            return None
        obj = self.obj()
        if obj is None:
            return None
        return getattr(obj, self.attr)

    def __call__(self, *args, **kwargs):
        method = self.get_method()
        if method:
            method(*args, **kwargs)

    def collect(self, r):
        if self.obj is None:
            # This is possible if garbage collection has been delayed
            return
        self.event.removeListener(self)

    def done(self):
        # Lose the reference to the weak reference so that it can be garbage
        # collected and so that it doesn't keep a circular reference to
        # self.collect.
        self.obj = None
