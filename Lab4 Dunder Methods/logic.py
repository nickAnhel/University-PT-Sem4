def matrix_add(m1: list[list[int]], m2: list[list[int]]) -> list[list[int]]:
    result_m = [[] for _ in range(len(m1))]

    for i, mline in enumerate(m1):
        for j, mvalue in enumerate(mline):
            result_m[i].append(mvalue + m2[i][j])

    return result_m


def matrix_dif(m1: list[list[int]], m2: list[list[int]]) -> list[list[int]]:
    result_m = [[] for _ in range(len(m1))]

    for i, mline in enumerate(m1):
        for j, mvalue in enumerate(mline):
            result_m[i].append(mvalue - m2[i][j])

    return result_m


def matrix_mul(m1: list[list[int]], m2: list[list[int]]) -> list[list[int]]:
    result_m = [[0 for _ in range(len(m1))] for _ in range(len(m2[0]))]

    for i, _ in enumerate(m1):
        for j, _ in enumerate(m2[0]):
            for k, _ in enumerate(m2):
                result_m[i][j] += m1[i][k] * m2[k][j]

    return result_m

def matrix_mul(m1: list[list[int]], num: int) -> None:
    for _, mline in enumerate(m1):
        for j, _ in enumerate(mline):
            mline[j] *= num


def matrix_neg(m1: list[list[int]]) -> None:
    for i, _ in enumerate(m1):
        for j, _ in enumerate(m1[i]):
            m1[i][j] *= -1


def matrix_transp(m1: list[list[int]]) -> list[list[int]]:
    trans_m = [[] for _ in range(len(m1))]

    for i, mline in enumerate(m1):
        for j, _ in enumerate(mline):
            trans_m[j].append(m1[i][j])

    return trans_m


matrix_1 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
matrix_2 = [
    [70, 8, 90],
    [4, 50, 6],
    [10, 2, 30],
]


print("Addition")
for line in matrix_add(matrix_1, matrix_2):
    print(line)

print("\nDifference")
for line in matrix_dif(matrix_1, matrix_2):
    print(line)

print("\nMultiple with number")
matrix_mul(matrix_2, 2)
for line in matrix_2:
    print(line)

print("\nTransposition")
for line in matrix_transp(matrix_1):
    print(line)

print("\nNegative matrix")
matrix_neg(matrix_1)
for line in matrix_1:
    print(line)
