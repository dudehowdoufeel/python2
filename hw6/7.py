MOD = 1_000_000_007

def compute_Psi(m):
    psi_3 = 7 
    current_psi = psi_3
    total_Psi = psi_3
    
    for n in range(4, m + 1):
        current_psi = (current_psi + (n - 2)) % MOD
        total_Psi = (total_Psi + current_psi) % MOD
    
    return total_Psi

m = 10**8
result = compute_Psi(m)
print(result)

'''result = compute_Psi(10)
print(result) #345
'''

