from unittest import TestCase

from f4py.Maybe import nothing, just, Maybe
from f4py.exception.NotPresentException import NotPresentException


class TestMaybe(TestCase):
    def setUp(self):
        self.empty = nothing()
        self.initial = 5
        self.filled = just(self.initial)
        self.mapper = lambda x: x + 1
        self.expected = 6
        self.emptifier = lambda x: None
        self.flat_mapper = lambda x: just(x + 1)
        self.flat_emptifier = lambda x: nothing()
        self.keep = lambda x: True
        self.omit = lambda x: False
        self.producer = lambda: self.expected
        self.none_producer = lambda: None
        self.flat_producer = lambda: just(self.expected)
        self.flat_none_producer = lambda: nothing()

    def test_is_present(self):
        self.assertTrue(self.filled.is_present())
        self.assertFalse(self.empty.is_present())

    def test_is_nothing(self):
        self.assertFalse(self.filled.is_nothing())
        self.assertTrue(self.empty.is_nothing())

    def test_map_empty(self):
        result = self.empty.map(self.mapper)
        self.assertNothing(result)

    def test_map_filled(self):
        result = self.filled.map(self.mapper)
        self.assertJust(result, self.expected)

    def test_map_filled_to_empty(self):
        result = self.filled.map(self.emptifier)
        self.assertNothing(result)

    def test_flat_map_empty(self):
        result = self.empty.flat_map(self.flat_mapper)
        self.assertNothing(result)

    def test_flat_map_filled(self):
        result = self.filled.flat_map(self.flat_mapper)
        self.assertJust(result, self.expected)

    def test_flat_map_filled_to_empty(self):
        result = self.filled.flat_map(self.flat_emptifier)
        self.assertNothing(result)

    def test_filter_empty(self):
        result = self.empty.filter(self.keep)
        self.assertNothing(result)

    def test_filter_filled(self):
        result = self.filled.filter(self.keep)
        self.assertJust(result, self.initial)

    def test_filter_filled_to_empty(self):
        result = self.filled.filter(self.omit)
        self.assertNothing(result)

    def test_or_else_filled(self):
        result = self.filled.or_else(6)
        self.assertEqual(result, self.initial)

    def test_or_else_empty(self):
        result = self.empty.or_else(self.expected)
        self.assertEqual(result, self.expected)

    def test_or_else_compute_filled(self):
        result = self.filled.or_else_compute(self.producer)
        self.assertEqual(result, self.initial)

    def test_or_else_compute_empty(self):
        result = self.empty.or_else_compute(self.producer)
        self.assertEqual(result, self.expected)

    def test_if_absent_filled(self):
        result = self.filled.if_absent(self.empty)
        self.assertJust(result, self.initial)

    def test_if_absent_empty_to_filled(self):
        result = self.empty.if_absent(self.filled)
        self.assertJust(result, self.initial)

    def test_if_absent_empty_to_empty(self):
        result = self.empty.if_absent(self.empty)
        self.assertNothing(result)

    def test_compute_if_absent_filled(self):
        result = self.filled.compute_if_absent(self.producer)
        self.assertJust(result, self.initial)

    def test_compute_if_absent_empty_to_filled(self):
        result = self.empty.compute_if_absent(self.producer)
        self.assertJust(result, self.expected)

    def test_compute_if_absent_empty_to_empty(self):
        result = self.empty.compute_if_absent(self.none_producer)
        self.assertNothing(result)

    def test_flat_compute_if_absent_filled(self):
        result = self.filled.flat_compute_if_absent(self.flat_producer)
        self.assertJust(result, self.initial)

    def test_flat_compute_if_absent_empty_to_filled(self):
        result = self.empty.flat_compute_if_absent(self.flat_producer)
        self.assertJust(result, self.expected)

    def test_flat_compute_if_absent_empty_to_empty(self):
        result = self.empty.flat_compute_if_absent(self.flat_none_producer)
        self.assertNothing(result)

    def test_get_filled(self):
        self.assertEqual(self.filled.get(), self.initial)

    def test_get_empty(self):
        with self.assertRaises(NotPresentException):
            self.empty.get()

    def test_peek_empty(self):
        store = {}
        result = self.empty.peek(lambda v: store.setdefault('v', v))
        self.assertNothing(result)
        self.assertIsNone(store.get('v'))

    def test_peel_filled(self):
        store = {}
        result = self.filled.peek(lambda v: store.setdefault('v', v))
        self.assertJust(result, self.initial)
        self.assertEqual(store['v'], self.initial)

    def test_of_none(self):
        self.assertNothing(Maybe.of(None))

    def test_of_value(self):
        self.assertJust(Maybe.of(self.expected), self.expected)

    def test_unpack(self):
        self.assertEqual(self.filled.unpack(), self.initial)
        self.assertIsNone(self.empty.unpack())

    def assertNothing(self, maybe):
        self.assertTrue(maybe.is_nothing())
        self.assertFalse(maybe.is_present())

    def assertJust(self, maybe, expected_value):
        self.assertFalse(maybe.is_nothing())
        self.assertTrue(maybe.is_present())
        self.assertEqual(maybe.get(), expected_value)
