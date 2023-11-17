def sudoku(puzzle):
    # idea:
    # 1 for each line / column / 3x3 calculate missing numbers
    # 2 determine for each cell possible values by intersecting missing numbers for line/column/3x3
    # 3 replace 0 with determined value in puzzle matrix and repeat the process
    #   note: because the puzzle is "easy" there should be at least one cell with a well determined value
    #         a well determined value is an intersection set with len() = 1 (one)
    # 4 if we found such a well determined value repeat the process (recursion)
    #    note: this method will return a partially solved puzzle if the puzzle is not easy
    go_deep = False

    # 1 - calculate missing numbers per line
    ml = []
    for l in puzzle:
        ml.append([x for x in range(1, 10) if x not in l])

    # 1 - calculate missing numbers per column
    mc = []
    for c in range(0, len(puzzle)):
        col = list(map(lambda l: l[c], puzzle))
        mc.append([y for y in range(1, 10) if y not in col])

    # 1 - calculate missing numbers per 3x3
    q33 = [[0] * 3 for _ in range(3)]
    mq33 = [[0] * 3 for _ in range(3)]
    for i3 in range(3):
        for j3 in range(3):
            q33[j3][i3] = [[puzzle[x3][y3] for y3 in range(i3 * 3, (i3 + 1) * 3)] for x3 in range(j3 * 3, (j3 + 1) * 3)]

    for i3 in range(3):
        for j3 in range(3):
            nums = []
            for q33_block in q33[j3][i3]:
                nums = nums + q33_block
            mq33[j3][i3] = [n for n in range(1, 10) if n not in nums]

    # 2 - determine for each possible values
    # mcl = 9x9 matrix with possible values
    mcl = [[0] * 9 for _ in range(9)]
    for li in range(0, 9):
        for lj in range(0, 9):
            if puzzle[li][lj] != 0:
                mcl[li][lj] = puzzle[li][lj]
            else:
                li33 = li // 3
                lj33 = lj // 3
                mcl[li][lj] = set(ml[li]).intersection(set(mc[lj])).intersection(set(mq33[li33][lj33]))

                # check if its a well determined value
                # 3 - replace in puzzle matrix and set flag to go deeper in recursion
                if len(mcl[li][lj]) == 1:
                    puzzle[li][lj] = list(mcl[li][lj])[0]
                    go_deep = True
                    break

    # 4 - repeat
    if go_deep:
        return sudoku(puzzle)

    return puzzle



hard_puzzle = \
         [[0, 0, 0, 4, 0, 0, 6, 0, 2],
          [0, 0, 6, 0, 0, 0, 1, 0, 0],
          [0, 9, 0, 5, 0, 0, 0, 8, 0],
          [0, 5, 0, 3, 0, 0, 0, 0, 0],
          [3, 0, 1, 2, 0, 6, 4, 0, 5],
          [0, 0, 0, 0, 0, 7, 0, 2, 0],
          [0, 3, 0, 0, 0, 2, 0, 6, 0],
          [0, 0, 4, 0, 0, 0, 9, 0, 0],
          [5, 0, 7, 0, 0, 9, 0, 0, 0]]

puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]

sol = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
       [6, 7, 2, 1, 9, 5, 3, 4, 8],
       [1, 9, 8, 3, 4, 2, 5, 6, 7],
       [8, 5, 9, 7, 6, 1, 4, 2, 3],
       [4, 2, 6, 8, 5, 3, 7, 9, 1],
       [7, 1, 3, 9, 2, 4, 8, 5, 6],
       [9, 6, 1, 5, 3, 7, 2, 8, 4],
       [2, 8, 7, 4, 1, 9, 6, 3, 5],
       [3, 4, 5, 2, 8, 6, 1, 7, 9]]

res = sudoku(hard_puzzle)

# pretty print
for l in res:
    print(" ".join(str(x) for x in [x if x else '.' for x in l]))
