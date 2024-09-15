def triangle_type(x, y, z):
    if x == y == z:
        return "Equilateral triangle"
    elif x == y or y == z or x == z:
        return "Isosceles triangle"
    else:
        return "Scalene triangle"
x = float(input("Input length of side x: "))
y = float(input("Input length of side y: "))
z = float(input("Input length of side z: "))
result = triangle_type(x, y, z)
print(result)
