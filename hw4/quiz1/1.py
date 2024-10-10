
a = [3, 6, 9, 12, 15, 18, 21]
b = [4, 8, 12, 16, 20, 24, 28]

odd_a = [a[i] for i in range(len(a)) if i % 2 == 1]
even_b = [b[i] for i in range(len(b)) if i % 2 == 0]
c = odd_a + even_b
print(c)