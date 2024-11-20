import numpy as np
arr1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
arr2 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

arr_add = arr1 + arr2
arr_sub = arr1 - arr2
arr_mult = arr1 * arr2

arr_add, arr_sub, arr_mult
print(arr_add)
print(arr_sub)
print(arr_mult)