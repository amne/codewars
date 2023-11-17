class Solved:
    def __init__(self, solved_map):
        self.solved_map = MapHelper.map_to_list(solved_map)

    def open(self, x, y):
        if MapHelper.num_to_char(self.solved_map[x][y]) == 'x':
            raise ValueError("oops at %d, %d" % (x, y))
        return self.solved_map[x][y]


class MapHelper:
    @staticmethod
    def print_map_str(mine_map):
        solved_map_str = "\n".join(map(lambda b: ' '.join(map(lambda c: MapHelper.num_to_char(c), b)), solved_map))

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

        for i in range(len(mine_map)):
            print(list(map(lambda x: MapHelper.num_to_char(x), mine_map[i])))

    @staticmethod
    def zeros(mine_map):
        zerocells = []
        for x in range(len(mine_map)):
            for y in range(len(mine_map[x])):
                if mine_map[x][y] == 0:
                    zerocells.append((x, y))

        return zerocells

    @staticmethod
    def unknowns(mine_map):
        unknowns = []
        for x in range(len(mine_map)):
            for y in range(len(mine_map[x])):
                if mine_map[x][y] == 10:
                    unknowns.append((x, y))

        return unknowns

    @staticmethod
    def mines(mine_map):
        mines = []
        for x in range(len(mine_map)):
            for y in range(len(mine_map[x])):
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
    def unknown_around(mine_map, x, y):
        return list(filter(lambda a: mine_map[a[0]][a[1]] == 10, MapHelper.all_around(mine_map, x, y)))

    @staticmethod
    def plant_mine(mine_map, x, y):
        around = MapHelper.all_around(mine_map, x, y)
        for cell in around:
            if mine_map[cell[0]][cell[1]] is not None and mine_map[cell[0]][cell[1]] - 1 < 0:
                return False

        for cell in around:
            if mine_map[cell[0]][cell[1]] is not None and mine_map[cell[0]][cell[1]] < 9:
                mine_map[cell[0]][cell[1]] = mine_map[cell[0]][cell[1]] - 1
                if mine_map[cell[0]][cell[1]] < 0:
                    print(
                        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    MapHelper.print_map(mine_map)

        mine_map[x][y] = 9

        return mine_map

    @staticmethod
    def open_around_zeros(mine_map):
        # open around zeros

        edge_cells = []
        opening = True
        while opening:
            zeros = MapHelper.zeros(mine_map)
            arround_zeros = []
            for z in zeros:
                for u in MapHelper.unknown_around(mine_map, z[0], z[1]):
                    arround_zeros.append(u)
            if len(arround_zeros) == 0:
                opening = False
                continue

            for uaz in set(arround_zeros):
                if mine_map[uaz[0]][uaz[1]] == 10:
                    mine_map[uaz[0]][uaz[1]] = open(uaz[0], uaz[1]) - MapHelper.count_mines_around(mine_map, uaz[0], uaz[1])
                    edge_cells = edge_cells + MapHelper.unknown_around(mine_map, uaz[0], uaz[1])
        return set(filter(lambda o: mine_map[o[0]][o[1]] == 10, edge_cells))

    @staticmethod
    def clone_map(mine_map):
        return [l[:] for l in mine_map]

    @staticmethod
    def map_from_mines(mine_map, map_mines):
        empty_map = [[0]*len(mine_map[0]) for _ in range(len(mine_map))]
        for m in map_mines:
            empty_map[m[0]][m[1]] = 9
            around = MapHelper.all_around(empty_map, m[0], m[1])
            for a in around:
                if empty_map[a[0]][a[1]] < 8:
                    empty_map[a[0]][a[1]] = empty_map[a[0]][a[1]] + 1

        return empty_map


class Heuristics:

    @staticmethod
    def pattern_first_corner_one(mine_map):
        for l in range(len(mine_map)):
            for c in range(len(mine_map[l])):
                if mine_map[l][c] == 1:
                    ua = MapHelper.unknown_around(mine_map, l, c)
                    if len(ua) == 1:
                        return ua[0]
        return False

    @staticmethod
    def count_hints(mine_map, x, y):
        all_round = MapHelper.all_around(mine_map, x, y)
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
            if score > 4:
                enriched.append((c[0], c[1], score))
        enriched = list(set(enriched))
        enriched.sort(key=lambda a: a[2])

        return enriched

    @staticmethod
    def enrich_score_ones(mine_map, cells):
        higher_than_2 = False
        cell_scores = []
        for c in cells:
            counts = Heuristics.count_hints(mine_map, c[0], c[1])
            score = int("".join(map(lambda d: str(d), counts)))
            if counts[1] + counts[2]*2 > 2:
                higher_than_2 = True
            if score > 0:
                cell_scores.append((c[0], c[1], score))
        cell_scores = list(set(cell_scores))
        cell_scores.sort(key=lambda a: a[2])

        if higher_than_2:
            return cell_scores
        else:
            return []

    @staticmethod
    def score_patterns(mine_map, scored_cells):
        new_scored_cells = scored_cells
        # look for triple matches
        if len(scored_cells) >= 3:
            (a, b, c) = (scored_cells[-1], scored_cells[-2], scored_cells[-3])
            # if top two have the same score
            if a[2] == b[2]:
                a = (a[0], a[1], a[2] + MapHelper.count_mines_around(mine_map, a[0], a[1]))
                b = (b[0], b[1], b[2] + MapHelper.count_mines_around(mine_map, b[0], b[1]))
                c = (c[0], c[1], c[2] + MapHelper.count_mines_around(mine_map, c[0], c[1]))
                # and same column
                if a[1] == b[1] == c[1]:
                    new_scored_cells = [a, b, c]
                    new_scored_cells.sort(key=lambda i: i[0])
                    return [new_scored_cells[1]]
                # or same line
                elif a[0] == b[0] == c[0]:
                    new_scored_cells = [a, b, c]
                    new_scored_cells.sort(key=lambda i: i[1])
                    return [new_scored_cells[1]]
            else:
                if a[1] == b[1] == c[1] or a[0] == b[0] == c[0]:
                    return new_scored_cells
                else:
                    return []

        return new_scored_cells



def solve_mine(mine_map, n):
    mine_map = MapHelper.map_to_list(mine_map)

    print("start map")
    MapHelper.print_map(mine_map)

    solving = True

    while solving:
        cell_scores = []

        edge_cells = MapHelper.open_around_zeros(mine_map)
        c1 = Heuristics.pattern_first_corner_one(mine_map)
        MapHelper.print_map(mine_map)

        if c1:
            MapHelper.plant_mine(mine_map, c1[0], c1[1])
            continue

        if len(edge_cells) > 0:
            cell_scores = Heuristics.enrich_score_ones(mine_map, edge_cells)
        else:
            cell_scores = Heuristics.enrich_score_ones(mine_map, MapHelper.unknowns(mine_map))

        new_cell_scores = Heuristics.score_patterns(mine_map, cell_scores)

        print("edge_cells=", edge_cells)
        print("scored_cells= ", cell_scores)
        print("pattern_scored_cells= ", new_cell_scores)
        if len(new_cell_scores) == 0:
            solving = False
            continue
        o = new_cell_scores.pop()
        print("pop=", o)
        MapHelper.plant_mine(mine_map, o[0], o[1])

    map_mines = MapHelper.mines(mine_map)
    if len(map_mines) != n:
        return '?'

    solved_map = MapHelper.map_from_mines(mine_map, map_mines)

    solved_map_str = "\n".join(map(lambda b: ' '.join(map(lambda c: MapHelper.num_to_char(c), b)), solved_map))

    # print(solved_map_str.strip())
    return solved_map_str


gamemap = []
solvedmap = []

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

gamemap.append("""
0 ? ?
0 ? ?
""".strip())

solvedmap.append("""
0 2 x
0 2 x
""".strip())

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

gamemap.append("""
0 ? ?
0 ? ?
""".strip())

solvedmap.append("""
0 1 x
0 1 1
""".strip())



map_index = 0
solved_helper = Solved(solved_map=solvedmap[map_index])
open = solved_helper.open
minecount = MapHelper.count_mines(MapHelper.map_to_list(solvedmap[map_index]))

result = solve_mine(gamemap[map_index], minecount)
print(result)
