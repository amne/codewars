def count_bits(n):
    sum = 0
    while n:
        print('n=', n)
        print('n&1=', n&1)
        sum = sum + (n & 1)
        n = n >> 1
    return sum


print(count_bits(10))
