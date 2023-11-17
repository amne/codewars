def mat_mul(fa, fb):
    f = (
        fa[0] * fb[0] + fa[1] * fb[2],
        fa[0] * fb[1] + fa[1] * fb[3],
        fa[2] * fb[0] + fa[3] * fb[2],
        fa[2] * fb[1] + fa[3] * fb[3]
    )
    return f


def mat_pow(f, n):
    if n == 0:
        return 1, 0, 0, 1
    if n == 1:
        return f
    if n % 2 == 0:
        # inline the square operation: mat_mul(f,f)
        return mat_pow((
            (f[0] * f[0] + f[1] * f[2]),
            (f[0] * f[1] + f[1] * f[3]),
            (f[2] * f[0] + f[3] * f[2]),
            (f[2] * f[1] + f[3] * f[3])
        ), n // 2)
    else:
        return mat_mul(mat_pow(f, n - 1), f)


def fib(n):
    # my first thought was of course iteration but then I remembered the spiral and
    # all the matrix multiplications I was doing in my 3d rendering era to rotate stuff in 2d and 3d
    #
    # a bit of research about fibonacci and matrices got me to this article:
    # https://simonwo.net/technical/log-time-fibonacci/
    # after all the math it becomes clear that you can do the matrix power operation in log(n) steps and then it clicked
    #
    # for negative N: if N is negative just start with a negative transformation matrix

    f = (1, 1, 1, 0)
    if n < 0:
        f = (-1, -1, -1, 0)
    ff = mat_pow(f, abs(n))

    # the sign is backwards because of the odd number of multiplications
    return ff[1] * f[0]


print(fib(-1)) # 1
print(fib(-41)) # 165580141
print(fib(-48)) # -4807526976
print(fib(-53)) # 53316291173

print(fib(1000))