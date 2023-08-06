from functools import wraps
from immutable import Immutable
import sys


from cloak.monadic import Monadic, InnerValueNotContainerTypeException, NoSuchElementException


IS_PY2 = sys.version_info[0] == 2


def _reverse_func_arity_two(func):
    return wraps(func)(lambda x, y: func(y, x))


class Option(Monadic, Immutable):
    product_arity = 1

    @classmethod
    def unit(cls, value):
        return Some(value)

    @classmethod
    def zero(cls):
        return nil

    @property
    def is_empty(self):
        raise NotImplementedError

    @property
    def is_defined(self):
        return not self.is_empty

    def get(self):
        raise NotImplementedError

    def get_or_else(self, else_value):
        raise NotImplementedError

    def or_else(self, alternative_callable):
        raise NotImplementedError

    def exists(self, praedicate_callable):
        raise NotImplementedError

    def filter(self, filter_callable):
        raise NotImplementedError


class Some(Option):
    def __init__(self, value):
        self._value = value
        super(Option, self).__init__()

    def __repr__(self):
        return "Some({0})".format(repr(self._value))

    def __str__(self):
        return "Some({0})".format(repr(self._value))

    def __eq__(self, other):
        return isinstance(other, Some) and self._value == other.get()

    def map(self, map_func):
        return self.__class__(map_func(self._value))

    def flatten(self):
        if not isinstance(self._value, Option):
            raise InnerValueNotContainerTypeException("Can't flatten if inner type is not an Option[T] type!")
        return self._value

    @property
    def is_empty(self):
        return False

    def get(self):
        return self._value

    def join(self):
        return self._value

    def get_or_else(self, _):
        return self._value

    def or_else(self, alternative_callable):
        return self

    def exists(self, praedicate_callable):
        return bool(praedicate_callable(self._value))

    def filter(self, filter_callable):
        return self if filter_callable(self._value) else nil

    def for_each(self, apply_callable):
        apply_callable(self._value)


class Nothing(Option):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Nothing, cls).__new__(cls, *args)
        return cls._instance

    def __init__(self, _):
        super(Option, self).__init__()

    def __repr__(self):
        return "nil"

    def __str__(self):
        return "nil"

    def map(self, _):
        return self._instance

    def flatten(self):
        return self._instance

    @property
    def is_empty(self):
        return True

    def get(self):
        raise NoSuchElementException

    def join(self):
        return nil

    def get_or_else(self, else_value):
        return else_value

    def or_else(self, alternative_callable):
        return alternative_callable()

    def exists(self, _):
        return False

    def filter(self, _):
        return nil

    def for_each(self, _):
        pass

nil = Nothing(None)


def lift_option_functor(function):
    def extract_argument_values(args):
        return (arg.get() if isinstance(arg, Some) else arg for arg in args)

    def extract_keyword_args(kwargs):
        if IS_PY2:
            return {key: value.get() if isinstance(value, Some) else value for key, value in kwargs.iteritems()}
        else:
            return {key: value.get() if isinstance(value, Some) else value for key, value in kwargs.items()}

    @wraps(function)
    def wrapped(*args, **kwargs):
        if IS_PY2:
            if nil in args or nil in kwargs.itervalues():
                return nil
            else:
                return Some(function(*extract_argument_values(args), **extract_keyword_args(kwargs)))
        else:
            if nil in args or nil in kwargs.values():
                return nil
            else:
                return Some(function(*extract_argument_values(args), **extract_keyword_args(kwargs)))
    return wrapped


def lift_exception_to_option_functor(function, target_exceptions):
    target_exceptions = tuple(target_exceptions)

    @wraps(function)
    def wrapped(*args, **kwargs):
        try:
            return Some(function(*args, **kwargs))
        except target_exceptions as _:
            return nil
    return wrapped
