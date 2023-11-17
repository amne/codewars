from functools import lru_cache


class BigNum:
    def __init__(self, n):
        self.sign = 1
        if n < 0:
            self.sign = -1
        self.digits = [int(c) for c in str(abs(n))]
        self.digits.reverse()

    def print(self):
        p = ''.join(reversed([str(d) for d in self.digits]))
        p = p.lstrip('0')
        if len(p) == 0:
            self.sign = 1
            return '0'
        if self.sign < 0:
            p = '-' + p
        return p

    def digit(self, idx):
        if idx >= len(self.digits):
            return 0
        return self.digits[idx]

    def set_digits(self, digits):
        self.digits = digits

    def add(self, n):
        carry = 0

        def add_digits(a, b):
            nonlocal carry
            c = a + b + carry
            carry = 0
            if c >= 10:
                carry = 1
                c = c - 10
            else:
                if c < 0:
                    carry = -1
                    c = c + 10
            return c

        max_len = max(len(self.digits), len(n.digits))
        new_digits = [0] * max_len

        for x in range(max_len):
            new_digits[x] = add_digits(self.digit(x) * self.sign, n.digit(x) * n.sign)
        if carry > 0:
            new_digits.append(carry)

        self.set_digits(new_digits)
        return self

    def copy(self):
        k = BigNum(0)
        k.digits = list(self.digits)
        k.sign = self.sign
        return k

    def mul(self, n):
        k = BigNum(0)
        k.digits = [d for d in self.digits]
        k.sign = self.sign
        n.add(BigNum(-1 * n.sign))
        while n.print() != '0':
            self.add(k)
            n.add(BigNum(-1 * n.sign))

        return self


def fib(n):
    fib0 = BigNum(0)
    fib1 = BigNum(1)
    fib2 = BigNum(1)
    while n > 0:
        fib2 = fib0.add(fib1).copy()
        fib0 = fib1.copy()
        fib1 = fib2.copy()
        n = n - 1
    return fib0.print()


print('fib=', fib(10))
