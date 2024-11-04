#6
def cntfnums(n):
    mod = 1000000007

    vd = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    dp = [0] * (n + 1)
    dp[0] = 1 

    for length in range(1, n + 1):
        for digit in vd:
            if length == 1 and digit == 0:
                continue
            dp[length] = (dp[length] + dp[length - 1]) % mod
    
    total = sum(dp[1:n + 1]) % mod 

    return total

result = cntfnums(18)
print(result)