def memofx(f):
    cache = {}

    def fx(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]
    return fx


def fibonacci(n):
    if n in [0, 1]:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


fibonacci = memofx(fibonacci)

print(fibonacci(70))
