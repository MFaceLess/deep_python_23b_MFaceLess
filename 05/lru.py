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
    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError("limit must be above zero")
        self.limit = limit
        self.cache = {}
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            node.move_to_end(self.tail)
            return node.value
        return None

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            node.move_to_end(self.tail)
        else:
            if len(self.cache) >= self.limit:
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
