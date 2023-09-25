import io


def file_read_filter_gen(file: str | io.TextIOWrapper, need_words: list[str]):
    if isinstance(file, str):
        try:
            with open(file, 'r', encoding='UTF-8') as file_:
                for line in file_:
                    temp = line.rstrip('\n').lower()
                    words_list = temp.split(' ')
                    for word in need_words:
                        if word.lower() in words_list:
                            yield line
                            break
        except OSError:
            print("Ошибка при открытии файла")
            raise
    elif isinstance(file, io.TextIOWrapper):
        for line in file:
            temp = line.rstrip('\n').lower()
            words_list = temp.split(' ')
            for word in need_words:
                if word.lower() in words_list:
                    yield line
                    break
    else:
        return
