from unittest import TestCase

from f4py.Try import failure, success, attempt


class TestTry(TestCase):
    class _FirstError(Exception):
        pass

    class _NextError(Exception):
        pass

    def setUp(self):
        self.error = self._FirstError()
        self.error_in_mapper = self._NextError()
        self.failure = failure(self.error)
        self.value = 'success'
        self.fallback_value = 'fallback'
        self.success = success(self.value)
        self.mapper = lambda x: x + self.value
        self.fallback = lambda: self.fallback_value
        self.flat_mapper = lambda x: success(self.mapper(x))
        self.flat_fallback = lambda: success(self.fallback_value)
        self.fail_flat_fallback = lambda: failure(self.error_in_mapper)
        self.handler = lambda e:\
            self.closure(self.check_error(e), self.fallback())
        self.fail_handler = lambda e:\
            self.closure(self.check_error(e), self.fail_fallback())
        self.flat_handler = lambda e:\
            self.closure(self.check_error(e), self.flat_fallback())
        self.flat_fail_handler = lambda e:\
            self.closure(self.check_error(e), self.fail_flat_fallback())

    def closure(self, *args):
        """
        Hack to create multi-statement lambda...
        """
        return args[-1]

    def check_error(self, e):
        self.assertEqual(e, self.error)

    def fail_mapper(self, x):
        raise self.error_in_mapper

    def fail_fallback(self):
        raise self.error_in_mapper

    def get_fail_flat_mapper(self):
        return lambda x: attempt(lambda: self.fail_mapper(x))

    def test_succeed(self):
        self.assertTrue(self.success.succeed())
        self.assertFalse(self.failure.succeed())

    def test_failure(self):
        self.assertFalse(self.success.failed())
        self.assertTrue(self.failure.failed())

    def test_map_success(self):
        result = self.success.map(self.mapper)
        self.assertSuccess(result, self.mapper(self.value))

    def test_map_failure(self):
        result = self.failure.map(self.mapper)
        self.assertFailure(result, self.error)

    def test_map_success_to_failure(self):
        result = self.success.map(self.fail_mapper)
        self.assertFailure(result, self.error_in_mapper)

    def test_flat_map_success_to_success(self):
        result = self.success.flat_map(self.flat_mapper)
        self.assertSuccess(result, self.mapper(self.value))

    def test_flat_map_success_to_failure(self):
        result = self.success.flat_map(self.get_fail_flat_mapper())
        self.assertFailure(result, self.error_in_mapper)

    def test_flat_map_failure(self):
        result = self.failure.flat_map(self.flat_mapper)
        self.assertFailure(result, self.error)

    def test_fallback_success(self):
        result = self.success.fallback(self.fallback)
        self.assertSuccess(result, self.value)

    def test_fallback_failure_to_success(self):
        result = self.failure.fallback(self.fallback)
        self.assertSuccess(result, self.fallback_value)

    def test_fallback_failure_to_failure(self):
        result = self.failure.fallback(self.fail_fallback)
        self.assertFailure(result, self.error_in_mapper)

    def test_flat_fallback_success(self):
        result = self.success.flat_fallback(self.flat_fallback)
        self.assertSuccess(result, self.value)

    def test_flat_fallback_failure_to_success(self):
        result = self.failure.flat_fallback(self.flat_fallback)
        self.assertSuccess(result, self.fallback_value)

    def test_flat_fallback_failure_to_failure(self):
        result = self.failure.flat_fallback(self.fail_flat_fallback)
        self.assertFailure(result, self.error_in_mapper)

    def test_handle_error_success(self):
        result = self.success.handle_error(self.handler)
        self.assertSuccess(result, self.value)

    def test_handle_error_failure_to_success(self):
        result = self.failure.handle_error(self.handler)
        self.assertSuccess(result, self.fallback_value)

    def test_handle_error_failure_to_failure(self):
        result = self.failure.handle_error(self.fail_handler)
        self.assertFailure(result, self.error_in_mapper)

    def test_flat_handle_error_success(self):
        result = self.success.flat_handle_error(self.flat_handler)
        self.assertSuccess(result, self.value)

    def test_flat_handle_error_failure_to_success(self):
        result = self.failure.flat_handle_error(self.flat_handler)
        self.assertSuccess(result, self.fallback_value)

    def test_flat_handle_error_failure_to_failure(self):
        result = self.failure.flat_handle_error(self.flat_fail_handler)
        self.assertFailure(result, self.error_in_mapper)

    def test_or_else_success(self):
        result = self.success.or_else(self.fallback_value)
        self.assertEqual(result, self.value)

    def test_or_else_failure(self):
        result = self.failure.or_else(self.fallback_value)
        self.assertEqual(result, self.fallback_value)

    def test_or_throw_success(self):
        result = self.success.or_throw()
        self.assertSuccess(result, self.value)

    def test_or_throw_failure(self):
        with self.assertRaises(self._FirstError):
            self.failure.or_throw()

    def assertFailure(self, attempt, error):
        """
        :param f4py.Try.Try attempt:
        :param error:
        :return:
        """
        self.assertTrue(attempt.failed())
        self.assertFalse(attempt.succeed())
        self.assertTrue(attempt.get_error().is_present())
        self.assertFalse(attempt.get_result().is_present())
        self.assertEqual(attempt.get_error().get(), attempt.unpack())
        self.assertEqual(attempt.get_error().get(), error)

    def assertSuccess(self, attempt, value):
        """
        :param f4py.Try.Try attempt:
        :param value:
        :return:
        """
        self.assertFalse(attempt.failed())
        self.assertTrue(attempt.succeed())
        self.assertFalse(attempt.get_error().is_present())
        # not checking for result to be present, cause result can be None
        self.assertEqual(attempt.get_result().unpack(), attempt.unpack())
        self.assertEqual(attempt.get_result().unpack(), value)
