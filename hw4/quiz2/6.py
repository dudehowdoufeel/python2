<<<<<<< HEAD
def calc(x1, y1, x2, y2):
    a = (y2 - y1) // (x2 - x1)
    b = y1 - a * x1
    return a, b

a = int(input())
results = []

for _ in range(a):
    x1, y1, x2, y2 = map(int, input().split())
    a, b = calc(x1, y1, x2, y2)
    results.append(f"({a} {b})")

print(" ".join(results))
