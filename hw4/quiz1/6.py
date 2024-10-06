def calc(a, b, n):
    return (n*(2*a+(n-1)*b)) // 2

num_test_cases = int(input("enter number"))
results = []

for _ in range(num_test_cases):
    a,b,n = map(int, input().split())
    results.append(calc(a,b,n))

print(" ".join(map(str, results)))
