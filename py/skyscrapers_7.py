def solve_puzzle(clues):
    size = 7
    # Your magic here...
    result = [[0] * size for _ in range(7)]

    clues_top = clues[0:size]
    clues_right = clues[size:size * 2]
    clues_down = clues[size * 2:size * 3][::-1]
    clues_left = clues[size * 3:size * 4][::-1]

    print(clues)
    print(clues_top)
    print(clues_right)
    print(clues_down)
    print(clues_left)
    print("================")

    def seen(buildings):
        highest = 0
        count = 0
        for b in buildings:
            if b > highest:
                count = count + 1
                highest = b
        return count

    def facts_top(state):
        return [seen([state[j][i] for j in range(0, size)]) for i in range(0, size)]

    def column_unique(state, c, l):
        col = [state[j][c] for j in range(l)]
        return len(set(col)) == l

    def facts_right(state):
        return [seen([state[i][j] for j in range(0, size)[::-1]]) for i in range(0, size)]

    def facts_down(state):
        return [seen([state[j][i] for j in range(0, size)[::-1]]) for i in range(0, size)]

    def facts_left(state):
        return [seen([state[i][j] for j in range(0, size)]) for i in range(0, size)]



    def gen_seq(clue1, clue2, seq):
        l = len(seq)
        # - 0 in seq means free cell (replaced with full list below)
        # - list in seq means what values are possible
        # anything int non-zero means resolved cell
        # clue zero means no constraint
        for k in range(l):
            if seq[k] == 0:
                seq[k] = list(range(1, l + 1))

        k = 0
        combinations = []
        combination = [0] * l
        indices = [0] * l
        while k >= 0:
            if k >= l:
                if len(set(combination)) == l and (clue1 == 0 or clue1 == seen(combination)) and (
                        clue2 == 0 or clue2 == seen(combination[::-1])):
                    combinations.append([scraper for scraper in combination])
                k = k - 1
                while k >= 0 and not isinstance(seq[k], list):
                    k = k - 1
                continue
            if isinstance(seq[k], list):
                if indices[k] >= len(seq[k]):
                    combination[k] = 0
                    indices[k] = 0
                    k = k - 1
                    while not isinstance(seq[k], list):
                        indices[k] = 0
                        k = k - 1
                    continue

                combination[k] = seq[k][indices[k]]
                indices[k] = indices[k] + 1
                k = k + 1
            else:
                combination[k] = seq[k]
                k = k + 1
        return combinations

    def find_map(clues1, clues2, sequences):
        l = len(sequences)
        # - 0 in seq means free cell (replaced with full list below)
        # - list in seq means what values are possible
        # anything int non-zero means resolved cell
        # clue zero means no constraint

        #filter sequences
        filtered = [[] * l for _ in range(l)]
        for b in range(l):
            for c in range(len(sequences[b])):
                seq1 = sequences[b][c]
                good_seq = True
                for a in range(l):
                    dist_clue_top = b
                    dist_clue_down = l - b
                    # on each cell a skyscraper can be there only if scraper < l - clue + distance + 2
                    if (clues1[a] != 0 and seq1[a] >= l - clues1[a] + dist_clue_top + 2) or (clues[2] != 0 and seq1[a] >= l - clues2[a] + dist_clue_down + 2):
                        good_seq = False
                        break
                if good_seq:
                    filtered[b].append(seq1)

        sequences = filtered
        k = 0
        combination = [[0] * l for _ in range(l)]
        indices = [0] * l
        jj = 0
        while k >= 0:
            jj = jj + 1
            if jj % 100000 == 0:
                print(indices)
            if k >= l:
                # validate map
                facts1 = facts_top(combination)
                facts2 = facts_down(combination)
                ok = True
                for a in range(l):
                    if clues1[a] != 0 and clues1[a] != facts1[a]:
                        ok = False
                        break
                    if clues2[a] != 0 and clues2[a] != facts2[a]:
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
                # optimization: check if sequences[k][indices[k]][x] can exist
                # based on distance from clues_top[x] or clues_down[x]
                # seq1 = sequences[k][indices[k]]
                # good_seq = True
                # for a in range(l):
                #     dist_clue_top = k
                #     dist_clue_down = l - k + 1
                #     # on each cell a skyscraper can be there only if scraper < l - clue + distance + 2
                #     if (seq1[a] >= l - clues1[a] + dist_clue_top + 2) or (seq1[a] >= l - clues2[a] + dist_clue_down + 2):
                #         good_seq = False
                #         break
                # if good_seq:
                #     combination[k] = sequences[k][indices[k]]
                #     indices[k] = indices[k] + 1
                #     k = k + 1
                # else:
                #     indices[k] = indices[k] + 1

                # check if vertical constraint is met
                combination[k] = sequences[k][indices[k]]
                indices[k] = indices[k] + 1

                ok = True
                for col_id in range(size):
                    ok = ok and column_unique(combination, col_id, k+1)
                    if not ok:
                        break
                if ok:
                    k = k + 1
            # else:
            #     combination[k] = sequences[k][0]
            #     k = k + 1
        pass


    # place the 7s
    for x in range(0, size):
        # top
        if clues_top[x] == 1:
            result[0][x] = size
        if clues_top[x] == size:
            # fill column up down
            for y in range(0, size):
                result[y][x] = y + 1
        if clues_top[x] + clues_down[x] == size + 1:
            result[clues_top[x]][x] = size

        # right
        if clues_right[x] == 1:
            result[x][size - 1] = size
        if clues_right[x] == size:
            # fill line right to left
            for y in range(size - 1, -1, -1):
                result[x][y] = size - y
        if clues_right[x] + clues_left[x] == size + 1:
            result[x][size - clues_right[x]] = size

        # down
        if clues_down[x] == 1:
            result[size - 1][size - 1 - x] = size
        if clues_down[x] == size:
            # fill column top to bottom
            for y in range(size - 1, -1, -1):
                result[y][size - 1 - x] = size - y

        # left
        if clues_left[x] == 1:
            result[size - 1 - x][0] = size
        if clues_left[x] == size:
            for y in range(size):
                result[size - 1 - x][y] = y + 1

    print(facts_top(result))
    print(facts_right(result))
    print(facts_down(result))
    print(facts_left(result))
    print("---===-----===---")

    seqs = []
    for i in range(size):
        seq = [result[i][j] for j in range(0, size)]
        seqs.append([x for x in gen_seq(clues_left[i], clues_right[i], seq)])


    print("### generated seq ###")
    print("# row = ", [result[2][j] for j in range(0, size)])
    # [print(x) for x in gen_seq(clues_left[2], clues_right[2], [result[2][j] for j in range(0, size)])]
    # print(seqs[2])
    print(find_map(clues_top, clues_down, seqs))
    print("### ############# ###")

    return result


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

print("\n".join([str(k) for k in solve_puzzle(test1)]))
