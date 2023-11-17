def height2(n, m):
    facts = {}

    f = max(n, m)
    i = 1
    z = 1
    while i <= f:
        z = z * i
        facts[i] = z
        i = i + 1
    s = 0
    n = min(n, m)
    mprod = m
    while n > 0:
        # print('m=', m, '; m-n=', m - n, '; n=', n)
        # print('m!=', facts[m], '; (m-n)!=', facts[m - n], '; n!=', facts[n])
        # print('s=', s)
        # print('max_floor_local=', (facts[m] // (facts[m - n] * facts[n])))
        s = s + (facts[m] // (facts[m - n] * facts[n]))
        n = n - 1

    return s


def height(n, m):
    # idea: sum series of m! / ( (m-n)! * n! )      where n goes to 1 and m stays put.
    # optimization: m! / (m-n)!    is actually m * (m-1) * (m-2) .... so you don't need to recalculate m! everytime. just multiply with new "m-1"
    # same idea for m! / k!    is actually   (m! / n!)  divided by 1, 2, 3 as you move through each "egg".
    # so in the loop just multiply by new m and divide by new k as m decreases and k increases until k = n aka all eggs have been crushed

    s = 0
    n = min(n, m)  # cover edge cases
    k = 1
    mprod = m
    while k <= n:
        s = s + mprod
        m -= 1
        k += 1
        mprod *= m
        mprod //= k

    return s

def height3(n, m):
    h, t = 0, 1
    for i in range(1, n + 1):
        t = t * (m - i + 1) // i
        h += t
    return h


print(height(2, 14))
print(height2(2, 14))
print(height(7, 20))
print(height2(7, 20))
print(height(7, 500))
print(height2(7, 500))
print(height(2, 0))
print(height2(2, 0))
print(height(0, 14))
print(height2(0, 14))
print(height(237, 500))
print(height2(237, 500))
print(height(477, 500))
print(height2(477, 500))
print(height(477, 2000))
print(height2(477, 2000))
print(height(477, 5000))
print(height2(477, 5000))
print('serious')
print(height(4477, 10000))
print(height3(4477, 10000))
