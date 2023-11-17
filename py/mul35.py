def solution(number):
    return sum(map(lambda a: 3*(a+1), range((number-1) // 3))) + sum(filter(lambda n: n % 3 > 0, map(lambda a: 5*(a+1), range((number-1) // 5))))


# 3 + 6 + 9    +    5 = 23
print(solution(0))
print(solution(10))


# (3 , 5 , 6 , 9 , 10, 12, 15, 18)
# (3,6,9,12,15,18) + (5,10,15)
# (3 + 6 + 9 + 5) + 12 + 15 + 18     +    10 = 23 + 45 + 10 = 78
print(solution(20))
print(solution(200))