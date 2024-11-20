import numpy as np
rows = 4
cols = 4
print(f"Enter the elements of the {rows}x{cols} matrix row by row, separated by spaces:")
matrix = []

for i in range(rows):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    matrix.append(row)

arr = np.array(matrix)

transpose = np.transpose(arr)
determinant = np.linalg.det(arr)
eigenvalues = np.linalg.eigvals(arr)

print("\nTranspose of the matrix:")
print(transpose)

print("\nDeterminant of the matrix:")
print(determinant)

print("\nEigenvalues of the matrix:")
print(eigenvalues)
