#5.	Write a Python program to sum all the items in a list.
def sum(n):
    sum = 0
    for i in n:
        sum+=i
    return sum
a = input()
n = [int(x.strip()) for x in a.split(',')]
result = sum(n)
print(n)
print(result)
