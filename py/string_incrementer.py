def increment_string(strng):
    x = list(strng)
    n = []
    z = []
    i = 1

    # get all the digits
    while len(x) and 48 <= ord(x[-1]) <= 57:
        n.append(x[-1])
        x.pop()
        i = i + 1

    strng = "".join(x)

    # fast case: no digits
    if not len(n):
        return strng + '1'

    # get the leading zeros out of the way
    i = 1
    while len(n) and 48 == ord(n[-1]):
        z.append('0')
        n.pop()
        i = i + 1

    # fast case #2: only zeros. replace last zero with a 1
    if not len(n):
        z[-1] = '1'
        return strng + "".join(z)

    n.reverse()
    num = int("".join(n)) + 1

    # if we added on digit and we have leading zeros take on out
    if len(str(num)) > len(n) and len(z):
        z.pop()

    return strng + "".join(z) + str(num)



tests = [
    ("foo", "foo1"),
    ("foobar001", "foobar002"),
    ("foobar0000000000091", "foobar0000000000092"),
    ("foobar1", "foobar2"),
    ("foobar00", "foobar01"),
    ("foobar99", "foobar100"),
    ("foobar099", "foobar100"),
    ("foobar000000000099", "foobar000000000100"),
    ("", "1")
]

for t in tests:
    print(t[0], "->", increment_string(t[0]), " ; expected=", t[1])