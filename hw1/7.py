#7.	Write a Python program to display your details like name, age, address in three different lines.
'''Input: Saule 18 Astana
Output: Saule
               18
               Astana
'''
def sep(name,age,address):
    print(name)
    print(age)
    print(address)

a = input()
name,age,address = a.split(maxsplit=2)
sep(name,age,address)