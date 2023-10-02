import unittest
from unittest import mock

import predict_message_mood


class TestSomeModel(unittest.TestCase):
    def test_predict_message_mood(self):
        model = predict_message_mood.SomeModel()
        with mock.patch('predict_message_mood.SomeModel.predict') \
                as mock_fetch:
            mock_fetch.return_value = 0.81
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    "Чапаев и пустота", model))
            expected_calls = [
                mock.call('Чапаев и пустота')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    "", model))
            expected_calls = [
                mock.call('Чапаев и пустота'),
                mock.call('')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    "1", model))
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    "А", model))
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    "12r12raffdffsfgdsg", model))

    def test_predict_message_mood_good(self):
        model = predict_message_mood.SomeModel()
        with mock.patch('predict_message_mood.SomeModel.predict') \
                as mock_fetch:
            mock_fetch.return_value = 0.5
            self.assertEqual(
                'норм',
                predict_message_mood.predict_message_mood(
                    '',
                    model))
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    'asdad', model))
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    '21rfef21qfwef', model))
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    '21rfef21qfwef afaf', model))
            expected_calls = [
                mock.call(''),
                mock.call('asdad'),
                mock.call('21rfef21qfwef'),
                mock.call('21rfef21qfwef afaf')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_predict_message_mood_bad(self):
        model = predict_message_mood.SomeModel()
        with mock.patch('predict_message_mood.SomeModel.predict') \
                as mock_fetch:
            mock_fetch.return_value = 0.2
            self.assertEqual(
                'неуд',
                predict_message_mood.predict_message_mood(
                    '',
                    model))
            self.assertEqual(
                'неуд', predict_message_mood.predict_message_mood(
                    'asdad', model))
            self.assertEqual(
                'неуд', predict_message_mood.predict_message_mood(
                    '21rfef21qfwef', model))
            self.assertEqual(
                'неуд', predict_message_mood.predict_message_mood(
                    '21rfef21qfwef afaf', model))
            expected_calls = [
                mock.call(''),
                mock.call('asdad'),
                mock.call('21rfef21qfwef'),
                mock.call('21rfef21qfwef afaf')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_predict_message_mood_non_usual(self):
        model = predict_message_mood.SomeModel()
        with mock.patch('predict_message_mood.SomeModel.predict') \
                as mock_fetch:
            mock_fetch.return_value = 0
            self.assertEqual(
                'неуд', predict_message_mood.predict_message_mood(
                    '', model, 1, 0))
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    '', model, 0, 0))
            expected_calls = [
                mock.call(''),
                mock.call('')
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)

    def test_predict_message_mood_edge_cases(self):
        model = predict_message_mood.SomeModel()
        with mock.patch('predict_message_mood.SomeModel.predict') \
                as mock_fetch:
            mock_fetch.return_value = 0.3
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    'call_1', model, 0.3, 0.8))
            mock_fetch.return_value = 0.8
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    'call_2', model, 0.3, 0.8))
            mock_fetch.return_value = 0.299
            self.assertEqual(
                'неуд', predict_message_mood.predict_message_mood(
                    'call_3', model, 0.3, 0.8))
            mock_fetch.return_value = 0.30001
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    'call_4', model, 0.3, 0.8))
            mock_fetch.return_value = 0.799
            self.assertEqual(
                'норм', predict_message_mood.predict_message_mood(
                    'call_5', model, 0.3, 0.8))
            mock_fetch.return_value = 0.80001
            self.assertEqual(
                'отл', predict_message_mood.predict_message_mood(
                    'call_6', model, 0.3, 0.8))
            expected_calls = [
                mock.call('call_1'),
                mock.call('call_2'),
                mock.call('call_3'),
                mock.call('call_4'),
                mock.call('call_5'),
                mock.call('call_6'),
            ]
            self.assertEqual(expected_calls, mock_fetch.mock_calls)


if __name__ == '__main__':
    unittest.main()
