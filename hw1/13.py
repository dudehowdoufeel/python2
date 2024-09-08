#13.	Write a Python program to remove and print every third number from a list of numbers until the list becomes empty.

def removeNums(n):
    index = 2 
    count = 1  
    
    while n:
        print(n[index])
        n.pop(index) 
        if n:
            index = (index + 2) % len(n)
        count += 1

a = [10, 20, 30, 40, 50, 60, 70, 80, 90]
removeNums(a)
