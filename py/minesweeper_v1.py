def char_to_num(c):
    charmap = {v: k for k, v in
               {10: '?', 9: 'x', 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}.items()}
    return charmap[c]

def num_to_char(c):
    charmap = {10: '?', 9: 'x', 0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', None: '.'}
    return charmap[c]

def map_to_list(gamemap):
    result = []
    for l in gamemap.split("\n"):
        line = []
        for c in l.split(" "):
            line.append(char_to_num(c))
        result.append(line)
    return result


class Solved:
    def __init__(self, solved_map):
        self.solved_map = map_to_list(solved_map)

    def open(self, x, y):
        if num_to_char(self.solved_map[x][y]) == 'x':
            raise ValueError
        return num_to_char(self.solved_map[x][y])


def solve_mine(mine_map, n):
    # coding and coding...
    solved = Solved(solved_map=solvedmap)

    mine_map = map_to_list(mine_map)

    # find first zero cell and open everything around it
    def first_zero(mine_map):
        for i in range(len(mine_map)):
            for j in range(len(mine_map[i])):
                if mine_map[i][j] == 0:
                    return i, j

        return None, None

    # get all 8 surrounding cells
    def all_around(mine_map, x, y):
        cells = [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
                 (x, y - 1), (x, y + 1),
                 (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)]

        return list(filter(lambda a: 0 <= a[0] < len(mine_map) and 0 <= a[1] < len(mine_map[a[0]]), cells))

    def count_mines_around(mine_map, x, y):
        return len(list(filter(lambda a: mine_map[a[0]][a[1]] == 9, all_around(mine_map, x, y))))

    # get up to eight unknown surrounding cells
    # start top-left
    def unknown_around(mine_map, x, y):
        return list(filter(lambda a: mine_map[a[0]][a[1]] == 10, all_around(mine_map, x, y)))

    # remove mine = increase adjacent mine count and mark mine as unknown
    def remove_mine(mine_map, x, y):
        around = all_around(mine_map, x, y)

        for cell in around:
            if mine_map[cell[0]][cell[1]] is not None and mine_map[cell[0]][cell[1]] < 9:
                mine_map[cell[0]][cell[1]] = mine_map[cell[0]][cell[1]] + 1

        mine_map[x][y] = 10

        return mine_map

    # plant mine = decrease adjacent mine count and return true; return false if no decrease
    def plant_mine(mine_map, x ,y):
        around = all_around(mine_map, x, y)
        for cell in around:
            if mine_map[cell[0]][cell[1]] is not None and mine_map[cell[0]][cell[1]] - 1 < 0:
                return False

        for cell in around:
            if mine_map[cell[0]][cell[1]] is not None and mine_map[cell[0]][cell[1]] < 9:
                mine_map[cell[0]][cell[1]] = mine_map[cell[0]][cell[1]] - 1

        mine_map[x][y] = 9

        return mine_map


    def unknown_cells(mine_map):
        unk = []
        for i in range(len(mine_map)):
            for j in range(len(mine_map[i])):
                if mine_map[i][j] == 10:
                    unk.append((i, j))
        return unk

    def print_map(mine_map):
        print('map:::::::::::::::::::')

        for i in range(len(mine_map)):
            print(list(map(lambda x: num_to_char(x), mine_map[i])))

    # print_map(mine_map)



    def bin_gen_seq(count_unknown, count_mines):
        # sequences = []
        idx = 2 ** count_mines - 1
        while idx <= 2 ** count_unknown:
            if bin(idx).count('1') == count_mines:
                # sequences.append()
                yield list(map(lambda b: int(b), list(('{:0=' + str(count_unknown) + 'b}').format(idx))))
            idx = idx + 1
        return None

    def compare_map(map_a, map_b):
        # maps are equal if all cells that are < 9 on both maps are also equal
        for i in range(len(map_a)):
            for j in range(len(map_a[i])):
                if (map_a[i][j] is None) or (map_b[i][j] is None) or map_a[i][j] >= 9 or map_b[i][j] >= 9 or map_a[i][j] == 0 or map_b[i][j] == 0:
                    continue
                if map_a[i][j] != map_b[i][j]:
                    return False
        return True

    def map_partially_solved(map_candidate):
        # map is partially solved if scratch map has only None, 0, 9, or 10
        for i in range(len(map_candidate)):
            for j in range(len(map_candidate[i])):
                if (map_candidate[i][j] is None) or map_candidate[i][j] >= 9 or map_candidate[i][j] == 0:
                    continue
                return False
        return True

    def calc_hints(solved_map):
        for i in range(len(solved_map)):
            for j in range(len(solved_map[i])):
                if solved_map[i][j] is None:
                    solved_map[i][j] = 0
                if solved_map[i][j] != 9:
                    continue

                cells = all_around(solved_map, i, j)
                for cell in cells:
                    if solved_map[cell[0]][cell[1]] == 9:
                        continue
                    if solved_map[cell[0]][cell[1]] is None or solved_map[cell[0]][cell[1]] == 10:
                        solved_map[cell[0]][cell[1]] = 0
                    solved_map[cell[0]][cell[1]] = solved_map[cell[0]][cell[1]] + 1

    def isolated_mines(map_candidate):
        iso_list = []
        for i in range(len(map_candidate)):
            for j in range(len(map_candidate[i])):
                if map_candidate[i][j] == 9:
                    cells = all_around(map_candidate, i, j)
                    is_iso = True
                    for cell in cells:
                        if map_candidate[cell[0]][cell[1]] is None or map_candidate[cell[0]][cell[1]] < 9:
                            is_iso = False
                            break
                    if is_iso:
                        iso_list.append((i, j))
        return iso_list

    # doubt mines if it has less than 4 zeros around it
    def doubt_mines(map_candidate):
        doubt_list = []
        for i in range(len(map_candidate)):
            for j in range(len(map_candidate[i])):
                if map_candidate[i][j] == 9:
                    cells = all_around(map_candidate, i, j)
                    count_zero = 0
                    count_mines = 0
                    for cell in cells:
                        if map_candidate[cell[0]][cell[1]] == 0:
                            count_zero = count_zero + 1
                        if map_candidate[cell[0]][cell[1]] == 9:
                            count_mines = count_mines + 1
                    if count_zero + count_mines < 4:
                        doubt_list.append((i, j))
        return doubt_list

    is_solved = False
    solved_map = None

    # start solve
    # open all zeros
    # bruteforce mines until all digits become zeros
    # mark mines
    # count isolated mines and set as new max_mines
    # stop when isolated mines = 0 or all sequences are processed
    ideal_seq = [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0]

    while not is_solved:
        is_solved = True

        zx, zy = first_zero(mine_map)
        while zx != None and zy != None:
            cells = unknown_around(mine_map, zx, zy)
            for c in cells:
                mine_map[c[0]][c[1]] = char_to_num(solved.open(c[0], c[1])) - count_mines_around(mine_map, c[0], c[1])
            mine_map[zx][zy] = None
            zx, zy = first_zero(mine_map)
        loose = unknown_cells(mine_map)
        # print(loose)
        ii = 0
        for seq in bin_gen_seq(len(loose), n):
            ii = ii + 1
            scratch_map = [l[:] for l in mine_map]
            map_good = True
            for i in range(len(seq)):
                if seq[i]:
                    flagged = loose[i]
                    if not plant_mine(scratch_map, flagged[0], flagged[1]):
                        map_good = False
                        break
            if map_good:
                if map_partially_solved(scratch_map):
                    # print_map(mine_map)
                    # print_map(scratch_map)
                    iso_mines = isolated_mines(scratch_map)
                    if len(iso_mines) != 0:
                        not_mines = doubt_mines(scratch_map)
                        for not_mine in not_mines:
                            remove_mine(scratch_map, not_mine[0], not_mine[1])
                        n = len(not_mines)
                        mine_map = [l[:] for l in scratch_map]
                        is_solved = False
                        break
                    calc_hints(scratch_map)
                    if len(unknown_cells(scratch_map)) > 0:
                        is_solved = False
                    else:
                        solved_map = scratch_map
                        break

    if solved_map is None:
        return '?'
    solved_map_str = "\n".join(map(lambda b: ' '.join(map(lambda c: num_to_char(c), b)), solved_map))

    return solved_map_str



gamemap = """
? ? ? ? ? ?
? ? ? ? ? ?
? ? ? 0 ? ?
? ? ? ? ? ?
? ? ? ? ? ?
0 0 0 ? ? ?
""".strip()

solvedmap = """
1 x 1 1 x 1
2 2 2 1 2 2
2 x 2 0 1 x
2 x 2 1 2 2
1 1 1 1 x 1
0 0 0 1 1 1
""".strip()

# gamemap = """
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? 0
# ? ? 0 ? ? ? 0 0 ? ? ? 0 0 0 0 ? ? ? ?
# ? ? 0 ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? ?
# 0 ? ? ? ? ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 0 0
# 0 ? ? ? 0 0 0 ? ? ? 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? 0 ? ? ? 0 ? ? ? ? 0 0 0 0 0
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 ? ? ? 0
# 0 0 ? ? ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 ? ? ? ? ? ? ? 0 0 0 0 ? ? ? 0
# 0 0 0 0 0 ? ? ? ? ? ? 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? 0 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ? ?
# 0 0 ? ? ? ? ? ? ? ? 0 0 0 0 0 0 0 ? ?
# 0 0 0 0 0 0 ? ? ? ? 0 0 0 ? ? ? 0 ? ?
# 0 0 0 ? ? ? ? ? ? ? 0 0 0 ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? ? ? ? ? ?
# 0 0 0 ? ? ? ? ? 0 0 0 ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# 0 0 0 0 ? ? ? ? ? ? ? ? ? ? 0 ? ? ? ?
# """.strip()
#
# solvedmap = """
# 1 1 0 1 1 1 0 0 1 1 1 0 0 0 0 1 1 1 0
# x 1 0 1 x 1 0 0 2 x 2 0 0 0 0 1 x 2 1
# 1 1 0 2 3 3 1 1 3 x 2 0 0 0 0 1 2 x 1
# 0 1 1 2 x x 1 2 x 3 1 0 0 0 0 0 1 1 1
# 0 1 x 2 2 2 1 3 x 3 0 0 0 0 0 0 0 0 0
# 0 1 1 1 0 0 0 2 x 2 0 0 0 0 0 0 0 0 0
# 0 0 0 0 0 0 0 1 1 1 1 2 2 1 0 0 0 0 0
# 0 0 0 0 0 0 0 0 0 0 1 x x 1 0 0 0 0 0
# 0 0 1 1 1 0 1 1 1 0 1 2 2 1 0 0 0 0 0
# 0 0 1 x 2 1 3 x 2 0 0 0 0 0 0 1 1 1 0
# 0 0 1 1 2 x 3 x 3 1 1 0 0 0 0 1 x 1 0
# 0 0 0 0 1 2 3 2 2 x 1 0 0 0 0 1 1 1 0
# 0 0 0 0 0 1 x 1 1 1 1 0 0 0 0 0 1 1 1
# 0 0 1 1 2 2 2 1 0 0 0 0 0 0 0 0 1 x 1
# 0 0 1 x 2 x 2 1 1 0 0 0 0 0 0 0 1 1 1
# 0 0 1 1 2 1 3 x 3 1 0 0 0 0 0 0 0 1 1
# 0 0 0 0 0 0 2 x x 1 0 0 0 1 1 1 0 1 x
# 0 0 0 1 1 1 1 2 2 1 0 0 0 1 x 1 1 2 2
# 0 0 0 1 x 3 2 1 0 0 0 1 1 2 1 1 1 x 2
# 0 0 0 1 2 x x 1 0 0 0 1 x 1 0 1 2 3 x
# 0 0 0 0 1 2 2 1 1 1 1 1 1 1 0 1 x 3 2
# 0 0 0 0 1 1 1 1 2 x 1 1 1 1 0 2 3 x 2
# 0 0 0 0 1 x 1 1 x 2 1 1 x 1 0 1 x 3 x
# """.strip()

# gamemap = """
# 0 ? ?
# 0 ? ?
# """.strip()
#
# solvedmap = """
# 0 1 x
# 0 1 1
# """.strip()

result = solve_mine(gamemap, 6)
print(result)