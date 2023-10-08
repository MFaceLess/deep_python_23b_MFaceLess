import unittest

from meta_class import CustomMeta


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val
        self.__priv = 1000

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


class TestCustomList(unittest.TestCase):
    def test_new(self):
        self.assertEqual(50, CustomClass.custom_x)
        with self.assertRaises(AttributeError) as err:
            CustomClass.x

        self.assertEqual(AttributeError, type(err.exception))

    def test_class_and_obj_attr_and_priv(self):
        inst = CustomClass()
        self.assertEqual(50, inst.custom_x)
        self.assertEqual(99, inst.custom_val)
        self.assertEqual(1000, inst.custom__CustomClass__priv)
        self.assertEqual(100, inst.custom_line())

    def test_save_magic_method(self):
        inst = CustomClass()
        self.assertTrue(hasattr(inst, '__init__'))
        self.assertTrue(hasattr(inst, '__str__'))
        self.assertEqual("Custom_by_metaclass", str(inst))
        self.assertFalse(hasattr(inst, 'line'))
        self.assertTrue(hasattr(inst, 'custom_line'))

    def test_no_have_acess_to_old_attr(self):
        inst = CustomClass()
        with self.assertRaises(AttributeError) as _:
            inst.x

        with self.assertRaises(AttributeError) as _:
            inst.val

        with self.assertRaises(AttributeError) as _:
            inst.line()

        with self.assertRaises(AttributeError) as _:
            inst.yyy

    def test_changin_after_construct(self):
        inst = CustomClass()
        inst.dynamic = "added later"
        self.assertEqual("added later", inst.custom_dynamic)
        with self.assertRaises(AttributeError) as _:
            inst.dynamic


if __name__ == '__main__':
    unittest.main()
