def det2x2(mat2x2):
    return mat2x2[0][0] * mat2x2[1][1] - mat2x2[1][0] * mat2x2[0][1]


def mat_minor(matrix, i, j):
    cols = list(map(lambda l: l[0:i] + l[i + 1:], matrix))
    return cols[0:j] + cols[j + 1:]


def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return det2x2(matrix)
    signs = [1, -1]
    detval = 0
    for x in range(len(matrix)):
        detval = detval + matrix[0][x] * signs[x % 2] * determinant(mat_minor(matrix, x, 0))
        # print(x, mat_minor(matrix, x, 0), signs[x % 2], determinant(mat_minor(matrix, x, 0)))
        # print('detval=', detval)

    return detval


m1 = [[1, 3], [2, 5]]

m2 = [
    [2, 5, 3],
    [1, -2, -1],
    [1, 3, 4]
]

# l = [1, 2, 3, 4, 5]

# print(l[0:1] + l[2:])

print(mat_minor(m2, 2, 0))

print(determinant(m1))
print(determinant(m2))
