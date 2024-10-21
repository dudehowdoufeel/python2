import tkinter as tk
from tkinter import simpledialog, messagebox

def get_matrix(size):
    matrix = []
    for i in range(size):
        row = simpledialog.askstring("input", f"enter row {i + 1} (space-separated):")
        row_values = list(map(float, row.split()))
        matrix.append(row_values)
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
    mat[row1], mat[row2] = mat[row2], mat[row1]

def inverse(matrix):
    n = len(matrix)
    det = determinant(matrix)

    if det == 0:
        return None

    identity_matrix = [[float(i == j) for j in range(n)] for i in range(n)]
    mat = [row[:] for row in matrix]

    for i in range(n):
        if mat[i][i] == 0:
            for k in range(i + 1, n):
                if mat[k][i] != 0:
                    swap_rows(mat, i, k)
                    swap_rows(identity_matrix, i, k)
                    break
            else:
                return None

        factor = mat[i][i]
        for j in range(n):
            mat[i][j] /= factor
            identity_matrix[i][j] /= factor

        for k in range(n):
            if i != k:
                factor = mat[k][i]
                for j in range(n):
                    mat[k][j] -= factor * mat[i][j]
                    identity_matrix[k][j] -= factor * identity_matrix[i][j]

    return identity_matrix

def display_matrix(matrix):
    result = "\n".join(" ".join(f"{x:.2f}" for x in row) for row in matrix)
    messagebox.showinfo("result", result)

def calculate_determinant():
    size = simpledialog.askinteger("input", "enter matrix size:")
    matrix = get_matrix(size)
    det = determinant(matrix)
    messagebox.showinfo("determinant", f"determinant: {det:.2f}")

def calculate_inverse():
    size = simpledialog.askinteger("input", "enter matrix size:")
    matrix = get_matrix(size)
    inv_matrix = inverse(matrix)
    if inv_matrix:
        display_matrix(inv_matrix)
    else:
        messagebox.showerror("error", "the matrix is non-invertible.")

def main():
    window = tk.Tk()
    window.title("matrix Calculator")
    window.geometry("400x300")  #window size to 400x300

    label = tk.Label(window, text="what do you want to calculate?", font=("Times New Roman", 16))
    label.pack(pady=20)

    determinant_button = tk.Button(window, text="determinant", command=calculate_determinant, font=("Times New Roman", 14), width=20, height=2)
    determinant_button.pack(pady=10)

    inverse_button = tk.Button(window, text="inverse Matrix", command=calculate_inverse, font=("Times New Roman", 14), width=20, height=2)
    inverse_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
