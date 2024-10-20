def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(len(matrix)):
        sub_matrix = [row[:c] + row[c + 1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(sub_matrix)

    return det

n = int(input())

matrix = []

for i in range(n):
    matrix.append(list(map(int, input().split())))

det = determinant(matrix)
print(f"Determinant: {det}")
