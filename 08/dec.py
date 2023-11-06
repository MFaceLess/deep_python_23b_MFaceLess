import cProfile
import pstats
from io import StringIO


def profile_deco(func):
    def wrapper(*args, **kwargs):
        if not hasattr(wrapper, 'profile'):
            wrapper.profile = cProfile.Profile()

        wrapper.profile.enable()
        result = func(*args, **kwargs)
        wrapper.profile.disable()

        return result

    def print_stat():
        if hasattr(wrapper, 'profile'):
            output_stream = StringIO()
            sortby = 'cumulative'
            ps = pstats.Stats(wrapper.profile,
                              stream=output_stream).sort_stats(sortby)
            ps.print_stats()
            print(output_stream.getvalue())

    wrapper.print_stat = print_stat
    return wrapper


if __name__ == '__main__':
    @profile_deco
    def add(a, b):
        return a + b

    @profile_deco
    def sub(a, b):
        return a - b

    add(1, 2)
    add(4, 5)
    sub(4, 5)

    add.print_stat()
    sub.print_stat()
