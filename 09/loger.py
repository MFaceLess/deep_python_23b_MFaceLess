import logging
import argparse


class CustomFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return message.startswith("DANGER!!!")


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

    def move_to_end(self, tail):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.prev = tail.prev
        self.next = tail
        tail.prev.next = self
        tail.prev = self


class LRUCache:
    def __init__(self, logger_var, limit=42):
        self.logger = logger_var
        if limit <= 0:
            self.logger.debug(
                "Обработка исключения неккоретного limit для кэша")
            self.logger.critical(
                "DANGER!!! uncorrected limit, terminate the process")
            raise ValueError("limit must be above zero")
        self.limit = limit
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.logger.debug("Инициализация системы прошла успешно")

    def get(self, key):
        if key in self.cache:
            self.logger.info("get существующего ключа")
            node = self.cache[key]
            node.move_to_end(self.tail)
            self.logger.debug("возвращение None из get")
            return node.value
        self.logger.warning("get отсутствующего ключа")
        self.logger.debug("возвращение None из get")
        return None

    def set(self, key, value):
        if key in self.cache:
            self.logger.info("set существующего ключа")
            node = self.cache[key]
            node.value = value
            node.move_to_end(self.tail)
        else:
            self.logger.warning("set отсутствующего ключа")
            if len(self.cache) >= self.limit:
                self.logger.warning(
                    "set отсутствующего ключа, достингнута емкость")
                del_node = self.head.next
                del self.cache[del_node.key]
                self.head.next = del_node.next
                del_node.next.prev = self.head

            new_node = Node(key, value)
            self.cache[key] = new_node
            new_node.prev = self.tail.prev
            new_node.next = self.tail
            self.tail.prev.next = new_node
            self.tail.prev = new_node


def setup_logging(name_log_file, flag_log_to_stdout, flag_custom_filter):
    logging.basicConfig(filename=name_log_file, level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger_var = logging.getLogger(__name__)

    if flag_log_to_stdout:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger_var.addHandler(console_handler)

    if flag_custom_filter:
        filter_handler = CustomFilter()
        logger_var.addFilter(filter_handler)

    return logger_var


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Logging')
    parser.add_argument(
        '-s',
        '--stdout',
        action='store_true',
        help='Log to stdout')
    parser.add_argument(
        '-f',
        '--filter',
        action='store_true',
        help='Custom filter')
    args = parser.parse_args()

    LOG_FILE = 'cache.log'
    log_to_stdout = args.stdout
    custom_filter = args.filter

    logger = setup_logging(LOG_FILE, log_to_stdout, custom_filter)

    try:
        temp = LRUCache(logger_var=logger, limit=-5)
    except ValueError:
        pass

    cache = LRUCache(logger_var=logger, limit=2)

    cache.set('key1', 'value1')
    cache.get('key1')
    cache.get('key2')
    cache.set('key2', 'value2')
    cache.set('key3', 'value3')
    cache.get('key1')
    cache.set('key4', 'value4')
    cache.get('key2')
    cache.set('key4', 'value_changed')
