
def bt_():
    k = 0
    p = 6
    m = 1
    n = 19
    s = [-1] * n
    c = 0
    while k >= 0:
        s[k] = s[k] + 1
        bits = len(list(filter(lambda b: b == 1, s[:k+1])))
        if s[k] > m or bits > p:
            k = k - 1
            continue
        if k == n - 1:
            if bits == p:
                c = c + 1
                print(c, s)
            continue
        else:
            k = k + 1
            s[k] = -1

def bit_bt_():
    n = 3
    p = 1
    idx = 2 ** p - 1
    c = 0
    while idx < 2 ** n:
        if bin(idx).count('1') == p:
            c = c + 1
            # seq = list(map(lambda b: int(b), list(('{:0='+ str(n) + 'b}').format(idx))[::-1]))
            seq = list(map(lambda b: int(b), list(bin(idx)[2:].zfill(n))[::-1]))
            print(c, seq)
        idx = idx + 1

bit_bt_()