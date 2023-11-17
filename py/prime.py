from math import sqrt


def is_prime(num):
    # print('==begin==')
    if num < 2:
        return False

    sieve = list(range(2, int(sqrt(num))+1))
    # print('s=', sieve)
    k = 1
    while len(sieve):
        k = sieve[0]
        # print('k=', k)
        # print(num,' %% ', k, ' = ', num % k)
        if num % k == 0:
            return False
        dust = list(range(k, int(sqrt(num))+1, k))
        # print('dust=', dust)
        # print([k for k in sieve if k not in dust])
        sieve = [k for k in sieve if k not in dust]
    return True


# print('-1 ', is_prime(-1))
# print('0 ', is_prime(0))
# print('5 ', is_prime(5))
print('4 ', is_prime(4))
print('8 ', is_prime(8))
print('75 ', is_prime(75))
print('73 ', is_prime(73))
# print('2 ', is_prime(2))






def is_prime_submitted(num):
    if num < 2:
        return False

    for k in range(2, int(sqrt(num))+1):
        if num % k == 0:
            return False
    return True