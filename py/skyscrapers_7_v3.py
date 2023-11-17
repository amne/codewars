def solve_puzzle(clues):
    RESOLVED = 0
    MODIFIED = 1
    LINE = 0
    COLUMN = 1
    size = len(clues) // 4

    result = [[list(range(1, size + 1)) for _ in range(size)] for _ in range(size)]

    clues_top = clues[0:size]
    clues_right = clues[size:size * 2]
    clues_down = clues[size * 2:size * 3][::-1]
    clues_left = clues[size * 3:size * 4][::-1]

    def double_seen(seq):
        high1 = 0
        high2 = 0
        count1 = 0
        count2 = 0
        for b in range(len(seq)):
            if seq[b] > high1:
                count1 = count1 + 1
                high1 = seq[b]
            if seq[-b - 1] > high2:
                high2 = seq[-b - 1]
                count2 = count2 + 1
        return count1, count2

    def seq_unique(seq, l):
        return len(set(seq[:l])) == l

    def column_unique(state, c, l):
        col = [state[j][c] for j in range(l)]
        return len(set(col)) == l

    gen_seq_rec_cache = {}

    # generate sequences (recursive implementation)
    def gen_seq_rec(clue1, clue2, seq):
        cache_key = str(clue1) + "_" + str(clue2) + str(seq)
        if cache_key in gen_seq_rec_cache.keys():
            return gen_seq_rec_cache[cache_key]
        # prepare
        l = len(seq)
        for k in range(l):
            if seq[k] == 0:
                seq[k] = list(range(1, l + 1))
            elif not isinstance(seq[k], list):
                seq[k] = [seq[k]]

        combinations = []

        def rec(s, idx):
            for x in seq[idx]:
                c = s.copy()
                if s.count(x):
                    continue
                c.append(x)

                if idx == len(seq) - 1:
                    fact1, fact2 = double_seen(c)
                    if (clue1 == 0 or clue1 == fact1) and (clue2 == 0 or clue2 == fact2):
                        combinations.append(c)
                else:
                    rec(c, idx + 1)
            pass

        rec([], 0)
        gen_seq_rec_cache[cache_key] = combinations
        return combinations

    audit = []

    # solve_edges
    for x in range(0, size):
        # top
        if clues_top[x] == 1:
            result[0][x] = size
            audit.append((0, x, RESOLVED))
        elif clues_top[x] == size:
            # fill column up down
            for y in range(0, size):
                result[y][x] = y + 1
                audit.append((y, x, RESOLVED))
        elif clues_top[x] != 0:
            # remove values that can't exist based on the edge clue
            for d in range(clues_top[x]):
                if isinstance(result[d][x], list):
                    # result[d][x] = [v for v in result[d][x] if v < size - clues_top[x] + 2 + d]
                    for v in range(size - clues_top[x] + 2 + d, size + 1):
                        try:
                            result[d][x].remove(v)
                            audit.append((d, x, MODIFIED, v, COLUMN))
                        except ValueError:
                            pass

        # sum of opposing clues is size + 1 then highest building is fixed
        if clues_top[x] + clues_down[x] == size + 1:
            result[clues_top[x] - 1][x] = size
            audit.append((clues_top[x] - 1, x, RESOLVED))

        # right
        if clues_right[x] == 1:
            result[x][size - 1] = size
            audit.append((x, size - 1, RESOLVED))
        elif clues_right[x] == size:
            # fill line right to left
            for y in range(size - 1, -1, -1):
                result[x][y] = size - y
                audit.append((x, y, RESOLVED))
        elif clues_right[x] != 0:
            # remove values that can't exist based on the edge clue
            for d in range(size - 1, size - 1 - clues_right[x], -1):
                if isinstance(result[x][d], list):
                    # result[x][d] = [v for v in result[x][d] if v < size - clues_right[x] + 2 + (size - d - 1)]
                    for v in range(size - clues_right[x] + 2 + (size - d - 1), size + 1):
                        try:
                            result[x][d].remove(v)
                            audit.append((x, d, MODIFIED, v, LINE))
                        except ValueError:
                            pass

        if clues_right[x] + clues_left[x] == size + 1:
            result[x][size - clues_right[x]] = size
            audit.append((x, size - clues_right[x], RESOLVED))

        # down
        if clues_down[x] == 1:
            result[size - 1][x] = size
            audit.append((size - 1, x, RESOLVED))
        elif clues_down[x] == size:
            # fill column top to bottom
            for y in range(size - 1, -1, -1):
                result[y][x] = size - y
                audit.append((y, x, RESOLVED))
        elif clues_down[x] != 0:
            # remove values that can't exist based on the edge clue
            for d in range(size - 1, size - 1 - clues_down[x], -1):
                if isinstance(result[d][x], list):
                    # result[d][x] = [v for v in result[d][x] if v < size - clues_down[x] + 2 + (size - d - 1)]
                    for v in range(size - clues_down[x] + 2 + (size - d - 1), size + 1):
                        try:
                            result[d][x].remove(v)
                            audit.append((d, x, MODIFIED, v, COLUMN))
                        except ValueError:
                            pass

        # left
        if clues_left[x] == 1:
            result[x][0] = size
            audit.append((x, 0, RESOLVED))
        elif clues_left[x] == size:
            for y in range(size):
                result[x][y] = y + 1
                audit.append((x, y, RESOLVED))
        elif clues_left[x] != 0:
            # remove values that can't exist based on the edge clue
            for d in range(clues_left[x]):
                if isinstance(result[x][d], list):
                    # result[x][d] = [v for v in result[x][d] if v < size - clues_left[x] + 2 + d]
                    for v in range(size - clues_left[x] + 2 + d, size + 1):
                        try:
                            result[x][d].remove(v)
                            audit.append((x, d, MODIFIED, v, LINE))
                        except ValueError:
                            pass

    # for each resolved cell
    while len(audit):
        # print("q: ", audit)
        # for x in range(len(test1) // 4):
        #     print(" ".join([str(k) for k in result[x]]))
        # for each cell remove the resolved value from the cross
        t = audit[0]
        # shift it first
        audit = audit[1:]
        if t[2] == RESOLVED:
            celly, cellx, op = t
            for i in range(size):
                try:
                    if isinstance(result[celly][i], list):
                        result[celly][i].remove(result[celly][cellx])
                        if len(result[celly][i]) == 1:
                            result[celly][i] = result[celly][i][0]
                            audit.append((celly, i, RESOLVED))
                        else:
                            audit.append((celly, i, MODIFIED, result[celly][cellx], LINE))
                except ValueError:
                    pass
                try:
                    if isinstance(result[i][cellx], list):
                        result[i][cellx].remove(result[celly][cellx])
                        if len(result[i][cellx]) == 1:
                            result[i][cellx] = result[i][cellx][0]
                            audit.append((i, cellx, RESOLVED))
                        else:
                            audit.append((i, cellx, MODIFIED, result[celly][cellx], COLUMN))
                except ValueError:
                    pass
        if t[2] == MODIFIED:
            # we have removed a value. check if there is only one cell with list that has the removed value
            # in the cross
            # direction is so we know which way the value was removed
            celly, cellx, op, val, direction = t
            if direction == LINE:
                # we were going per line so check column
                col = [a[cellx] for a in result if isinstance(a, list)]
                ll = [a for a in col if
                      (isinstance(a, list) and a.count(val)) or (not isinstance(a, list) and a == val)]
                if len(ll) == 1:
                    for i in range(size):
                        if isinstance(result[i][cellx], list) and result[i][cellx].count(val):
                            result[i][cellx] = val
                            audit.append((i, cellx, RESOLVED))
            if direction == COLUMN:
                # we were going per column so check line
                line = result[celly]
                ll = [a for a in line if
                      (isinstance(a, list) and a.count(val)) or (not isinstance(a, list) and a == val)]
                if len(ll) == 1:
                    for i in range(size):
                        if isinstance(result[celly][i], list) and result[celly][i].count(val):
                            result[celly][i] = val
                            audit.append((celly, i, RESOLVED))

        # per line
        seqs = []
        for i in range(size):
            seq = [result[i][j] for j in range(0, size)]
            if clues_left[i] or clues_right[i]:
                seqs.append((i, [x for x in gen_seq_rec(clues_left[i], clues_right[i], seq)]))
        for i, s in seqs:
            if len(s) == 1:
                for k in range(size):
                    if isinstance(result[i][k], list):
                        audit.append((i, k, RESOLVED))
                    result[i][k] = s[0][k]
            elif len(s) > 1:
                # see if all sequences have same value on some cells
                for i, s in seqs:
                    bloom = [[] for _ in range(size)]
                    for seq in s:
                        for v in range(size):
                            bloom[v].append(seq[v])
                    for j in range(size):
                        bloom[j] = list(set(bloom[j]))
                        if isinstance(result[i][j], list):
                            if len(bloom[j]) == 1:
                                result[i][j] = bloom[j][0]
                                audit.append((i, j, RESOLVED))
                            elif len(bloom[j]) < len(result[i][j]):
                                for ij in [r for r in result[i][j]]:
                                    if bloom[j].count(ij) == 0:
                                        result[i][j].remove(ij)
                                        audit.append((i, j, MODIFIED, ij, LINE))
                                        audit.append((i, j, MODIFIED, ij, COLUMN))

        # per column
        seqs = []
        for i in range(size):
            seq = [result[j][i] for j in range(0, size)]
            if clues_top[i] or clues_down[i]:
                seqs.append((i, [x for x in gen_seq_rec(clues_top[i], clues_down[i], seq)]))
        for i, s in seqs:
            if len(s) == 1:
                for k in range(size):
                    if isinstance(result[k][i], list):
                        audit.append((k, i, RESOLVED))
                    result[k][i] = s[0][k]
            elif len(s) > 1:
                # see if all sequences have same value on some cells

                for i, s in seqs:
                    bloom = [[] for _ in range(size)]
                    for seq in s:
                        for v in range(size):
                            bloom[v].append(seq[v])
                    for j in range(size):
                        bloom[j] = list(set(bloom[j]))
                        if isinstance(result[j][i], list):
                            if len(bloom[j]) == 1:
                                result[j][i] = bloom[j][0]
                                audit.append((j, i, RESOLVED))
                            elif len(bloom[j]) < len(result[j][i]):
                                for ij in [r for r in result[j][i]]:
                                    if bloom[j].count(ij) == 0:
                                        result[j][i].remove(ij)
                                        audit.append((j, i, MODIFIED, ij, LINE))
                                        audit.append((j, i, MODIFIED, ij, COLUMN))

    seqs = []
    for i in range(size):
        seq = [result[i][j] for j in range(0, size)]
        seqs.append([x for x in gen_seq_rec(clues_left[i], clues_right[i], seq)])

    # same idea as gen seq but iterative implementation
    def solve_map(clues1, clues2, sequences):
        l = len(sequences)

        k = 0
        combination = [[0] * l for _ in range(l)]
        indices = [0] * l
        jj = 0
        while k >= 0:
            jj = jj + 1
            if k >= l:
                # validate map
                # facts1 = facts_top(combination)
                # facts2 = facts_down(combination)
                ok = True
                for a in range(l):
                    col = [combination[i][a] for i in range(size)]
                    facts1, facts2 = double_seen(col)
                    if clues1[a] != 0 and clues1[a] != facts1:
                        ok = False
                        break
                    if clues2[a] != 0 and clues2[a] != facts2:
                        ok = False
                        break
                if ok:
                    return combination
                k = k - 1
                while k >= 0 and len(sequences[k]) == 1:
                    k = k - 1
                continue
            if True:
                if indices[k] >= len(sequences[k]):
                    combination[k] = []
                    indices[k] = 0
                    k = k - 1
                    while len(sequences[k]) == 1:
                        indices[k] = 0
                        k = k - 1
                    continue

                # check if vertical constraint is met
                combination[k] = sequences[k][indices[k]]
                indices[k] = indices[k] + 1

                ok = True
                for col_id in range(size):
                    col = [combination[lk][col_id] for lk in range(k + 1)]
                    ok = ok and len(set(col)) == k + 1

                    if not ok:
                        break
                if ok:
                    k = k + 1

        pass

    return solve_map(clues_top, clues_down, seqs)

