import io


def file_read_filter_gen(file: str | io.TextIOWrapper, need_words: list[str]):
    try:
        file_descriptor = None
        if isinstance(file, str):
            file_descriptor = open(file, 'r', encoding='UTF-8')
        elif isinstance(file, io.TextIOWrapper):
            file_descriptor = file
        if file_descriptor is not None:
            for line in file_descriptor:
                temp = line.rstrip('\n').lower()
                words_list = temp.split(' ')
                for word in need_words:
                    if word.lower() in words_list:
                        yield line
                        break
        if isinstance(file, str):
            file_descriptor.close()
    except OSError as oserror:
        raise OSError("Ошибка при работе с файлом") from oserror
