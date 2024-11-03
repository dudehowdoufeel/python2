from math import *
import itertools

def all_perm(n):
    global all_perm
    numbers = []
    for i in range(1, n + 1):
        numbers.append(i)
    all_perm = [p for p in itertools.product(numbers, repeat=n)]
    return all_perm

def repeation(a):
    result = 0
    all_result = []
    for i in range(len(a) - 1):
        if a[i] == a[i+1]:
            result += 1
            if i == len(a) - 2:
                all_result.append(result + 1)
        else:
            all_result.append(result + 1)
            result = 0
    return max(all_result)

def all():
    n = int(input("n = "))
    all_perm(n)
    result= 0
    for seq in all_perm:
        result += repeation(seq)
    print(result)

all()