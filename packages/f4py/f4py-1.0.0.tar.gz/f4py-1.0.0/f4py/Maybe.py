from f4py.Monad import Monad
from f4py.exception.NotPresentException import NotPresentException


class Maybe(Monad):
    def __init__(self):
        raise Exception('Direct usage of maybe monad!')

    def is_present(self): return False

    def is_nothing(self): return False

    def map(self, mapper):
        if self.is_nothing():
            return self
        result = mapper(self._get())
        return Maybe.of(result)

    def flat_map(self, mapper):
        if self.is_nothing():
            return self
        return mapper(self._get())

    def filter(self, tester):
        if self.is_nothing() or tester(self._get()):
            return self
        return _Nothing()

    def or_else(self, value):
        if self.is_nothing():
            return value
        return self._get()

    def or_else_compute(self, producer):
        if self.is_nothing():
            return producer()
        return self._get()

    def if_absent(self, maybe):
        if self.is_nothing():
            return maybe
        return self

    def compute_if_absent(self, producer):
        if self.is_nothing():
            return Maybe.of(producer())
        return self

    def flat_compute_if_absent(self, producer):
        if self.is_nothing():
            return producer()
        return self

    def get(self):
        if self.is_present():
            return self._get()
        raise NotPresentException

    def unpack(self): return self._get()

    def _get(self): return None

    @classmethod
    def of(cls, value):
        if value is None:
            return _Nothing()
        return _Just(value)


class _Nothing(Maybe):
    def __init__(self): pass

    def is_nothing(self): return True

    def __str__(self):
        return 'Nothing'


class _Just(Maybe):
    def __init__(self, value):
        self.value = value

    def is_present(self): return True

    def _get(self): return self.value

    def __str__(self):
        return 'Just ' + str(self.value)


def nothing(): return _Nothing()


def just(value): return _Just(value)


def maybe(value): return Maybe.of(value)
