import cProfile
import time


class Solved:
    def __init__(self, solved_map):
        self.solved_map = MapHelper.map_to_list(solved_map)

    def open(self, x, y):
        if MapHelper.num_to_char(self.solved_map[x][y]) == 'x':
            raise ValueError("oops at %d, %d" % (x, y))
        return self.solved_map[x][y]


class MapHelper:
    @staticmethod
    def char_to_num(c):
        charmap = {v: k for k, v in
                   {10: '?', 9: 'x', 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}.items()}
        return charmap[c]

    @staticmethod
    def num_to_char(c):
        charmap = {10: '?', 9: 'x', 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', None: '.'}
        return charmap[c]

    @staticmethod
    def map_to_list(gamemap):
        result = []
        for l in gamemap.split("\n"):
            line = []
            for c in l.split(" "):
                line.append(MapHelper.char_to_num(c))
            result.append(line)
        return result

    @staticmethod
    def count_mines(minemap):
        minecount = 0
        for l in minemap:
            for c in l:
                if c == 9:
                    minecount = minecount + 1
        return minecount

    @staticmethod
    def print_map(mine_map):
        print('map:::::::::::::::::::')
        print("\n".join(map(lambda b: ' '.join(map(lambda c: MapHelper.num_to_char(c), b)), mine_map)))

    @staticmethod
    def zeros(mine_map):
        zerocells = set()
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for x in rlx:
            for y in rly:
                if mine_map[x][y] == 0:
                    zerocells.add((x, y))

        return zerocells

    @staticmethod
    def unknowns(mine_map):
        unknowns = []
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for x in rlx:
            for y in rly:
                if mine_map[x][y] == 10:
                    unknowns.append((x, y))

        return unknowns

    @staticmethod
    def mines(mine_map):
        mines = []
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for x in rlx:
            for y in rly:
                if mine_map[x][y] == 9:
                    mines.append((x, y))

        return mines

    # get all 8 surrounding cell positions
    @staticmethod
    def all_around(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return list(filter(lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]), cells))

    @staticmethod
    def count_mines_around(mine_map, x, y):
        return len(list(filter(lambda a: mine_map[a[0]][a[1]] == 9, MapHelper.all_around(mine_map, x, y))))

    @staticmethod
    def known_around(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return list(filter(
            lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]) and mine_map[a[0]][a[1]] < 10,
            cells))

    @staticmethod
    def is_isolated(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return len(list(filter(
            lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]) and mine_map[a[0]][a[1]] < 10,
            cells))) == 0

    @staticmethod
    def unknown_around2(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return list(filter(
            lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]) and mine_map[a[0]][a[1]] == 10,
            cells))

    @staticmethod
    def unknown_around(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return list(filter(
            lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]) and mine_map[a[0]][a[1]] == 10,
            cells))
        # return list(filter(lambda a: mine_map[a[0]][a[1]] == 10, MapHelper.all_around(mine_map, x, y)))

    @staticmethod
    def plant_mine(mine_map, x, y, zeros):
        around = MapHelper.known_around(mine_map, x, y)
        for cell in around:
            if mine_map[cell[0]][cell[1]] - 1 < 0:
                return False

        for cell in around:
            if 0 < mine_map[cell[0]][cell[1]] < 9:
                mine_map[cell[0]][cell[1]] = mine_map[cell[0]][cell[1]] - 1
                if mine_map[cell[0]][cell[1]] == 0:
                    zeros.add((cell[0], cell[1]))
                if mine_map[cell[0]][cell[1]] < 0:
                    print(
                        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    MapHelper.print_map(mine_map)

        mine_map[x][y] = 9

        return mine_map

    @staticmethod
    def map_solved(mine_map):
        # map is partially solved if scratch map has only None, 0, 9, or 10
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for i in rlx:
            for j in rly:
                if mine_map[i][j] >= 9 or mine_map[i][j] == 0:
                    continue
                return False
        return True

    @staticmethod
    def open_around_zeros(mine_map, zeros):
        # open around zeros
        while len(zeros):
            arround_zeros = []
            for z in zeros:
                for u in MapHelper.unknown_around2(mine_map, z[0], z[1]):
                    arround_zeros.append(u)
            zeros = set()
            #if len(arround_zeros) == 0:
            #    solved_zeros = solved_zeros.union(zeros)
            #    opening = False
            #    continue

            for uaz in set(arround_zeros):
                c = open(uaz[0], uaz[1]) - MapHelper.count_mines_around(mine_map, uaz[0], uaz[1])
                if c == 0:
                    zeros.add((uaz[0], uaz[1]))
                mine_map[uaz[0]][uaz[1]] = c

        return None

    @staticmethod
    def clone_map(mine_map):
        return [l[:] for l in mine_map]

    @staticmethod
    def map_from_mines(mine_map, map_mines):
        lx = len(mine_map)
        ly = len(mine_map[0])
        rlx = range(lx)
        rly = range(ly)
        empty_map = [[0] * ly for _ in rlx]
        for m in map_mines:
            empty_map[m[0]][m[1]] = 9
        for x in rlx:
            for y in rly:
                if empty_map[x][y] == 0:
                    empty_map[x][y] = open(x, y)

            # around = MapHelper.all_around(empty_map, m[0], m[1])
            # for a in around:
            #     if empty_map[a[0]][a[1]] < 8:
            #         empty_map[a[0]][a[1]] = empty_map[a[0]][a[1]] + 1

        return empty_map


class Heuristics:
    @staticmethod
    def pattern_first_corner_one(mine_map):
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for l in rlx:
            for c in rly:
                if mine_map[l][c] == 1:
                    ua = MapHelper.unknown_around(mine_map, l, c)
                    if len(ua) == 1:
                        yield ua[0]
        return False

    @staticmethod
    def count_hints(mine_map, x, y):
        all_round = MapHelper.known_around(mine_map, x, y)
        ones = []
        # if len(all) == 8:
        sums = [0] * 9
        for a in all_round:
            cell = mine_map[a[0]][a[1]]
            if 1 <= cell <= 8:
                sums[cell] = sums[cell] + 1

        return sums

    @staticmethod
    def enrich_count_ones(mine_map, cells):
        enriched = []
        for c in cells:
            counts = Heuristics.count_hints(mine_map, c[0], c[1])
            score = counts[1]
            if score > 3:
                enriched.append((c[0], c[1], score))
        enriched = list(set(enriched))
        enriched.sort(key=lambda a: a[2])

        return enriched


class Bruteforce:
    @staticmethod
    # generate sequence of given length with n 1s inside it
    def genseq2(length, n0, n):
        sequences = []
        idx = 2**n0 - 1
        while idx <= (2 ** length) - 1:
            b = bin(idx)
            # l = [int(b) for b in list(bin(idx))[2:]]
            if b.count('1') <= n:
                sequences.append(list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx)))))
                # yield list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx))))
                # yield [0] * (length - len(l)) + l

            idx = idx + 1
        # return None
        return sequences

    @staticmethod
    # generate sequence of given length with n 1s inside it
    def genseq(length, n):
        sequences = []
        idx = 2 ** n - 1
        while idx <= (2 ** length) - 1:
            b = bin(idx)
            # l = [int(b) for b in list(bin(idx))[2:]]
            if b.count('1') == n:
                sequences.append(list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx)))))
                # yield list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx))))
                # yield [0] * (length - len(l)) + l

            idx = idx + 1
        # return None
        return sequences

    @staticmethod
    def find_safe_squares(mine_map, unknowns, n):
        # print("trying mines on partial map")
        # MapHelper.print_map(mine_map)

        horizon = set()
        edge = set()
        for a in unknowns:
            ka = MapHelper.known_around(mine_map, a[0], a[1])
            if len(ka) > 0:
                [horizon.add(k) for k in ka]
                edge.add(a)

        edge = list(edge)
        mines_left = n - MapHelper.count_mines(mine_map)
        min_edge_mines = max(0, mines_left - (len(unknowns) - len(edge)))
        seqs2 = Bruteforce.genseq2(len(edge), min_edge_mines, mines_left)

        si = -1
        unsafe_squares = [0] * len(edge)
        rle = range(len(edge))
        for s in seqs2:
            zeros = set()
            si = si + 1
            scratch_map = MapHelper.clone_map(mine_map)
            map_good = True
            for mi in rle:
                if s[mi]:
                    if not MapHelper.plant_mine(scratch_map, edge[mi][0], edge[mi][1], zeros):
                        map_good = False
                        break
            if not map_good:
                continue
            # is map solved v2
            if len(list(filter(lambda h: scratch_map[h[0]][h[1]] != 0 and scratch_map[h[0]][h[1]] != 9, horizon))) > 0:
                continue
            for c in rle:
                unsafe_squares[c] = s[c] or unsafe_squares[c]
            # there is no safe square to open for sure on the next step
            if sum(unsafe_squares) == len(unsafe_squares):
                return []

        safe_squares = []
        for ui in rle:
            if unsafe_squares[ui]:
                continue
            safe_squares.append(edge[ui])

        return safe_squares


