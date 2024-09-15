def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

input_string = input("Input a string: ")
if is_integer(input_string):
    print("The string is an integer.")
else:
    print("The string is not an integer.")
