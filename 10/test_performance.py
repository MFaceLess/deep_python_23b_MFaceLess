import json
import cjson
import ujson
import time


if __name__ == '__main__':
    name = "temp0"
    big_dict_for_dumps = {}
    for i in range(10000):
        name = name.replace(str(i), str(i+1))
        big_dict_for_dumps[name] = i
    
    time_start = time.time()
    ans_json = json.dumps(big_dict_for_dumps)
    time_end = time.time()

    print(f"Время выполнения dumps для модуля JSON: {time_end - time_start}")

    time_start = time.time()
    ans_cjson = cjson.dumps(big_dict_for_dumps)
    time_end = time.time()

    print(f"Время выполнения dumps для модуля C_JSON: {time_end - time_start}")
    assert(ans_json == ans_cjson)

    time_start = time.time()
    _ = ujson.dumps(big_dict_for_dumps)
    time_end = time.time()

    print(f"Время выполнения dumps для модуля UJSON: {time_end - time_start}\n")

    time_start = time.time()
    ans_json_l = json.loads(ans_json)
    time_end = time.time()

    print(f"Время выполнения loads для модуля JSON: {time_end - time_start}")

    time_start = time.time()
    ans_cjson_l = cjson.loads(ans_json)
    time_end = time.time()

    print(f"Время выполнения loads для модуля C_JSON: {time_end - time_start}")
    assert(json.dumps(ans_json_l) == cjson.dumps(ans_cjson_l))

    time_start = time.time()
    ans_cjson_l = ujson.loads(ans_json)
    time_end = time.time()

    print(f"Время выполнения loads для модуля U_JSON: {time_end - time_start}")