def solve_mine(mine_map, n):
    mine_map = MapHelper.map_to_list(mine_map)
    # print("start map")
    # MapHelper.print_map(mine_map)

    solving = True

    solved_zeros = set()
    if len(mine_map) * len(mine_map[0]) < 2:
        if n:
            mine_map = [[9]]
        else:
            mine_map = [[0]]
        solving = False
    zeros = MapHelper.zeros(mine_map)
    while solving:
        MapHelper.open_around_zeros(mine_map, zeros)
        zeros = set()

        c1 = Heuristics.pattern_first_corner_one(mine_map)
        # MapHelper.print_map(mine_map)

        planted_mines = False
        for c in c1:
            planted_mines = True
            MapHelper.plant_mine(mine_map, c[0], c[1], zeros)

        if planted_mines:
            continue

        unknowns = MapHelper.unknowns(mine_map)
        if len(unknowns):

            safe_squares = Bruteforce.find_safe_squares(mine_map, unknowns, n)
            if len(safe_squares):
                for ss in safe_squares:
                    c = open(ss[0], ss[1]) - MapHelper.count_mines_around(mine_map, ss[0], ss[1])
                    if c == 0:
                        zeros.add((ss[0], ss[1]))
                    mine_map[ss[0]][ss[1]] = c
            else:
                if len(unknowns) == n - MapHelper.count_mines(mine_map):
                    for u in unknowns:
                        MapHelper.plant_mine(mine_map, u[0], u[1], zeros)
                solving = False
        else:
            solving = False

    map_mines = MapHelper.mines(mine_map)
    if len(map_mines) != n:
        return '?'

    solved_map = MapHelper.map_from_mines(mine_map, map_mines)
    solved_map_str = "\n".join(map(lambda b: ' '.join(map(lambda c: MapHelper.num_to_char(c), b)), solved_map))
    return solved_map_str


