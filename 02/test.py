import unittest
from unittest import mock
import time

import point1
from point2 import mean


class TestModels(unittest.TestCase):
    def test_parse_json_no_keywords(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            mock_fetch.return_value = 'Call callback'
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["key5"]
            keywords = ["word2"]
            expected_calls = []
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            self.assertEqual(None, point1.parse_json(json_str))
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_key_not_exists(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["not_exist"]
            keywords = ["word2"]
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual([], mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_word_not_found(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["key1"]
            keywords = ["not_exists"]
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual([], mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_correct1(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["key1", "key2"]
            keywords = ["word2"]
            expected_call = [
                mock.call('word2'),
                mock.call('word2'),
            ]
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(2, mock_fetch.call_count)

    def test_parse_json_correct2(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = ["word2", "word3"]
            expected_call = [
                mock.call('word2'),
                mock.call('word2'),
                mock.call('word3'),
                mock.call('word3'),
            ]
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(4, mock_fetch.call_count)

    def test_parse_json_correct3(self):
        with mock.patch('point1.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key5"]
            keywords = ["word2", "word3"]
            expected_call = [
                mock.call('word2'),
                mock.call('word3'),
            ]
            self.assertEqual(
                None,
                point1.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    point1.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(2, mock_fetch.call_count)

    def test_decorator_without_argument(self):
        @mean()
        def some_function():
            time.sleep(0.1)

        with self.assertRaises(ValueError) as _:
            some_function()

    def test_decorator_with_argument(self):
        @mean(2)
        def another_function():
            time.sleep(0.2)

        @mean()
        def func():
            time.sleep(0.2)

        another_function()
        self.assertEqual(1, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
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

        another_function()
        self.assertEqual(1, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))

        func()
        self.assertEqual(1, len(func.call_times))
        func()
        self.assertEqual(2, len(func.call_times))
        func()
        self.assertEqual(3, len(func.call_times))
        func()
        self.assertEqual(3, len(func.call_times))

        another_function()
        self.assertEqual(2, len(another_function.call_times))
        another_function()
        self.assertEqual(2, len(another_function.call_times))

        func()
        self.assertEqual(3, len(func.call_times))
        func()
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
        self.assertEqual(1, len(func.call_times))
        func()
        self.assertEqual(2, len(func.call_times))
        func()
        self.assertEqual(3, len(func.call_times))

        for _ in range(0, 10):
            first_value_time = func.call_times[1]
            func()
            self.assertEqual(3, len(func.call_times))
            self.assertEqual(first_value_time, func.call_times[0])

        self.assertAlmostEqual(sum(func.call_times) /
                               len(func.call_times), 0.3, delta=0.01)


if __name__ == '__main__':
    unittest.main()