# test1:
# [1, 5, 6, 7, 4, 3, 2]
# [2, 7, 4, 5, 3, 1, 6]
# [3, 4, 5, 6, 7, 2, 1]
# [4, 6, 3, 1, 2, 7, 5]
# [5, 3, 1, 2, 6, 4, 7]
# [6, 2, 7, 3, 1, 5, 4]
# [7, 1, 2, 4, 5, 6, 3]
#       |        up-down     |    right-left      |     down-up        |    left-right     |
test1 = [7, 0, 0, 0, 2, 2, 3, 0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4]
#       |                    |                    |                    |                   |
test2 = [0, 2, 3, 0, 2, 0, 0, 5, 0, 4, 5, 0, 4, 0, 0, 4, 2, 0, 0, 0, 6, 5, 2, 2, 2, 2, 4, 1]

# medved
#       |                    |                    |                    |                   |
test3 = [3, 3, 2, 1, 2, 2, 3, 4, 3, 2, 4, 1, 4, 2, 2, 4, 1, 4, 5, 3, 2, 3, 1, 4, 2, 5, 2, 3]

# failing
#       |                    |                    |                    |                   |
test4 = [0, 0, 3, 0, 0, 0, 0, 3, 0, 3, 0, 0, 5, 0, 0, 0, 0, 0, 5, 0, 4, 7, 0, 0, 0, 2, 2, 3]

scraper_map = solve_puzzle(test3)

print("=" * 10)
for x in range(len(test1) // 4):
    print(" ".join([str(k) for k in scraper_map[x]]))
