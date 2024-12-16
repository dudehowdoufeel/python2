def determinant(matrix):
#recursion method of det
    n=len(matrix)
    if n==1:
        return matrix[0][0]
    if n==2:
          #define 2*2 matrix
        return matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    
    det=0
    for col in range(n):
        minor=[[matrix[i][j] for j in range(n) if j != col] for i in range(1,n)]
        det+=((-1)**col)*matrix[0][col]*determinant(minor)
    return det

def cramer(matrix,constants):
    n=len(matrix)
    # det main 
    det_main=determinant(matrix)
    if det_main==0:
        raise ValueError("det=0, have no solution")
    
    solutions=[]
    for col in range(n):
        #copy matrix and replace the coloumn
        modified_matrix=[row[:] for row in matrix]
        for row in range(n):
            modified_matrix[row][col]=constants[row]
        
        # det new matrix
        det_modified=determinant(modified_matrix)
        solutions.append(det_modified/det_main)  
    return solutions

def input_system():
    n=int(input("size of matrix: "))
    print("coefficients of the matrix(sep by a space): ")
    matrix=[]
    for i in range(n):
        row=list(map(float, input(f"row {i+1}: ").split()))
        matrix.append(row)
    
    print("enter constants(sep by a space):")
    constants=list(map(float, input().split()))
    return matrix,constants

try:
    matrix,constants=input_system()
    result=cramer(matrix,constants)
    result=[round(x, 6) for x in result]  #round the res
    print("solution: ", result)
except ValueError as e:
    print("error:",e)

#nedostatok: recursive calculation of the determinant can be slow for large matrices (better for 𝑛≤5).