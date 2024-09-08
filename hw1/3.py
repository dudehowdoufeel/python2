#3.	Write a Python program to test if a variable is a list or tuple or a set.
def test(var):
    if isinstance(var, list):
        return "list"
    elif isinstance(var, tuple):
        return "tuple"
    elif isinstance(var, set):
        return "set"
    else:
        return "none"
    
a = input()
try:
    var = eval(a)
    result = test(var)
    print(result)
except:
    print("error!!! enter set,list or tuple!")