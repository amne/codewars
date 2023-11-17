def sort_array(source_array):
    l = []
    for i,k in enumerate(source_array):
        if k % 2:
            continue
        l.append([i,k]);
    r = list(filter(lambda n: n % 2 == 1, source_array))
    r.sort()
    for even in l:
        r = r[0:even[0]] + [even[1]] + r[even[0]:]
    return r
    # Return a sorted array.



print(sort_array([5,3,2,1,4,7,6]))