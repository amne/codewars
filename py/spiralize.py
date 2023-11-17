"""
5
00000
....0
000.0
0...0
00000

6
000000
.....0
0000.0
0..0.0
0....0
000000

7
0000000
......0
00000.0
0...0.0
0.000.0
0.....0
0000000

8
00000000
.......0
000000.0
0....0.0
0.0..0.0
0.0000.0
0......0
00000000

9
000000000
........0
0000000.0
0.....0.0
0.000.0.0
0.0...0.0
0.00000.0
0.......0
000000000

10
0000000000
.........0
00000000.0
0......0.0
0.0000.0.0
0.0..0.0.0
0.0....0.0
0.000000.0
0........0
0000000000
"""

def seed5():
    return [
        "11111",
        "00001",
        "11101",
        "10001",
        "11111",
    ]

def seed6():
    return [
        "111111",
        "000001",
        "111101",
        "100101",
        "100001",
        "111111",

    ]


def seed_180(seed):
    seed.reverse()
    return [s[::-1] for s in seed]


def grow_spiral(size):
    if size == 5:
        return seed5()
    if size == 6:
        return seed6()
    seed = seed_180(grow_spiral(size - 2))
    spiral = [""] * size
    spiral[0] = "1" * size
    spiral[1] = "0" * (size - 1) + "1"
    for k in range(2, size - 1):
        spiral[k] = seed[k - 2] + "01"
    spiral[size - 1] = "1" * size

    return spiral


def spiralize(size):
    return [[int(c) for c in s] for s in grow_spiral(size)]


[print(" ".join([str(c) for c in l])) for l in spiralize(10)]
