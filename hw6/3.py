def L(m, n):

    dp = [[0] * (n + 1) for _ in range(m + 1)]
    dp[1][1] = 1

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if i == 1 and j == 1:
                continue
            dp[i][j] = dp[i - 1][j] * (2 * j - 1) + dp[i][j - 1] * (2 * i - 1)

    return dp[m][n]

m, n = 6, 10
result = L(m, n) % (10**10)
print(result)
