import unittest
from unittest import mock

import parser_json


class TestModels(unittest.TestCase):
    def test_parse_json_no_keywords(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            mock_fetch.return_value = 'Call callback'
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["key5"]
            keywords = ["word2"]
            expected_calls = []
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_default_args(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            mock_fetch.return_value = 'Call callback'
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            expected_calls = []

            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            self.assertEqual(None, parser_json.parse_json(json_str))
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_word_not_found(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
            required_fields = ["key1"]
            keywords = ["not_exists"]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual([], mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_correct1(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = ["word2", "word3"]
            expected_call = [
                mock.call('key1', 'word2'),
                mock.call('key2', 'word2'),
                mock.call('key2', 'word3'),
                mock.call('key5', 'word3'),
            ]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(4, mock_fetch.call_count)

    def test_parse_json_correct_not_all_keywords(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key5"]
            keywords = ["word2", "word3"]
            expected_call = [
                mock.call('key1', 'word2'),
                mock.call('key5', 'word3'),
            ]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(2, mock_fetch.call_count)

    def test_parse_json_edge_case1(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 Word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = ["word1", "word3"]
            expected_call = [
                mock.call('key1', 'Word1'),
                mock.call('key2', 'Word3'),
                mock.call('key5', 'word3'),
            ]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(3, mock_fetch.call_count)

    def test_parse_json_edge_case_whole_sentences(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "Word1 word2", "key2": "word2 Word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = ["word1 word2"]
            expected_call = []
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_edge_empty_sentences1(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "", "key2": "word2 Word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = [""]
            expected_call = [
                mock.call('key1', ""),
            ]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(1, mock_fetch.call_count)

    def test_parse_json_edge_empty_sentences2(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "saffsa", "key2": "word2 Word3", \
            "key5": "word3 word5"}'
            required_fields = ["key1", "key2", "key5"]
            keywords = [""]
            expected_call = []
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(0, mock_fetch.call_count)

    def test_parse_json_edge_empty_sentences3(self):
        with mock.patch('parser_json.keyword_callback') as mock_fetch:
            json_str = '{"key1": "", "key2": "", \
            "key5": ""}'
            required_fields = ["key1", "key2", "key5"]
            keywords = [""]
            expected_call = [
                mock.call('key1', ""),
                mock.call('key2', ""),
                mock.call('key5', ""),
            ]
            self.assertEqual(
                None,
                parser_json.parse_json(
                    json_str,
                    required_fields,
                    keywords,
                    parser_json.keyword_callback))
            self.assertEqual(expected_call, mock_fetch.mock_calls)
            self.assertEqual(3, mock_fetch.call_count)


if __name__ == '__main__':
    unittest.main()
