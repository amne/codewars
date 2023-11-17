# "abCdE" -> "A-Bb-Ccc-Dddd-Eeeee" .. ez
def accum(s):
    k = 0
    r = []
    while s:
        r.append(s[0].upper() + (s[0].lower() * k))
        k = k + 1
        s = s[1:]
    return "-".join(r)


print(accum("AbcDe"))