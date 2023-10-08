import unittest

import descriptors


class TestCustomList(unittest.TestCase):
    def test_get_empty_values(self):
        self.assertIsNone(descriptors.ChessOpeningsPrepare.fr_opening)
        self.assertIsNone(descriptors.ChessOpeningsPrepare.rus_opening)
        self.assertIsNone(descriptors.ChessOpeningsPrepare.sicilian_opening)

    def test_not_correct_prepare(self):
        with self.assertRaises(ValueError) as err:
            my_prepare = descriptors.ChessOpeningsPrepare(
                "e4 e5 kf3 kf6", "e4 c5", "e4 a6")
        self.assertEqual("wrong opening", str(err.exception))

        my_prepare = descriptors.ChessOpeningsPrepare(
            "e4 e5 kf3 kf6", "e4 c5", "e4 e6")
        with self.assertRaises(ValueError) as err:
            my_prepare.rus_opening = "e4 e5 kf3 kc6"
        self.assertEqual("wrong opening", str(err.exception))

        with self.assertRaises(ValueError) as err:
            my_prepare.sicilian_opening = "e4 b6"
        self.assertEqual("wrong opening", str(err.exception))

        with self.assertRaises(ValueError) as err:
            my_prepare.fr_opening = "e4 b6"
        self.assertEqual("wrong opening", str(err.exception))

    def test_not_correct_type(self):
        my_prepare = descriptors.ChessOpeningsPrepare(
            "e4 e5 kf3 kf6", "e4 c5", "e4 e6")
        with self.assertRaises(ValueError) as err:
            my_prepare.rus_opening = 15
        self.assertEqual("string notation required", str(err.exception))

        with self.assertRaises(ValueError) as err:
            my_prepare.sicilian_opening = 15
        self.assertEqual("string notation required", str(err.exception))

        with self.assertRaises(ValueError) as err:
            my_prepare.fr_opening = 15
        self.assertEqual("string notation required", str(err.exception))

    def test_correct_values(self):
        my_prepare = descriptors.ChessOpeningsPrepare(
            "e4 e5 kf3 kf6", "e4 c5", "e4 e6")
        my_prepare.fr_opening = "e4 e6 d4 d5 kc3 cb4"
        self.assertEqual("e4 e6 d4 d5 kc3 cb4", my_prepare.fr_opening)
        my_prepare.sicilian_opening = "e4 c5 kf3 kc6 d4 cd kd4"
        self.assertEqual(
            "e4 c5 kf3 kc6 d4 cd kd4",
            my_prepare.sicilian_opening)
        my_prepare.rus_opening = "e4 e5 kf3 kf6 ke5 d6 kf3 ke4"
        self.assertEqual(
            "e4 e5 kf3 kf6 ke5 d6 kf3 ke4",
            my_prepare.rus_opening)


if __name__ == '__main__':
    unittest.main()
