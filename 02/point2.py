import time


def mean(num_of_call=0):
    def _repeat(fun):
        def inner(*args, **kwargs):
            if num_of_call == 0:
                raise ValueError

            if not hasattr(inner, 'call_times'):
                inner.call_times = []

            time1 = time.time()
            res = fun(*args, **kwargs)
            time2 = time.time()

            elapsed_time = time2 - time1
            inner.call_times.append(elapsed_time)

            if len(inner.call_times) > num_of_call:
                inner.call_times.pop(0)

            average_time = sum(inner.call_times) / len(inner.call_times)

            print(
                f'Вызовов - {len(inner.call_times)}, \
                Среднее время - {average_time}')

            return res
        return inner
    return _repeat
