import unittest

from custom_class import CustomList


class TestCustomList(unittest.TestCase):
    def test_sum_two_obj(self):
        lst1 = [5, 1, 3, 7]
        lst2 = [1, 2, 7]
        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 + obj2

        self.assertEqual(res, [6, 3, 10, 7])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [5, 1, 3, 7])
        self.assertEqual(obj2, [1, 2, 7])
        self.assertEqual(res.__str__(),
                         'Элементы: [6, 3, 10, 7], sum = 26')

    def test_sum_obj_and_list(self):
        lst1 = [1]
        lst2 = [2, 5]

        obj = CustomList(lst1)
        res = obj + lst2

        self.assertEqual(res, [3, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [1])
        self.assertEqual(lst2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [3, 5], sum = 8')

    def test_sum_list_and_obj(self):
        lst1 = [1]
        lst2 = [2, 5]

        obj = CustomList(lst1)
        res = lst2 + obj

        self.assertEqual(res, [3, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [1])
        self.assertEqual(lst2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [3, 5], sum = 8')

    def test_sum_obj_len0(self):
        lst1 = []
        lst2 = [2, 5]

        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 + obj2

        self.assertEqual(res, [2, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [])
        self.assertEqual(obj2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [2, 5], sum = 7')

    def test_sum_objs_len0(self):
        lst1 = []
        lst2 = []

        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 + obj2

        self.assertEqual(res, [])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [])
        self.assertEqual(obj2, [])
        self.assertEqual(res.__str__(),
                         'Элементы: [], sum = 0')

    def test_sum_lst_len0(self):
        lst1 = [2, 5]
        lst2 = []

        obj = CustomList(lst1)

        res = obj + lst2

        self.assertEqual(res, [2, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [2, 5])
        self.assertEqual(lst2, [])
        self.assertEqual(res.__str__(),
                         'Элементы: [2, 5], sum = 7')

    def test_sum_exception(self):
        lst1 = [2, 5]
        lst2 = 5

        obj = CustomList(lst1)

        with self.assertRaises(TypeError) as err:
            _ = obj + lst2

        self.assertEqual("Неподходящий тип", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
        self.assertEqual(obj, [2, 5])

    def test_sub_exception(self):
        lst1 = [2, 5]
        lst2 = 5

        obj = CustomList(lst1)

        with self.assertRaises(TypeError) as err:
            _ = obj - lst2

        self.assertEqual("Неподходящий тип", str(err.exception))
        self.assertEqual(TypeError, type(err.exception))
        self.assertEqual(obj, [2, 5])

    def test_sub_two_obj(self):
        lst1 = [5, 1, 3, 7]
        lst2 = [1, 2, 7]

        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 - obj2

        self.assertEqual(res, [4, -1, -4, 7])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [5, 1, 3, 7])
        self.assertEqual(obj2, [1, 2, 7])
        self.assertEqual(res.__str__(),
                         'Элементы: [4, -1, -4, 7], sum = 6')

    def test_sub_obj_and_list(self):
        lst1 = [1]
        lst2 = [2, 5]

        obj = CustomList(lst1)
        res = obj - lst2

        self.assertEqual(res, [-1, -5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [1])
        self.assertEqual(lst2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [-1, -5], sum = -6')

    def test_sub_list_and_obj(self):
        lst1 = [1]
        lst2 = [2, 5]

        obj = CustomList(lst1)
        res = lst2 - obj

        self.assertEqual(res, [1, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [1])
        self.assertEqual(lst2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [1, 5], sum = 6')

    def test_sub_obj_len0(self):
        lst1 = []
        lst2 = [2, 5]

        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 - obj2

        self.assertEqual(res, [-2, -5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [])
        self.assertEqual(obj2, [2, 5])
        self.assertEqual(res.__str__(),
                         'Элементы: [-2, -5], sum = -7')

    def test_sub_objs_len0(self):
        lst1 = []
        lst2 = []

        obj1 = CustomList(lst1)
        obj2 = CustomList(lst2)

        res = obj1 - obj2

        self.assertEqual(res, [])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj1, [])
        self.assertEqual(obj2, [])
        self.assertEqual(res.__str__(),
                         'Элементы: [], sum = 0')

    def test_sub_lst_len0(self):
        lst1 = [2, 5]
        lst2 = []

        obj = CustomList(lst1)

        res = obj - lst2

        self.assertEqual(res, [2, 5])
        self.assertTrue(isinstance(res, CustomList))
        self.assertEqual(obj, [2, 5])
        self.assertEqual(lst2, [])
        self.assertEqual(res.__str__(),
                         'Элементы: [2, 5], sum = 7')

    def test_eq(self):
        self.assertTrue(CustomList([1, 1, 1]) == CustomList([3]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) == CustomList([2, 3]))
        self.assertTrue(CustomList([]) == CustomList([]))
        self.assertTrue(CustomList([]) == CustomList([0]))
        self.assertTrue(CustomList([10]) == CustomList([10]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1]) == CustomList([2, 4]))

    def test_ne(self):
        self.assertTrue(CustomList([1, 1, 1]) != CustomList([4]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) != CustomList([2, 4]))
        self.assertTrue(CustomList([]) != CustomList([1]))
        self.assertTrue(CustomList([10]) != CustomList([10, 1]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1]) != CustomList([2, 3]))

    def test_gt(self):
        self.assertTrue(CustomList([1, 1, 1]) > CustomList([2]))
        self.assertFalse(CustomList([1]) > CustomList([2]))
        self.assertFalse(CustomList([]) > CustomList([]))
        self.assertFalse(CustomList([]) > CustomList([0]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1]) > CustomList([5]))

    def test_ge(self):
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) >= CustomList([5]))
        self.assertFalse(CustomList([1, 1, 1, 1]) >= CustomList([5]))
        self.assertTrue(CustomList([]) >= CustomList([0]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1]) >= CustomList([6]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1]) >= CustomList([3, 2, 1]))

    def test_lt(self):
        self.assertFalse(CustomList([1, 1, 1]) < CustomList([2]))
        self.assertTrue(CustomList([1]) < CustomList([2]))
        self.assertFalse(CustomList([]) < CustomList([]))
        self.assertFalse(CustomList([]) < CustomList([0]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) < CustomList([6]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1])
                        < CustomList([1, 1, 1, 1, 1, 1]))

    def test_le(self):
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) <= CustomList([5]))
        self.assertTrue(CustomList([1, 1, 1, 1]) <= CustomList([5]))
        self.assertTrue(CustomList([]) <= CustomList([0]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) <= CustomList([6]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1]) <= CustomList([3, 2, 1]))
        self.assertTrue(CustomList([1, 1, 1, 1, 1, 1]) <= CustomList([6]))
        self.assertFalse(CustomList([1, 1, 1, 1, 1, 1]) <= CustomList([5]))
        self.assertTrue(CustomList([]) <= CustomList([]))


if __name__ == '__main__':
    unittest.main()
