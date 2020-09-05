
from functools import wraps
def timer(func):
    @wraps(func)
    def time_display(*args, **kargs):
        import time
        begin = time.time()
        result = func(*args, **kargs)
        end = time.time()
        print(f'total run time is {end - begin:.2f}s')
        return result
    return time_display