#12.	Write a Python program to create a tuple with numbers and print one item.
def tup():
    a = input()
    numTup = tuple(map(int, a.split(',')))
    return numTup

def item(tup):
    index = int(input())
    if 0 <= index < len(tup):
        print(f"The item at index {index} is: {tup[index]}")
    else:
        print("Invalid index. Please enter a valid index.")

result = tup()
item(result)
