import numpy as np

rows = int(input("enter the number of rows: "))
cols = int(input("enter the number of columns: "))

print(f"enter the elements of the {rows}x{cols} matrix row by row, separated by spaces:")
matrix = []

for i in range(rows):
    row = list(map(int, input(f"Row {i+1}: ").split()))
    matrix.append(row)

arr = np.array(matrix)

filtered_arr = arr[arr % 5 == 0]

print("\nOriginal Matrix:")
print(arr)

print("\nFiltered Elements (divisible by 5):")
print(filtered_arr)
