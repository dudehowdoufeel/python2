def print_number_pattern(n):
    for i in range(1, n + 1):
        for j in range(i):
            print(i, end='')
        print()
try:
    n = int(input("Enter the number of rows: "))
    if n > 0:
        print_number_pattern(n)
    else:
        print("Please enter a positive integer.")
except ValueError:
    print("Please enter a valid integer.")

