def kadane(arr):
    max_sum = float('-inf')
    current_sum = 0
    for value in arr:
        current_sum = max(value, current_sum + value)
        max_sum = max(max_sum, current_sum)
    return max_sum

def max_sum_subrectangle(matrix, N):
    max_sum = float('-inf')
    
    for start_row in range(N):
        temp = [0] * N
        
        for end_row in range(start_row, N):
            for col in range(N):
                temp[col] += matrix[end_row][col]
            
            current_max_sum = kadane(temp)
            max_sum = max(max_sum, current_max_sum)
    
    return max_sum

N = int(input()) 
array = []

for i in range(N):
    row = list(map(int, input().split()))
    array.append(row)

# Output the result
print(max_sum_subrectangle(array, N))