gamemap = []
solvedmap = []

# 0
gamemap.append("""
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip())

solvedmap.append("""
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip())

# 1
gamemap.append("""
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
""".strip())

solvedmap.append("""
1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
""".strip())

# 2
gamemap.append("""
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? 0 ? ? ?
0 0 0 0 0 0 0 0 ? ? ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? ? ? ? ?
0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 ? ? ? ? ? ? 0
? ? 0 0 0 ? ? ? 0 ? ? ? ? 0 0 ? ? ? ? ? ?
? ? 0 0 0 ? ? ? 0 ? ? ? 0 0 0 ? ? ? ? ? ?
? ? ? 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 ? ? ?
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
? ? ? 0 0 0 0 0 0 0 ? ? ? ? 0 0 ? ? ? 0 0
""".strip())

solvedmap.append("""
0 0 0 0 0 0 0 0 1 x x 2 1 0 1 x 1 0 1 2 x
0 0 0 0 0 0 0 0 1 2 3 x 1 0 2 2 2 1 2 x 2
0 0 0 0 0 0 0 0 0 0 2 2 2 0 1 x 1 1 x 2 1
0 0 0 0 0 1 1 1 0 0 1 x 1 0 1 2 2 2 1 1 0
1 1 0 0 0 1 x 1 0 1 2 2 1 0 0 1 x 1 1 1 1
x 1 0 0 0 1 1 1 0 1 x 1 0 0 0 1 1 1 1 x 1
2 2 1 0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 1 1 1
1 x 1 0 0 0 0 0 0 0 1 2 2 1 0 0 1 1 1 0 0
1 1 1 0 0 0 0 0 0 0 1 x x 1 0 0 1 x 1 0 0
""".strip())

