import time
import weakref

from memory_profiler import profile


class MockClass:
    pass


class UsualAttrClass:
    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2


class SlotsClass:
    __slots__ = ('val1', 'val2')

    def __init__(self, val1, val2):
        self.val1 = val1
        self.val2 = val2


class WeakRefClass:
    def __init__(self, val1, val2):
        self.val1 = weakref.ref(val1)
        self.val2 = weakref.ref(val2)


@profile
def create_attr(cls):
    start_time = time.time()
    attr_inst = [cls(MockClass(), MockClass()) for _ in range(100000)]
    end_time = time.time()
    print(f'Elapsed time for attributes = {end_time - start_time}\n')
    return attr_inst


@profile
def changing_inst_atr(ints_attr):
    start_time = time.time()
    for inst in ints_attr:
        inst.val1 = MockClass()
        inst.val2 = MockClass()
    end_time = time.time()
    print(f'Elapsed time for changing attributes = {end_time - start_time}\n')


if __name__ == '__main__':
    usual_attr_inst = create_attr(UsualAttrClass)
    slots_attr_inst = create_attr(SlotsClass)
    weak_ref_attr_inst = create_attr(WeakRefClass)
    # Измерение время изменения атрибутов
    changing_inst_atr(usual_attr_inst)
    changing_inst_atr(slots_attr_inst)
    changing_inst_atr(weak_ref_attr_inst)
