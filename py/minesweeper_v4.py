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
    def zeros(mine_map, solved_zeros):
        zerocells = set()
        rlx = range(len(mine_map))
        rly = range(len(mine_map[0]))
        for x in rlx:
            for y in rly:
                if (x, y) in solved_zeros:
                    continue
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
    def plant_mine(mine_map, x, y):
        around = MapHelper.known_around(mine_map, x, y)
        for cell in around:
            if mine_map[cell[0]][cell[1]] - 1 < 0:
                return False

        for cell in around:
            if mine_map[cell[0]][cell[1]] < 9:
                mine_map[cell[0]][cell[1]] = mine_map[cell[0]][cell[1]] - 1
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
    def open_around_zeros(mine_map, solved_zeros):
        # open around zeros
        opening = True
        while opening:
            zeros = MapHelper.zeros(mine_map, solved_zeros)
            arround_zeros = []
            for z in zeros:
                for u in MapHelper.unknown_around2(mine_map, z[0], z[1]):
                    arround_zeros.append(u)
            if len(arround_zeros) == 0:
                solved_zeros = solved_zeros.union(zeros)
                opening = False
                continue

            for uaz in set(arround_zeros):
                mine_map[uaz[0]][uaz[1]] = open(uaz[0], uaz[1]) - MapHelper.count_mines_around(mine_map, uaz[0], uaz[1])
        return solved_zeros

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
    def genseq(length, n):
        # sequences = []
        idx = 2 ** n - 1
        while idx <= (2 ** length) - 1:
            b = bin(idx)
            # l = [int(b) for b in list(bin(idx))[2:]]
            if b.count('1') == n:
                # sequences.append(list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx)))))
                yield list(map(lambda b: int(b), list(('{:0=' + str(length) + 'b}').format(idx))))
                # yield [0] * (length - len(l)) + l

            idx = idx + 1
        return None
        # return sequences

    @staticmethod
    def find_safe_squares(seqs, mine_map):
        # print("trying mines on partial map")
        # MapHelper.print_map(mine_map)
        solved_maps = []
        unknowns = MapHelper.unknowns(mine_map)
        horizon = set()
        isolated_unknowns = []
        for a in unknowns:
            ka = MapHelper.known_around(mine_map, a[0], a[1])
            if len(ka) == 0:
                isolated_unknowns.append(1)
            else:
                isolated_unknowns.append(0)
                [horizon.add(k) for k in ka]

        # isolated_unknowns = [int(len(MapHelper.unknown_around(mine_map, a[0], a[1])) == len(MapHelper.all_around(mine_map, a[0], a[1]))) for a in unknowns]
        # isolated_unknowns = [int(MapHelper.is_isolated(mine_map, a[0], a[1])) for a in unknowns]
        si = -1
        visited_seq = []
        solved_seq = []
        unsafe_squares = [0] * len(unknowns)
        rls = range(len(unknowns))
        for s in seqs:
            si = si + 1
            s2 = tuple((int(s[mi] and not isolated_unknowns[mi])) for mi in rls)
            if s2 in visited_seq:
                continue
            visited_seq.append(s2)
            scratch_map = MapHelper.clone_map(mine_map)
            map_good = True
            for mi in rls:
                if isolated_unknowns[mi]:
                    continue
                if s[mi] and not MapHelper.plant_mine(scratch_map, unknowns[mi][0], unknowns[mi][1]):
                    map_good = False
                    break
            if not map_good:
                continue
            # is map solved v2
            if len(list(filter(lambda h: scratch_map[h[0]][h[1]] != 0 and scratch_map[h[0]][h[1]] != 9, horizon))) > 0:
                continue
            # if not MapHelper.map_solved(scratch_map):
            #    continue

            # print("hmm. solved something: ")
            # print("s2=", s2)
            # print("sum(s2)=", sum(s2))
            # print("solved_map candidate=")
            # MapHelper.print_map(scratch_map)
            for c in rls:
                unsafe_squares[c] = s[c] or unsafe_squares[c]

        safe_squares = []
        for ui in rls:
            if unsafe_squares[ui] or isolated_unknowns[ui]:
                continue
            safe_squares.append(unknowns[ui])

        return safe_squares


def solve_mine(mine_map, n):
    mine_map = MapHelper.map_to_list(mine_map)
    print("start map")
    MapHelper.print_map(mine_map)

    solving = True

    solved_zeros = set()
    if len(mine_map) * len(mine_map[0]) < 2:
        mine_map = [[0]]
        solving = False
    t = time.time()
    while solving:
        if time.time() - t > 10:
            MapHelper.print_map(mine_map)
            return '?'
        solved_zeros = MapHelper.open_around_zeros(mine_map, solved_zeros)

        c1 = Heuristics.pattern_first_corner_one(mine_map)
        # MapHelper.print_map(mine_map)

        planted_mines = False
        for c in c1:
            planted_mines = True
            MapHelper.plant_mine(mine_map, c[0], c[1])

        if planted_mines:
            continue

        unknowns = MapHelper.unknowns(mine_map)
        if len(unknowns):
            seq = Bruteforce.genseq(len(unknowns), n - MapHelper.count_mines(mine_map))
            safe_squares = Bruteforce.find_safe_squares(seq, mine_map)
            if len(safe_squares):
                for ss in safe_squares:
                    mine_map[ss[0]][ss[1]] = open(ss[0], ss[1]) - MapHelper.count_mines_around(mine_map, ss[0], ss[1])
            else:
                if len(unknowns) == n:
                    for u in unknowns:
                        MapHelper.plant_mine(mine_map, u[0], u[1])
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

map_index = 4
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
