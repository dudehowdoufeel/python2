#8.	Write a Python program that will accept the base and height of a triangle and compute the area.
'''There are two circles C1 with radius r1, central coordinate (x1, y1) and C2 with radius r2 and central coordinate (x2, y2). 
Write a Python program to test the followings - 
•	"C2 is in C1" if C2 is in C1
•	"C1 is in C2" if C1 is in C2
•	"Circumference of C1 and C2 intersect" if circumference of C1 and C2 intersect, and
•	"C1 and C2 do not overlap" if C1 and C2 do not overlap.
Ex.: 
Input numbers (real numbers) are separated by a space.
Input x1, y1, r1, x2, y2, r2:
5 6 4 8 7 9
C1 is in C2
'''
import math
def tri(a, b):
    return 0.5*a*b
a = int(input())
b = int(input())
area = tri(a, b)
print(f"triangle's area {area}")


def cir(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
    
    if distance + r2 <= r1:
        return "C2 is in C1"
    elif distance + r1 <= r2:
        return "C1 is in C2"
    elif distance <= r1 + r2 and distance >= abs(r1 - r2):
        return "C1 and C2 intersect"
    else:
        return "C1 and C2 don't overlap"
    
x1, y1, r1, x2, y2, r2 = map(float, input("Enter x1, y1, r1, x2, y2, r2: ").split())
result = cir(x1, y1, r1, x2, y2, r2)
print(result)
