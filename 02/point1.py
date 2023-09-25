import json


def keyword_callback(_):
    pass


def parse_json(json_str: str, required_fields=None,
               keywords=None, keyword_callback_=None):
    json_doc = json.loads(json_str)
    if required_fields is not None or keywords \
            is not None or keyword_callback_ is not None:
        for key in required_fields:
            if key in json_doc:
                lst_word = json_doc[key].split(' ')
                for word in lst_word:
                    if word in keywords:
                        keyword_callback_(word)
