def hamming(nth):
    k = 3
    m = 1
    l = {1, 2, 3, 5}
    if nth == 1:
        return m
    while nth > 1:
        m = min(l)
        l.remove(m)
        l.add(m * 2)
        l.add(m * 3)
        l.add(m * 5)
        # print('=======')
        # print('m*2=', m * 2, '; m*3= ', m * 3, '; m*5=', m * 5)
        # print('m = ', m)
        # print('nth = ', nth)
        # print('l = ', sorted(l))
        # print('k = ', k)
        nth = nth - 1
    return min(l)


def hamming2(nth):
    hams = []
    # 0 => 2, 1 => 3, 2 => 5
    l = [1, 1, 1]
    abc = [0, 0, 0]
    k = 1
    while nth >= 1:
        hams.append(min(l))
        if hams[-1] == l[0]:
            l[0] = hams[abc[0]] * 2
            abc[0] = abc[0] + 1

        if hams[-1] == l[1]:
            l[1] = hams[abc[1]] * 3
            abc[1] = abc[1] + 1

        if hams[-1] == l[2]:
            l[2] = hams[abc[2]] * 5
            abc[2] = abc[2] + 1

        print('l= ', l, '; abc= ', abc)
        print('first ',k,' hammings= ', hams)
        k = k + 1
        nth = nth - 1
    return hams[-1]


# the winner
print('hamming2(19) = ', hamming2(19))
