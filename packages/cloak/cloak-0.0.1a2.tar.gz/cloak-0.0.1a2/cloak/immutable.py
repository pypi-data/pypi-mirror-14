class ImmutableMeta(type):
    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj._locked = True
        return obj


def with_metaclass(mcls):
    def decorator(cls):
        body = vars(cls).copy()
        # clean out class body
        body.pop('__dict__', None)
        body.pop('__weakref__', None)
        return mcls(cls.__name__, cls.__bases__, body)
    return decorator


@with_metaclass(ImmutableMeta)
class Immutable(object):
    _locked = False

    def __setattr__(self, *args):
        if self._locked:
            raise TypeError("Instance is immutable!")
        object.__setattr__(self, *args)

    def __delattr__(self, *args):
        if self._locked:
            raise TypeError("Instance is immutable!")
        object.__delattr__(self, *args)

    def __setitem__(self, *args):
        if self._locked:
            raise TypeError("Instance is immutable!")
        object.__setitem__(self, *args)

    def __delitem__(self, *args):
        if self._locked:
            raise TypeError("Instance is immutable!")
        object.__delitem__(self, *args)
