import unittest

from lru import LRUCache


class TestCustomList(unittest.TestCase):
    def test_limit_below_zero(self):
        with self.assertRaises(ValueError) as err:
            _ = LRUCache(0)
        self.assertEqual("limit must be above zero", str(err.exception))
        with self.assertRaises(ValueError) as err:
            _ = LRUCache(-1)
        self.assertEqual("limit must be above zero", str(err.exception))

    def test_correct_work1(self):
        cache = LRUCache(2)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")
        cache.set("k3", "val3")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertIsNone(cache.get("k2"))
        self.assertEqual(cache.get("k1"), "val1")

    def test_correct_work2(self):
        cache = LRUCache(3)
        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")
        cache.set("k4", "val4")
        cache.set("k5", "val5")
        cache.set("k6", "val6")
        self.assertIsNone(cache.get("k1"))
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k3"))
        self.assertEqual(cache.get("k6"), "val6")
        self.assertEqual(cache.get("k5"), "val5")
        self.assertEqual(cache.get("k4"), "val4")
        cache.set("k7", "val7")
        self.assertIsNone(cache.get("k6"))
        self.assertEqual(cache.get("k5"), "val5")
        self.assertEqual(cache.get("k7"), "val7")
        self.assertEqual(cache.get("k4"), "val4")
        cache.set("k1", "val0")
        self.assertIsNone(cache.get("k2"))
        self.assertIsNone(cache.get("k3"))
        self.assertIsNone(cache.get("k5"))
        self.assertIsNone(cache.get("k6"))
        self.assertEqual(cache.get("k1"), "val0")
        self.assertEqual(cache.get("k7"), "val7")
        self.assertEqual(cache.get("k4"), "val4")


if __name__ == '__main__':
    unittest.main()
