def count_patterns_from(firstPoint, length):
    points = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    free_patterns = {
        1: [2, 4, 5, 6, 8],
        2: [1, 3, 4, 5, 6, 7, 9],
        3: [2, 4, 5, 6, 8],
        4: [1, 2, 3, 5, 7, 8, 9],
        5: [1, 2, 3, 4, 6, 7, 8, 9],
        6: [1, 2, 3, 5, 7, 8, 9],
        7: [2, 4, 5, 6, 8],
        8: [1, 3, 4, 5, 6, 7, 9],
        9: [2, 4, 5, 6, 8]
    }
    jump_patterns = {
        1: {2: 3, 4: 7, 5: 9},
        2: {5: 8},
        3: {2: 1, 6: 9, 5: 7},
        4: {5: 6},
        5: {},
        6: {5: 4},
        7: {4: 1, 8: 9, 5: 3},
        8: {5: 2},
        9: {6: 3, 8: 7, 5: 1}
    }

    count_paths = 0

    if length < 2:
        return length

    def get_next(visited):
        for k in free_patterns[visited[-1]]:
            if k not in visited[:-1]:
                yield k
        for x in jump_patterns[visited[-1]].items():
            if x[0] in visited and x[1] not in visited:
                yield x[1]

    def do_count(visited):
        nonlocal count_paths
        if len(visited) == length:
            count_paths = count_paths + 1
            return
        for a in get_next(visited):
            do_count(visited + [a])

    p1 = points.index(firstPoint)

    do_count([p1])

    return count_paths


print(count_patterns_from('A', 10))
print(count_patterns_from('A', 0))
print(count_patterns_from('E', 14))
print(count_patterns_from('B', 1))
print(count_patterns_from('C', 2))
print(count_patterns_from('E', 2))
print(count_patterns_from('E', 4))
