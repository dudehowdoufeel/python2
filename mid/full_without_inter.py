def get_matrix():
    n = int(input("enter the size of matrix: "))
    matrix = []
    for i in range(n):
        row = list(map(float, input(f"enter the row {i + 1} sep by a space: ").split()))
        matrix.append(row)
    return matrix

def determinant(matrix):
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for c in range(len(matrix)):
        sub_matrix = [row[:c] + row[c + 1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(sub_matrix)

    return det

def swap_rows(mat, row1, row2):
    #a function for rearranging two rows in a matrix if the leading element is zero
    mat[row1], mat[row2] = mat[row2], mat[row1]

def inverse(matrix):
    n = len(matrix)
    det = determinant(matrix)

    if det == 0:
        return None  #if the determinant is 0, the matrix is irreversible

    #a single matrix of the same size
    identity_matrix = [[float(i == j) for j in range(n)] for i in range(n)]

    #copy the original matrix so as not to change the original matrix during the algorithm. Instead, all changes are made to its copy
    mat = [row[:] for row in matrix]

    for i in range(n):
        #if the leading element is zero, we change the row to another one where the leading element is not zero
        if mat[i][i] == 0:
            for k in range(i + 1, n):
                if mat[k][i] != 0:
                    swap_rows(mat, i, k)
                    swap_rows(identity_matrix, i, k)
                    break
            else:
                return None  #if the row for the permutation couldn't be found, the matrix is irreversible

        # Normalize the leading element to 1 by dividing the row.
        # This is essential for converting the matrix to the identity matrix
        # and for finding the inverse matrix.

        factor = mat[i][i]
        for j in range(n):
            mat[i][j] /= factor
            identity_matrix[i][j] /= factor

        # Process rows below and above the leading element.
        # This step creates zeros in the current column, simplifying the matrix.

        for k in range(n):
            if i != k:
                factor = mat[k][i]
                for j in range(n):
                    mat[k][j] -= factor * mat[i][j]
                    identity_matrix[k][j] -= factor * identity_matrix[i][j]

    return identity_matrix

def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(lambda x: f"{x:.2f}", row)))

def main():
    print("what do you want to find?")
    print("1 - determinant")
    print("2 - inverse matrix")
    choice = input("enter your choice (1 or 2): ")

    matrix = get_matrix()

    if choice == '1':
        det = determinant(matrix)
        print(f"determinant of the matrix: {det:.2f}")
    elif choice == '2':
        inverse_matrix = inverse(matrix)
        if inverse_matrix:
            print("inverse matrix:")
            print_matrix(inverse_matrix)
        else:
            print("the matrix is non-invertible.")
    else:
        print("invalid choice. Please select 1 or 2.")

main()
