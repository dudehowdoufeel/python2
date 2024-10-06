def rotation(a):
    if not a:
        return a
    return a[-1:] + a[:-1]
ex = [1, 2, 3, 4, 5]
result = rotation(ex)
print(result)
