def find_median(a, b, c):
    numbers = [a, b, c]
    numbers.sort()
    return numbers[1]

first_number = float(input("Input first number: "))
second_number = float(input("Input second number: "))
third_number = float(input("Input third number: "))

median = find_median(first_number, second_number, third_number)
print(f"The median is {median}.")
