def sum(a, b):
    total = a + b
    if 15 <= total <= 20:
        return 20
    else:
        return total
num1 = int(input("Enter the first integer: "))
num2 = int(input("Enter the second integer: "))

result = sum(num1, num2)
print(f"The result is: {result}")
