def move_zeros(array):
    z = list(filter(lambda a: a == 0 and type(a) != type(False), array))
    r = list(filter(lambda a: a != 0 or type(a) == type(False), array)) + z
    return r



print(move_zeros([1,2,0,1,0,1,0,3,0,1]))
print(move_zeros([0,1,None,2,False,1,0]))