import cjson
import json
import unittest


class TestCustomList(unittest.TestCase):
    def test_cjson_load_not_str(self):
        with self.assertRaises(TypeError) as err:
            cjson.loads(5)
        self.assertEqual("Invalid argument", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads([1, 2, 3, 4, 5])
        self.assertEqual("Invalid argument", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads({"temp":2})
        self.assertEqual("Invalid argument", str(err.exception))

    def test_cjson_load_not_correct_str(self):
        with self.assertRaises(TypeError) as err:
            cjson.loads('not correct string')
        self.assertEqual("Expected object or value", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads('"integer": "temp"')
        self.assertEqual("Expected object or value", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads('{"integer":}')
        self.assertEqual("Expected object or value", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads('{"integer": 10')
        self.assertEqual("Expected object or value", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads('"integer": 10}')
        self.assertEqual("Expected object or value", str(err.exception))

    def test_cjson_load_src_str_not_changed(self):
        json_str = '{"hello temp": 10, "  world": "value  ", "temp": 5, "twef": "yep"}'
        cjson_doc = cjson.loads(json_str)
        self.assertEqual('{"hello temp": 10, "  world": "value  ", "temp": 5, "twef": "yep"}', json_str)

    def test_cjson_load_not_correct_value_key(self):
        json_str1 = '{"hello temp": [1,2,3]}'
        json_str2 = '{(1,2,3): 10}'
        with self.assertRaises(TypeError) as err:
            cjson.loads(json_str1)
        self.assertEqual("Expected object or value", str(err.exception))
        with self.assertRaises(TypeError) as err:
            cjson.loads(json_str2)
        self.assertEqual("Expected object or value", str(err.exception))

    def test_cjson_load_test_correct_work(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, cjson_doc)
        json_str = '{"hello  world ": 10, " world  ": "value  ", "temp": 124124124}'
        json_doc = json.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, cjson_doc)

    def test_cjson_dumps_not_correct_value(self):
        json_dict = [{"hello": 10}, {"world": "value"}]
        with self.assertRaises(TypeError) as err:
            cjson.dumps(json_dict)
        self.assertEqual("Invalid argument", str(err.exception))

    def test_cjson_dumps_correct_work(self):
        json_dict = {"hello": 10, "world": "value"}
        self.assertEqual(json.dumps(json_dict), cjson.dumps(json_dict))
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(json_doc, cjson_doc)
        self.assertEqual(json_str, cjson.dumps(cjson.loads(json_str)))

    def test_cjson_dumps_dict_not_changed(self):
        json_dict = {"hello": 10, "world": "value"}
        cjson.dumps(json_dict)
        self.assertEqual({"hello": 10, "world": "value"}, json_dict)


if __name__ == '__main__':
    unittest.main()
