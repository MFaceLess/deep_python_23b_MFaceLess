import json


def keyword_callback(_):
    pass


def parse_json(json_str: str, required_fields=None,
               keywords=None, keyword_callback_=None):
    json_doc = json.loads(json_str)
    if required_fields is None or keywords \
            is None or keyword_callback_ is None:
        return
    for key in required_fields:
        if key not in json_doc:
            continue
        if any(json_doc[key].lower() == elem.lower() for elem in keywords):
            keyword_callback_(json_doc[key])
            continue
        lst_word = json_doc[key].split(' ')
        for word in lst_word:
            if any(word.lower() == elem.lower() for elem in keywords):
                keyword_callback_(word)
