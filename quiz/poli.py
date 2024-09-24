def is_poli(string):
    return string==string[::-1]
a=input()
if is_poli(a):
    print("yes")
else:
    print("no")