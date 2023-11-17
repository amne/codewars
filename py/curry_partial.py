import inspect


def curry_partial(f, *initial_args):
    if not inspect.isfunction(f):
        return f
    f_args = inspect.getfullargspec(f)
    if len(initial_args) < len(f_args[0]):
        def c(*passed_args):
            return curry_partial(f, *(initial_args + passed_args))

        return c
    else:
        if len(f_args[0]) == 0 and (f_args[1] != '' or f_args[2] != ''):
            return f(*(initial_args))
        else:
            return f(*(initial_args[:len(f_args[0])]))


def add(a, b, c):
    return a + b + c


a = 1
b = 2
c = 3

# print(add(1,2,3))
# print(curry_partial(add)(1)(2, 3))
print(curry_partial(curry_partial(add, 1, 2), 3))

# print(curry_partial(add)()(a)()()(b, c, 5, 6, 7))