# 3
gamemap.append("""
0 ? ?
0 ? ?
""".strip())

solvedmap.append("""
0 2 x
0 2 x
""".strip())

# 4
gamemap.append("""
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 0
""".strip())

solvedmap.append("""
0 0 0 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0 2 x 2 1 x 1 0
1 1 1 0 0 0 0 1 1 1 0 0 0 0 1 1 2 x 1 0 0 0 0 2 x 2 1 1 1 0
1 x 1 1 1 1 0 1 x 2 1 1 0 0 1 x 2 1 1 0 0 0 0 1 1 1 0 0 0 0
1 2 2 3 x 2 0 1 1 2 x 1 0 0 1 2 2 1 0 0 0 0 0 1 1 1 0 0 1 1
0 1 x 3 x 2 0 0 0 1 1 1 0 1 2 3 x 1 0 0 0 0 0 1 x 1 0 0 1 x
0 1 1 3 3 3 2 1 1 1 1 2 1 2 x x 2 2 1 1 0 0 0 1 1 1 1 1 2 1
0 0 0 1 x x 2 x 1 1 x 2 x 2 3 3 3 2 x 1 0 1 1 1 0 0 2 x 2 0
0 1 1 2 2 2 3 2 2 1 1 2 1 1 1 x 2 x 2 1 0 1 x 1 0 0 2 x 2 0
1 2 x 1 0 1 2 x 1 0 0 0 1 1 2 2 3 2 1 0 0 1 1 1 0 0 1 1 1 0
1 x 2 1 0 1 x 3 2 1 0 0 1 x 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 0
1 1 2 1 2 2 2 2 x 1 0 0 1 1 1 1 2 x 1 0 0 0 1 x 2 1 0 0 0 0
1 1 2 x 2 x 1 1 1 1 0 0 0 0 1 1 2 1 1 0 0 0 1 2 x 1 0 0 0 0
1 x 3 2 2 1 1 0 0 1 1 1 0 0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0
1 2 x 1 0 0 0 0 0 1 x 1 0 0 1 1 1 0 0 0 0 0 1 x 1 0 0 0 0 0
""".strip())

# 5
gamemap.append("""
0 ? ?
0 ? ?
""".strip())

solvedmap.append("""
0 1 x
0 1 1
""".strip())

# 6
gamemap.append("""
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 ? ? ? ? ? ? 0
0 0 0 0 0 0 0 0 0 0 0 0 ? ? ? 0 ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? 0 0 0 0 ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? ? ? ? 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? 0 0 0 0 ? ? ? 0 0 0 0
? ? ? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ?
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ?
0 0 0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
0 ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? ? 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? 0 0 0 ? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0
? ? ? ? 0 ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? 0 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? ? ? ? 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? ? 0 0 0 0
? ? ? ? 0 0 0 0 0 ? ? ? 0 0 ? ? ? 0 0 0 0 0 ? ? ? 0 0 0 0 0
""".strip())

