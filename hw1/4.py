#4.	Write a python program to sum of the first n positive integers
def sum(n):
    return n*(n+1)//2
a = int(input())
result = sum(a)
print(result)