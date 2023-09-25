import unittest
from unittest import mock

import point1
import point2


class TestSomeModel(unittest.TestCase):
    def test_predict_message_mood(self):
        model = point1.SomeModel()
        with mock.patch('point1.SomeModel.predict') as mock_fetch:
            mock_fetch.return_value = 0.81
            self.assertEqual(
                'отл', point1.predict_message_mood(
                    "Чапаев и пустота", model))
            expected_calls = [
                mock.call('Чапаев и пустота')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual('отл', point1.predict_message_mood("", model))
            expected_calls = [
                mock.call('Чапаев и пустота'),
                mock.call('')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual('отл', point1.predict_message_mood("1", model))
            self.assertEqual('отл', point1.predict_message_mood("А", model))
            self.assertEqual(
                'отл', point1.predict_message_mood(
                    "12r12raffdffsfgdsg", model))

    def test_predict_message_mood_good(self):
        model = point1.SomeModel()
        with mock.patch('point1.SomeModel.predict') as mock_fetch:
            mock_fetch.return_value = 0.5
            self.assertEqual('норм', point1.predict_message_mood('', model))
            self.assertEqual(
                'норм', point1.predict_message_mood(
                    'asdad', model))
            self.assertEqual(
                'норм', point1.predict_message_mood(
                    '21rfef21qfwef', model))
            self.assertEqual(
                'норм', point1.predict_message_mood(
                    '21rfef21qfwef afaf', model))
            expected_calls = [
                mock.call(''),
                mock.call('asdad'),
                mock.call('21rfef21qfwef'),
                mock.call('21rfef21qfwef afaf')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_predict_message_mood_bad(self):
        model = point1.SomeModel()
        with mock.patch('point1.SomeModel.predict') as mock_fetch:
            mock_fetch.return_value = 0.2
            self.assertEqual('неуд', point1.predict_message_mood('', model))
            self.assertEqual(
                'неуд', point1.predict_message_mood(
                    'asdad', model))
            self.assertEqual(
                'неуд', point1.predict_message_mood(
                    '21rfef21qfwef', model))
            self.assertEqual(
                'неуд', point1.predict_message_mood(
                    '21rfef21qfwef afaf', model))
            expected_calls = [
                mock.call(''),
                mock.call('asdad'),
                mock.call('21rfef21qfwef'),
                mock.call('21rfef21qfwef afaf')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_predict_message_mood_non_usual(self):
        model = point1.SomeModel()
        with mock.patch('point1.SomeModel.predict') as mock_fetch:
            mock_fetch.return_value = 0
            self.assertEqual(
                'неуд', point1.predict_message_mood(
                    '', model, 1, 0))
            self.assertEqual(
                'норм', point1.predict_message_mood(
                    '', model, 0, 0))
            expected_calls = [
                mock.call(''),
                mock.call('')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_file_read_filter_gen(self):
        file_content = """а Роза упала на лапу Азора1\n
а эта строчка уже не подходит\n
а Роза упала на лапу Азора3\n"""
        with mock.patch(
            'builtins.open',
            new=unittest.mock.mock_open(read_data=file_content),
                create=True) as _:
            result = point2.file_read_filter_gen('test_file.txt', ['роза'])
            self.assertEqual(next(result), 'а Роза упала на лапу Азора1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            with self.assertRaises(StopIteration) as _:
                next(result)

    def test_file_read_filter_gen_begin(self):
        file_content = """а Роза упала на лапу Азора1\n
слово эта строчка уже не подходит\n
а Роза упала на лапу Азора3\n"""
        with mock.patch('builtins.open',
                        new=unittest.mock.mock_open(
                            read_data=file_content),
                        create=True) as _:
            result = point2.file_read_filter_gen(
                'test_file.txt', ['роз', 'подходит', 'розан'])
            self.assertEqual(next(result),
                             'слово эта строчка уже не подходит\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = point2.file_read_filter_gen(
                'test_file.txt', ['слово'])
            self.assertEqual(next(result),
                             'слово эта строчка уже не подходит\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = point2.file_read_filter_gen(
                'test_file.txt', ['Азора3'])
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = point2.file_read_filter_gen(
                'test_file.txt', ['а Роза'])
            with self.assertRaises(StopIteration) as _:
                next(result)

    def test_file_read_filter_gen_not_exists(self):
        file_content = ""
        with mock.patch('builtins.open',
                        new=unittest.mock.mock_open(read_data=file_content),
                        create=True) as file_mock:
            file_mock.side_effect = OSError
            with self.assertRaises(OSError) as _:
                result = point2.file_read_filter_gen(
                    'test_file.txt', ['а Роза'])
                next(result)

    def test_file_read_filter_gen_empty(self):
        file_content = ""
        with mock.patch('builtins.open',
                        new=unittest.mock.mock_open(read_data=file_content),
                        create=True) as _:
            result = point2.file_read_filter_gen(
                'test_file.txt', [''])
            with self.assertRaises(StopIteration) as _:
                next(result)

    def test_file_read_filter_file_obj(self):
        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = point2.file_read_filter_gen(file_, ['роз', 'розан'])
            with self.assertRaises(StopIteration) as _:
                next(result)

        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = point2.file_read_filter_gen(file_, ['роза'])
            self.assertEqual(next(result), 'а роза на лапу Азора 1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора 3')
            with self.assertRaises(StopIteration) as _:
                next(result)

        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = point2.file_read_filter_gen(file_, [])
            with self.assertRaises(StopIteration) as _:
                next(result)


if __name__ == '__main__':
    unittest.main()