solvedmap.append("""
0 0 0 0 0 0 0 0 0 0 0 0 1 x 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 0 0 0 0 2 x 2 1 x 1 0
1 1 1 0 0 0 0 1 1 1 0 0 0 0 1 1 2 x 1 0 0 0 0 2 x 2 1 1 1 0
1 x 1 1 1 1 0 1 x 2 1 1 0 0 1 x 2 1 1 0 0 0 0 1 1 1 0 0 0 0
1 2 2 3 x 2 0 1 1 2 x 1 0 0 1 2 2 1 0 0 0 0 0 1 1 1 0 0 1 1
0 1 x 3 x 2 0 0 0 1 1 1 0 1 2 3 x 1 0 0 0 0 0 1 x 1 0 0 1 x
0 1 1 3 3 3 2 1 1 1 1 2 1 2 x x 2 2 1 1 0 0 0 1 1 1 1 1 2 1
0 0 0 1 x x 2 x 1 1 x 2 x 2 3 3 3 2 x 1 0 1 1 1 0 0 2 x 2 0
0 1 1 2 2 2 3 2 2 1 1 2 1 1 1 x 2 x 2 1 0 1 x 1 0 0 2 x 2 0
1 2 x 1 0 1 2 x 1 0 0 0 1 1 2 2 3 2 1 0 0 1 1 1 0 0 1 1 1 0
1 x 2 1 0 1 x 3 2 1 0 0 1 x 1 1 x 2 1 0 0 0 1 1 1 0 0 0 0 0
1 1 2 1 2 2 2 2 x 1 0 0 1 1 1 1 2 x 1 0 0 0 1 x 2 1 0 0 0 0
1 1 2 x 2 x 1 1 1 1 0 0 0 0 1 1 2 1 1 0 0 0 1 2 x 1 0 0 0 0
1 x 3 2 2 1 1 0 0 1 1 1 0 0 1 x 1 0 0 0 0 0 1 2 2 1 0 0 0 0
1 2 x 1 0 0 0 0 0 1 x 1 0 0 1 1 1 0 0 0 0 0 1 x 1 0 0 0 0 0
""".strip())

# 7
gamemap.append("""
?
""".strip())

solvedmap.append("""
0
""".strip())

# 8
gamemap.append("""
0 0 0 0 0 0
0 ? ? ? 0 0
? ? ? ? 0 0
? ? ? ? 0 0
? ? ? ? ? 0
? ? ? ? ? 0
? ? ? ? ? 0
? ? ? 1 0 0
""".strip())

solvedmap.append("""
0 0 0 0 0 0
0 1 1 1 0 0
1 2 x 1 0 0
1 x 2 1 0 0
1 1 2 1 1 0
1 1 2 x 1 0
1 x 3 2 1 0
1 2 x 1 0 0
""".strip())

# 9
gamemap.append("""
0 ? ?
0 ? ?
""".strip())

solvedmap.append("""
0 2 x
0 2 x
""".strip())

# 10
gamemap.append("""
0 0 0 0
0 0 0 0
? ? 0 0
? ? ? ?
? ? ? ?
? ? ? ?
? ? 0 0
0 0 0 0
0 0 0 0
0 0 0 0
""".strip())

solvedmap.append("""
0 0 0 0
0 0 0 0
1 1 0 0
x 2 1 1
x 3 1 x
x 2 1 1
1 1 0 0
0 0 0 0
0 0 0 0
0 0 0 0
""".strip())

# 11
gamemap.append("""
0 0 0 0 0 0 0 0 0 0 0
0 0 0 ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? ? 0 0
0 0 ? ? ? ? ? ? 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip())

solvedmap.append("""
0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 3 3 2 1 0 0
0 0 1 3 x x x x 1 0 0
0 0 2 x x x x 5 2 0 0
0 0 3 x x x x x 2 0 0
0 0 3 x x x x x 2 0 0
0 0 2 x x x x 3 1 0 0
0 0 1 2 3 3 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0
""".strip())

map_index = 11
solved_helper = Solved(solved_map=solvedmap[map_index])
open = solved_helper.open
minecount = MapHelper.count_mines(MapHelper.map_to_list(solvedmap[map_index]))

pr = cProfile.Profile()
pr.enable()
result = solve_mine(gamemap[map_index], minecount)
pr.disable()

pr.print_stats(sort="calls")

# result = solve_mine(gamemap[map_index], minecount)
print("solved")
print(result)
