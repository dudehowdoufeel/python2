from math import *
import itertools

def all_perm(n):
    global permutations
    numbers = []
    for i in range(2, n):
        numbers.append(i)
    permutations = list(itertools. permutations(numbers))
    return permutations

def perm_with_max_3(n):
    all_perm(n)
    res = 0
    for perm in permutations:
        flag = True
        for i in range(len(perm) - 1):
            if abs(perm[i + 1] - perm[i]) > 3:
                flag = False
                break
            if perm[i+1] == perm[n - 3]:
                if perm[i+1] + 3 < n:
                    flag = False
                    break
            if perm[i] == perm[0]:
                if abs(perm[i] - 3) > 1:
                    flag = False
                    break
        if flag:
            res += 1               
    return res

def S(L):
    res = 0
    for i in range(1, L+1):
        res += pow(perm_with_max_3(i), 3)
    print(res)

L = int(input("L = "))
S(L)