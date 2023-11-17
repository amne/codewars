from math import sqrt


def productFib(prod):
    ret = [0, 1]

    for k in range(-1,int(sqrt(prod))+1):
        if ret[0] * ret[1] == prod:
            return ret + [True]
        if ret[0] * ret[1] > prod:
            return ret + [False]
        fibT = ret[0]
        ret[0] = ret[1]
        ret[1] = fibT + ret[1]
    return ret + [False]


def productFib2(prod):
  a, b = 0, 1
  while prod > a * b:
    a, b = b, a + b
  return [a, b, prod == a * b]


print(productFib2(4895))
print(productFib2(5895))
print(productFib2(2))
