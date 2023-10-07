import unittest
import time
import sys
from io import StringIO
import re

from time_decorator import mean


class TestModels(unittest.TestCase):
    def setUp(self):
        self.original_stdout = sys.stdout
        self.redirect_stdout = StringIO()
        sys.stdout = self.redirect_stdout

    def tearDown(self):
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        sys.stdout = self.original_stdout

    def test_decorator_without_argument(self):
        @mean()
        def some_function():
            time.sleep(0.1)

        with self.assertRaises(ValueError) as err:
            some_function()

        self.assertEqual("Некорректное значение", str(err.exception))

    def test_decorator_with_less_zero_arg(self):
        @mean(-10)
        def some_function():
            time.sleep(0.1)

        with self.assertRaises(ValueError) as err:
            some_function()

        self.assertEqual("Некорректное значение", str(err.exception))

    def test_decorator_with_argument(self):
        @mean(2)
        def another_function():
            time.sleep(0.2)

        @mean()
        def func():
            time.sleep(0.2)

        another_function()
        expected_pattern = r"^Вызовов - 1, Среднее время - 0.200[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(1, len(another_function.call_times))
        another_function()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.200[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.200[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.200[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(2, len(another_function.call_times))

        with self.assertRaises(ValueError) as _:
            func()

    def test_decorator_with_functions(self):
        @mean(2)
        def another_function():
            time.sleep(0.2)

        @mean(3)
        def func():
            time.sleep(0.3)

        def check_pattern(pattern, func_):
            self.redirect_stdout.truncate(0)
            self.redirect_stdout.seek(0)
            func_()
            return re.fullmatch(pattern, self.redirect_stdout.getvalue())

        expected_pattern = r"^Вызовов - 1, Среднее время - 0.200[0-9]*\n$"
        self.assertIsNotNone(check_pattern(expected_pattern, another_function))
        self.assertEqual(1, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.200[0-9]*\n$"
        self.assertIsNotNone(check_pattern(expected_pattern, another_function))
        self.assertEqual(2, len(another_function.call_times))

        func()
        self.assertEqual(1, len(func.call_times))
        func()
        self.assertEqual(2, len(func.call_times))
        func()
        self.assertEqual(3, len(func.call_times))
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        func()
        expected_pattern = r"^Вызовов - 3, Среднее время - 0.300[0-9]*\n$"
        self.assertIsNotNone(check_pattern(expected_pattern, func))
        self.assertEqual(3, len(func.call_times))

        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.200[0-9]*\n$"
        self.assertIsNotNone(check_pattern(expected_pattern, another_function))
        self.assertEqual(2, len(another_function.call_times))

        func()
        self.assertEqual(3, len(func.call_times))
        func()
        expected_pattern = r"^Вызовов - 3, Среднее время - 0.300[0-9]*\n$"
        self.assertIsNotNone(check_pattern(expected_pattern, func))
        self.assertEqual(3, len(func.call_times))

        self.assertAlmostEqual(sum(another_function.call_times) /
                               len(another_function.call_times), 0.2,
                               delta=0.01)
        self.assertAlmostEqual(sum(func.call_times) /
                               len(func.call_times), 0.3,
                               delta=0.01)

    def test_decorator_shift_queue(self):
        @mean(3)
        def func():
            time.sleep(0.3)

        func()
        expected_pattern = r"^Вызовов - 1, Среднее время - 0.300[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(1, len(func.call_times))
        func()
        expected_pattern = r"^Вызовов - 2, Среднее время - 0.300[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(2, len(func.call_times))
        func()
        expected_pattern = r"^Вызовов - 3, Среднее время - 0.300[0-9]*\n$"
        temp = re.fullmatch(expected_pattern, self.redirect_stdout.getvalue())
        self.redirect_stdout.truncate(0)
        self.redirect_stdout.seek(0)
        self.assertIsNotNone(temp)
        self.assertEqual(3, len(func.call_times))

        for _ in range(0, 10):
            first_value_time = func.call_times[1]
            func()
            expected_pattern = r"^Вызовов - 3, Среднее время - 0.300[0-9]*\n$"
            temp = re.fullmatch(
                expected_pattern,
                self.redirect_stdout.getvalue())
            self.redirect_stdout.truncate(0)
            self.redirect_stdout.seek(0)
            self.assertIsNotNone(temp)
            self.assertEqual(3, len(func.call_times))
            self.assertEqual(first_value_time, func.call_times[0])

        self.assertAlmostEqual(sum(func.call_times) /
                               len(func.call_times), 0.3, delta=0.01)


if __name__ == '__main__':
    unittest.main()
