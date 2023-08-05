from unittest import TestCase

from f4py.Eithrer import left, right, Either


class TestEither(TestCase):
    def setUp(self):
        self.left_value = 'left'
        self.right_value = 'right'
        self.left = left(self.left_value)
        self.right = right(self.right_value)
        self.mapper = lambda x: x.upper()
        self.flat_left_mapper = lambda x: left(self.mapper(x))
        self.flat_right_mapper = lambda x: right(self.mapper(x))
        self.left_bimapper = lambda x: x + self.left_value
        self.right_bimapper = lambda x: x + self.right_value
        self.flat_left_bimapper_to_left = lambda x: left(self.left_bimapper(x))
        self.flat_left_bimapper_to_right = lambda x: right(self.left_bimapper(x))
        self.flat_right_bimapper_to_right = lambda x: right(self.right_bimapper(x))
        self.flat_right_bimapper_to_left = lambda x: left(self.right_bimapper(x))

    def test_is_left(self):
        self.assertTrue(self.left.is_left())
        self.assertFalse(self.right.is_left())

    def test_is_right(self):
        self.assertFalse(self.left.is_right())
        self.assertTrue(self.right.is_right())

    def test_map_left(self):
        result = self.left.map(self.mapper)
        self.assertLeft(result, self.mapper(self.left_value))

    def test_map_right(self):
        result = self.right.map(self.mapper)
        self.assertRight(result, self.mapper(self.right_value))

    def test_flat_map_left_to_left(self):
        result = self.left.flat_map(self.flat_left_mapper)
        self.assertLeft(result, self.mapper(self.left_value))

    def test_flat_map_left_to_right(self):
        result = self.left.flat_map(self.flat_right_mapper)
        self.assertRight(result, self.mapper(self.left_value))

    def test_flat_map_right_to_right(self):
        result = self.right.flat_map(self.flat_right_mapper)
        self.assertRight(result, self.mapper(self.right_value))

    def test_flat_map_right_to_left(self):
        result = self.right.flat_map(self.flat_left_mapper)
        self.assertLeft(result, self.mapper(self.right_value))

    def test_bimap_left(self):
        result = self.left.bimap(self.left_bimapper, self.right_bimapper)
        self.assertLeft(result, self.left_bimapper(self.left_value))

    def test_bimap_right(self):
        result = self.right.bimap(self.left_bimapper, self.right_bimapper)
        self.assertRight(result, self.right_bimapper(self.right_value))

    def test_flat_bimap_left_to_left(self):
        result = self.left.flat_bimap(self.flat_left_bimapper_to_left, self.flat_right_bimapper_to_right)
        self.assertLeft(result, self.left_bimapper(self.left_value))

    def test_flat_bimap_left_to_right(self):
        result = self.left.flat_bimap(self.flat_left_bimapper_to_right, self.flat_right_bimapper_to_right)
        self.assertRight(result, self.left_bimapper(self.left_value))

    def test_flat_bimap_right_to_right(self):
        result = self.right.flat_bimap(self.flat_left_bimapper_to_left, self.flat_right_bimapper_to_right)
        self.assertRight(result, self.right_bimapper(self.right_value))

    def test_flat_bimap_right_to_left(self):
        result = self.right.flat_bimap(self.flat_left_bimapper_to_left, self.flat_right_bimapper_to_left)
        self.assertLeft(result, self.right_bimapper(self.right_value))

    def test_flip_left(self):
        self.assertRight(self.left.flip(), self.left_value)

    def test_flip_right(self):
        self.assertLeft(self.right.flip(), self.right_value)

    def test_peek_left(self):
        saved = {}
        result = self.left.peek(lambda v: saved.setdefault('v', v))
        self.assertLeft(result, self.left_value)
        self.assertEqual(saved['v'], self.left_value)

    def test_peek_right(self):
        saved = {}
        result = self.right.peek(lambda v: saved.setdefault('v', v))
        self.assertRight(result, self.right_value)
        self.assertEqual(saved['v'], self.right_value)

    def test_of_left(self):
        pair = (self.left_value, None)
        self.assertLeft(Either.of(pair), self.left_value)

    def test_of_right(self):
        pair = (None, self.right_value)
        self.assertRight(Either.of(pair), self.right_value)

    def assertLeft(self, either, value):
        self.assertTrue(either.is_left())
        self.assertFalse(either.is_right())
        self.assertFalse(either.get_right().is_present())
        self.assertTrue(either.get_left().is_present())
        self.assertEqual(either.get_left().get(), either.unpack())
        self.assertEqual(either.get_left().get(), value)

    def assertRight(self, either, value):
        self.assertFalse(either.is_left())
        self.assertTrue(either.is_right())
        self.assertTrue(either.get_right().is_present())
        self.assertFalse(either.get_left().is_present())
        self.assertEqual(either.get_right().get(), either.unpack())
        self.assertEqual(either.get_right().get(), value)
