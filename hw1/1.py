#1. Write a Python program to get the identity of an object
def identity(b):
    return id(b)
a = input()
result = identity(a)
print(result)