from f4py.Eithrer import either
from f4py.Maybe import maybe
from f4py.Monad import Monad
from f4py.exception.CompositeException import CompositeException


class Try(Monad):
    def __init__(self):
        raise Exception('Direct usage of try monad!')

    def failed(self): return False

    def succeed(self): return False

    def as_either(self): return either((self._get_result(), self._get_error()))

    def get_error(self): return maybe(self._get_error())

    def get_result(self): return maybe(self._get_result())

    def map(self, mapper):
        if self.failed():
            return self
        return attempt(lambda: mapper(self._get_result()))

    def flat_map(self, mapper):
        if self.failed():
            return self
        return mapper(self._get_result())

    def fallback(self, tryable):
        if self.failed():
            return attempt(tryable)
        return self

    def flat_fallback(self, fallback):
        if self.failed():
            return fallback()
        return self

    def handle_error(self, handler):
        if self.failed():
            return attempt(lambda: handler(self._get_error()))
        return self

    def flat_handle_error(self, handler):
        if self.failed():
            return handler(self._get_error())
        return self

    def peek(self, mapper):
        if self.succeed():
            mapper(self._get_result())
        return self

    def on_success(self, action):
        if self.succeed():
            action(self._get_result())
        return self

    def on_success_try(self, action):
        if self.succeed():
            attempt(lambda: action(self._get_result()))
        return self

    def on_failure(self, action):
        if self.failed():
            action(self._get_error())
        return self

    def on_failure_try(self, action):
        if self.failed():
            result = attempt(lambda: action(self._get_error()))
            if result.failed():
                return failure(CompositeException(self._get_error(), result._get_error()))
        return self

    def or_else(self, result):
        if self.failed():
            return result
        return self._get_result()

    def or_throw(self):
        if self.failed():
            raise self._get_error()
        return self

    def unpack(self):
        if self.failed():
            return self._get_error()
        return self._get_result()

    @classmethod
    def of(cls, tryable):
        try:
            return success(tryable())
        except BaseException as e:
            return failure(e)

    def _get_error(self): return None

    def _get_result(self): return None


class _Success(Try):
    def __init__(self, value):
        self.value = value

    def succeed(self): return True

    def _get_result(self): return self.value

    def __str__(self):
        return 'Success ' + str(self.value)


class _Failure(Try):
    def __init__(self, e):
        self.e = e

    def failed(self): return True

    def _get_error(self): return self.e

    def __str__(self):
        return 'Failure ' + str(self.e)


def success(value):
    return _Success(value)


def failure(e):
    return _Failure(e)


def attempt(tryable):
    return Try.of(tryable)
