import unittest
from unittest import mock

import file_read_filter_gen


class TestSomeModel(unittest.TestCase):
    def test_file_read_filter_gen(self):
        file_content = """а Роза упала на лапу Азора1\n
а эта строчка уже не подходит\n
а Роза упала на лапу Азора3\n"""
        with mock.patch(
            'builtins.open',
            new=unittest.mock.mock_open(read_data=file_content),
                create=True) as _:
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['роза'])
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
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['роз', 'подходит', 'розан'])
            self.assertEqual(next(result),
                             'слово эта строчка уже не подходит\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['слово'])
            self.assertEqual(next(result),
                             'слово эта строчка уже не подходит\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['Азора3'])
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            with self.assertRaises(StopIteration) as _:
                next(result)
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['а Роза'])
            with self.assertRaises(StopIteration) as _:
                next(result)

    def test_file_read_filter_gen_not_exists(self):
        file_content = ""
        with mock.patch('builtins.open',
                        new=unittest.mock.mock_open(read_data=file_content),
                        create=True) as file_mock:
            file_mock.side_effect = OSError
            with self.assertRaises(OSError) as err:
                result = file_read_filter_gen.file_read_filter_gen(
                    'test_file.txt', ['а Роза'])
                next(result)
            self.assertEqual("Ошибка при работе с файлом", str(err.exception))
            self.assertEqual(OSError, type(err.exception))

    def test_file_read_filter_gen_empty(self):
        file_content = ""
        with mock.patch('builtins.open',
                        new=unittest.mock.mock_open(read_data=file_content),
                        create=True) as _:
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', [''])
            with self.assertRaises(StopIteration) as _:
                next(result)

    def test_file_read_filter_file_obj(self):
        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = file_read_filter_gen.file_read_filter_gen(
                file_, ['роз', 'розан'])
            with self.assertRaises(StopIteration) as _:
                next(result)

        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = file_read_filter_gen.file_read_filter_gen(file_, ['роза'])
            self.assertEqual(next(result), 'а роза на лапу Азора 1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора 3')
            with self.assertRaises(StopIteration) as _:
                next(result)

        with open('./test.txt', 'r', encoding='UTF-8') as file_:
            result = file_read_filter_gen.file_read_filter_gen(file_, [])
            with self.assertRaises(StopIteration) as _:
                next(result)

    # тест на случай если искомое слово == всей строке целиком (добавлено)
    def test_file_read_word_sentence(self):
        file_content = """а Роза упала на лапу Азора1\n
а Роза упала на лапу Азора1\n
а Роза упала на лапу Азора1\n"""
        with mock.patch(
            'builtins.open',
            new=unittest.mock.mock_open(read_data=file_content),
                create=True) as _:
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['а Роза упала на лапу Азора1'])
            with self.assertRaises(StopIteration) as _:
                next(result)
    # -----------------------------------------------------------------------

    def test_file_read_many_words_in_one_sentence(self):
        file_content = """а Роза упала на лапу Азора1\n
а Роза упала на лапу Азора2\n
а Роза упала на лапу Азора3\n"""
        with mock.patch(
            'builtins.open',
            new=unittest.mock.mock_open(read_data=file_content),
                create=True) as _:
            result = file_read_filter_gen.file_read_filter_gen(
                'test_file.txt', ['роза', 'упала', 'лапу'])
            self.assertEqual(next(result), 'а Роза упала на лапу Азора1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора1\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора2\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора2\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора2\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            self.assertEqual(next(result), 'а Роза упала на лапу Азора3\n')
            with self.assertRaises(StopIteration) as _:
                next(result)


if __name__ == '__main__':
    unittest.main()
