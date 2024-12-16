class LinearAlgebra:
    def __init__(self, matrix=None, vector=None):
        self.matrix = matrix
        self.vector = vector

    # --- VECTOR OPERATIONS ---

    # Vector Addition
    def vector_add(self, v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Vectors must have the same length")
        return [v1[i] + v2[i] for i in range(len(v1))]

    # Vector Subtraction
    def vector_sub(self, v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Vectors must have the same length")
        return [v1[i] - v2[i] for i in range(len(v1))]

    # Scalar Multiplication
    def scalar_multiply(self, scalar, v):
        return [scalar * x for x in v]

    # Dot Product
    def dot_product(self, v1, v2):
        if len(v1) != len(v2):
            raise ValueError("Vectors must have the same length")
        return sum([v1[i] * v2[i] for i in range(len(v1))])

    # --- MATRIX OPERATIONS ---

    # Matrix Addition
    def matrix_add(self, m1, m2):
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("Matrices must have the same dimensions")
        return [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

    # Matrix Subtraction
    def matrix_sub(self, m1, m2):
        if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
            raise ValueError("Matrices must have the same dimensions")
        return [[m1[i][j] - m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]

    # Matrix Multiplication
    def matrix_multiply(self, m1, m2):
        if len(m1[0]) != len(m2):
            raise ValueError("Number of columns of the first matrix must equal the number of rows of the second matrix")
        result = [[sum(m1[i][k] * m2[k][j] for k in range(len(m2))) for j in range(len(m2[0]))] for i in range(len(m1))]
        return result

    # Matrix Transpose
    def transpose(self, m):
        return [[m[i][j] for i in range(len(m))] for j in range(len(m[0]))]

    # Determinant of a Matrix (for 2x2 and 3x3 matrices for simplicity)
    def determinant(self, m):
        if len(m) == 2 and len(m[0]) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        elif len(m) == 3 and len(m[0]) == 3:
            return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])) - \
                   (m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])) + \
                   (m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
        else:
            raise ValueError("Currently, this function only supports 2x2 and 3x3 matrices")

    # --- GAUSSIAN ELIMINATION TO SOLVE LINEAR SYSTEMS ---

    def gaussian_elimination(self, A, b):
        n = len(A)
        Augmented = [A[i] + [b[i]] for i in range(n)]

        for i in range(n):
            if Augmented[i][i] == 0:
                raise ValueError("Matrix is singular and cannot be solved.")
            
            for j in range(i + 1, n):
                ratio = Augmented[j][i] / Augmented[i][i]
                for k in range(i, n + 1):
                    Augmented[j][k] -= ratio * Augmented[i][k]

        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = Augmented[i][n] / Augmented[i][i]
            for j in range(i - 1, -1, -1):
                Augmented[j][n] -= Augmented[j][i] * x[i]

        return x

    # --- MATRIX INVERSION ---

    def inverse(self, A):
        n = len(A)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        Augmented = [A[i] + I[i] for i in range(n)]

        # Forward elimination
        for i in range(n):
            if Augmented[i][i] == 0:
                raise ValueError("Matrix is singular and cannot be inverted.")
            for j in range(i + 1, n):
                ratio = Augmented[j][i] / Augmented[i][i]
                for k in range(2 * n):
                    Augmented[j][k] -= ratio * Augmented[i][k]

        # Backward elimination
        for i in range(n - 1, -1, -1):
            for j in range(i - 1, -1, -1):
                ratio = Augmented[j][i] / Augmented[i][i]
                for k in range(2 * n):
                    Augmented[j][k] -= ratio * Augmented[i][k]

        
        for i in range(n):
            divisor = Augmented[i][i]
            for j in range(2 * n):
                Augmented[i][j] /= divisor

        # Extract the inverse matrix
        inv_A = [row[n:] for row in Augmented]
        return inv_A


# Example Usage
if __name__ == "__main__":
    la = LinearAlgebra()

    # Vector operations example
    v1 = [1, 2, 3, 1]
    v2 = [4, 5, 6, 1]
    print("Vector Addition:", la.vector_add(v1, v2))
    print("Dot Product:", la.dot_product(v1, v2))

    # Matrix operations example
    m1 = [[1, 2], [3, 4]]
    m2 = [[5, 6], [7, 8]]
    print("Matrix Addition:", la.matrix_add(m1, m2))

    # Solving linear system example
    A = [[2, 1], [1, 3]]
    b = [3, 5]
    print("Solution to Linear System:", la.gaussian_elimination(A, b))

    # Matrix Inversion example
    A_inv = la.inverse([[4, 7], [2, 6]])
    print("Matrix Inverse:", A_inv)

