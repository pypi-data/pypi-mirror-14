class Monadic(object):
    product_arity = None

    def map(self, map_func):
        raise NotImplementedError

    def join(self):
        raise NotImplementedError

    def bind(self, bind_func):
        return self.map(bind_func).join()

    @classmethod
    def unit(cls, _):
        raise NotImplementedError

    @classmethod
    def zero(cls):
        raise NotImplementedError


class InnerValueNotContainerTypeException(Exception):
    pass


class NoSuchElementException(Exception):
    pass

