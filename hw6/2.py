from math import *

def tri(a, b, c):
    if a < b + c and b < a + c and c < a + b:
        return True

def check(a, b, c):
    if a <= b <= c:
        return True

def med(a, b, c):
    m = sqrt(2 * pow(a, 2) + 2 * pow(b, 2) - pow(c, 2))/2
    if m.is_integer():
        return True

n = int(input("n = "))
result = 0
for i in range(n + 1):
    for j in range(n + 1):
        for k in range(n + 1):
            if tri(i, j, k) and med(i, j, k) and check(i, j, k):
                result += 1

print(result)