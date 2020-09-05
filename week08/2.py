
def map_self(func, *args):
    try:
        length = len(args[0])
        for i in range(length):
            yield(func(*[arg[i] for arg in args]))
    except TypeError:
        raise
    except IndexError:
        pass
    else:
        pass