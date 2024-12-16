import math
import re
import tkinter as tk
from tkinter import ttk, messagebox

# ---------------- Conic Functions ---------------- #

def sintax(equation):
    # Remove spaces and split at '=' to get the left-hand side
    equation = equation.replace(" ", "").split("=")[0]

    # Replace '-' with '+-' to simplify splitting
    equation = equation.replace("-", "+-")

    # Remove leading '+' if present
    if equation.startswith("+"):
        equation = equation[1:]

    # Split the equation into parts based on '+'
    parts = equation.split("+")

    # Initialize coefficients
    coefficients = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

    # Regex to identify terms
    patterns = {
        "A": re.compile(r'^([+-]?[\d\.]*)x\^2$'),
        "B": re.compile(r'^([+-]?[\d\.]*)xy$'),
        "C": re.compile(r'^([+-]?[\d\.]*)y\^2$'),
        "D": re.compile(r'^([+-]?[\d\.]*)x$'),
        "E": re.compile(r'^([+-]?[\d\.]*)y$'),
        "F": re.compile(r'^([+-]?[\d\.]+)$')
    }

    for part in parts:
        if not part:
            continue
        matched = False
        for key, pattern in patterns.items():
            match = pattern.match(part)
            if match:
                coeff = match.group(1)
                if coeff in ["", "+"]:
                    coeff = 1.0
                elif coeff == "-":
                    coeff = -1.0
                else:
                    try:
                        coeff = float(coeff)
                    except ValueError:
                        raise ValueError(f"Invalid coefficient in term '{part}'")
                coefficients[key] += coeff
                matched = True
                break
        if not matched:
            raise ValueError(f"Unrecognized term: '{part}'")

    return coefficients["A"], coefficients["B"], coefficients["C"], coefficients["D"], coefficients["E"], coefficients["F"]

def classify_conic(A, B, C):
    disc = B**2 - 4*A*C  # Discriminant
    if disc < 0:
        if A == C and B == 0:
            return "Circle"
        return "Ellipse"
    elif disc == 0:
        return "Parabola"
    else:
        return "Hyperbola"

def rotate_conic(A, B, C):
    if B == 0:
        return A, B, C, 0  # No rotation needed
    angle = 0.5 * math.atan2(B, A - C)
    cos_t = math.cos(angle)
    sin_t = math.sin(angle)
    A_new = A * cos_t**2 - B * cos_t * sin_t + C * sin_t**2
    C_new = A * sin_t**2 + B * cos_t * sin_t + C * cos_t**2
    return A_new, 0, C_new, angle

def translate_conic(A, C, D, E, F):
    x0 = -D / (2 * A) if A != 0 else 0
    y0 = -E / (2 * C) if C != 0 else 0
    F_new = F + A * x0**2 + C * y0**2 + D * x0 + E * y0
    return F_new, x0, y0

def canonical_parabola(A, C, D, E, F):
    if A != 0 and C == 0:  # y^2 = 4px type
        x0 = -D / (2 * A)
        p = -E / (2 * A)
        return f"(y - {p})² = {4 * A}(x - {x0})"
    elif C != 0 and A == 0:  # x^2 = 4py type
        y0 = -E / (2 * C)
        p = -D / (2 * C)
        return f"(x - {p})² = {4 * C}(y - {y0})"
    else:
        return "Cannot simplify to canonical form"

def to_canonical_form(A, B, C, D, E, F):
    A_new, _, C_new, angle = rotate_conic(A, B, C)
    F_new, x0, y0 = translate_conic(A_new, C_new, D, E, F)
    return A_new, C_new, F_new, x0, y0, angle

def get_conic_info(equation):
    A, B, C, D, E, F = sintax(equation)
    conic_type = classify_conic(A, B, C)

    if conic_type == "Circle":
        A_new, _, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
        if A_new == 0:
            raise ValueError("Invalid equation for a circle.")
        radius_sq = -F_new / A_new
        if radius_sq < 0:
            raise ValueError("Negative radius squared. Check the equation.")
        radius = math.sqrt(radius_sq)
        canonical = f"(x - {x0})² + (y - {y0})² = {radius_sq}"
        return conic_type, canonical

    elif conic_type == "Ellipse":
        A_new, C_new, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
        if A_new == 0 or C_new == 0:
            raise ValueError("Invalid equation for an ellipse.")
        a_sq = -F_new / A_new
        b_sq = -F_new / C_new
        if a_sq <= 0 or b_sq <= 0:
            raise ValueError("Invalid canonical form for an ellipse.")
        a = math.sqrt(a_sq)
        b = math.sqrt(b_sq)
        canonical = f"((x - {x0})²) / {a_sq} + ((y - {y0})²) / {b_sq} = 1"
        return conic_type, canonical

    elif conic_type == "Hyperbola":
        A_new, C_new, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
        if A_new == 0 or C_new == 0:
            raise ValueError("Invalid equation for a hyperbola.")
        a_sq = abs(F_new / A_new)
        b_sq = abs(F_new / C_new)
        if a_sq == 0 or b_sq == 0:
            raise ValueError("Invalid canonical form for a hyperbola.")
        a = math.sqrt(a_sq)
        b = math.sqrt(b_sq)
        # Determine the sign to place with a_sq
        if F_new / A_new > 0:
            canonical = f"((x - {x0})²) / {a_sq} - ((y - {y0})²) / {b_sq} = 1"
        else:
            canonical = f"((y - {y0})²) / {b_sq} - ((x - {x0})²) / {a_sq} = 1"
        return conic_type, canonical

    elif conic_type == "Parabola":
        canonical = canonical_parabola(A, C, D, E, F)
        return conic_type, canonical

# ---------------- Linear Algebra Functions ---------------- #

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

    # Determinant of a Matrix (supports 2x2 and 3x3)
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

# ---------------- Additional Mathematical Functions ---------------- #

def polynomial_roots(coeffs):
    n = len(coeffs) - 1
    if n == 1:
        return [-coeffs[0] / coeffs[1]]
    elif n == 2:
        a = coeffs[2]
        b = coeffs[1]
        c = coeffs[0]
        disc = b * b - 4 * a * c
        if disc < 0:
            return []
        elif abs(disc) < 1e-14:
            return [-b / (2 * a)]
        else:
            sqrt_disc = math.sqrt(disc)
            return [(-b + sqrt_disc) / (2 * a), (-b - sqrt_disc) / (2 * a)]
    else:
        raise NotImplementedError("Roots only implemented up to quadratic.")

def char_poly_coefficients(A):
    # Characteristic polynomial coefficients for 2x2 and 3x3 matrices
    n = len(A)
    if n == 2:
        a = 1
        b = - (A[0][0] + A[1][1])
        c = A[0][0]*A[1][1] - A[0][1]*A[1][0]
        return [c, b, a]
    elif n == 3:
        a = 1
        b = - (A[0][0] + A[1][1] + A[2][2])
        c = (A[0][0]*A[1][1] + A[0][0]*A[2][2] + A[1][1]*A[2][2]) - (A[0][1]*A[1][0] + A[0][2]*A[2][0] + A[1][2]*A[2][1])
        d = - (A[0][0]*A[1][1]*A[2][2] + A[0][1]*A[1][2]*A[2][0] + A[0][2]*A[1][0]*A[2][1] -
                A[0][2]*A[1][1]*A[2][0] - A[0][1]*A[1][0]*A[2][2] - A[0][0]*A[1][2]*A[2][1])
        return [d, c, b, a]
    else:
        raise NotImplementedError("Characteristic polynomial implemented only for 2x2 and 3x3 matrices.")

def eigenvalues_eigenvectors(A):
    coeffs = char_poly_coefficients(A)
    lambdas = polynomial_roots(coeffs)
    # For simplicity, eigenvectors computation is omitted
    return lambdas, None  # Placeholder for eigenvectors

def gram_schmidt(V):
    U = []
    for v in V:
        v_copy = v[:]
        for u in U:
            dot_vu = sum(x * y for x, y in zip(v_copy, u))
            v_copy = [x - dot_vu * u_el for x, u_el in zip(v_copy, u)]
        norm = math.sqrt(sum(x * x for x in v_copy))
        if abs(norm) > 1e-14:
            U.append([x / norm for x in v_copy])
    return U

def project_onto_subspace(v, subspace):
    Q = gram_schmidt(subspace)
    proj = [0] * len(v)
    for q in Q:
        dot_vq = sum(x * y for x, y in zip(v, q))
        proj = [pv + dot_vq * qv for pv, qv in zip(proj, q)]
    return proj

# ---------------- GUI Application ---------------- #

class MathCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Comprehensive Math Calculator")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        # Tabs
        self.conic_tab = ttk.Frame(tab_control)
        self.linear_tab = ttk.Frame(tab_control)
        self.vector_tab = ttk.Frame(tab_control)
        self.matrix_tab = ttk.Frame(tab_control)
        self.poly_tab = ttk.Frame(tab_control)
        self.eigen_tab = ttk.Frame(tab_control)
        self.gram_schmidt_tab = ttk.Frame(tab_control)
        self.projection_tab = ttk.Frame(tab_control)

        # Add tabs to notebook
        tab_control.add(self.conic_tab, text='Conic Classification')
        tab_control.add(self.linear_tab, text='Linear System Solver')
        tab_control.add(self.vector_tab, text='Vector Operations')
        tab_control.add(self.matrix_tab, text='Matrix Operations')
        tab_control.add(self.poly_tab, text='Polynomial Roots')
        tab_control.add(self.eigen_tab, text='Eigenvalues/Vectors')
        tab_control.add(self.gram_schmidt_tab, text='Gram-Schmidt')
        tab_control.add(self.projection_tab, text='Projection')

        tab_control.pack(expand=1, fill="both")

        # Initialize each tab
        self.create_conic_tab()
        self.create_linear_tab()
        self.create_vector_tab()
        self.create_matrix_tab()
        self.create_poly_tab()
        self.create_eigen_tab()
        self.create_gram_schmidt_tab()
        self.create_projection_tab()

    # ---------------- Conic Classification Tab ---------------- #

    def create_conic_tab(self):
        frame = self.conic_tab

        # Equation input
        equation_label = ttk.Label(frame, text="Enter Conic Equation:")
        equation_label.pack(pady=10)
        self.conic_equation_entry = ttk.Entry(frame, width=50)
        self.conic_equation_entry.pack()

        # Solve button
        solve_button = ttk.Button(frame, text="Classify & Canonical Form", command=self.solve_conic)
        solve_button.pack(pady=10)

        # Result display
        self.conic_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.conic_result.pack(pady=10)

    def solve_conic(self):
        equation = self.conic_equation_entry.get()
        try:
            conic_type, canonical = get_conic_info(equation)
            result_text = f"Conic Type: {conic_type}\nCanonical Form: {canonical}"
        except Exception as e:
            result_text = f"Error: {e}"

        self.conic_result.configure(state='normal')
        self.conic_result.delete("1.0", tk.END)
        self.conic_result.insert(tk.END, result_text)
        self.conic_result.configure(state='disabled')

    # ---------------- Linear System Solver Tab ---------------- #

    def create_linear_tab(self):
        frame = self.linear_tab

        # Matrix size
        size_frame = ttk.Frame(frame)
        size_frame.pack(pady=10)
        size_label = ttk.Label(size_frame, text="Size of Matrix (n):")
        size_label.pack(side=tk.LEFT)
        self.linear_size_entry = ttk.Entry(size_frame, width=5)
        self.linear_size_entry.pack(side=tk.LEFT, padx=5)
        size_button = ttk.Button(size_frame, text="Set", command=self.set_linear_matrix_size)
        size_button.pack(side=tk.LEFT, padx=5)

        # Matrix input
        self.linear_matrix_frame = ttk.Frame(frame)
        self.linear_matrix_frame.pack(pady=10)

        # Constants input
        constants_label = ttk.Label(frame, text="Constants (separated by space):")
        constants_label.pack()
        self.linear_constants_entry = ttk.Entry(frame, width=50)
        self.linear_constants_entry.pack()

        # Solve button
        solve_button = ttk.Button(frame, text="Solve System", command=self.solve_linear_system)
        solve_button.pack(pady=10)

        # Result display
        self.linear_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.linear_result.pack(pady=10)

    def set_linear_matrix_size(self):
        size = self.linear_size_entry.get()
        if not size.isdigit() or int(size) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for matrix size.")
            return
        self.linear_matrix_size = int(size)
        # Clear previous matrix entries
        for widget in self.linear_matrix_frame.winfo_children():
            widget.destroy()
        # Create new matrix entries
        self.linear_matrix_entries = []
        for i in range(self.linear_matrix_size):
            row_entries = []
            for j in range(self.linear_matrix_size):
                entry = ttk.Entry(self.linear_matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.linear_matrix_entries.append(row_entries)

    def solve_linear_system(self):
        la = LinearAlgebra()
        try:
            if not hasattr(self, 'linear_matrix_size'):
                raise ValueError("Please set the matrix size first.")
            # Extract matrix
            matrix = []
            for row_entries in self.linear_matrix_entries:
                row = []
                for entry in row_entries:
                    val = float(entry.get())
                    row.append(val)
                matrix.append(row)
            # Extract constants
            constants = self.linear_constants_entry.get().strip().split()
            if len(constants) != self.linear_matrix_size:
                raise ValueError("Number of constants must match the matrix size.")
            constants = [float(c) for c in constants]
            # Solve using Gaussian Elimination
            solutions = la.gaussian_elimination(matrix, constants)
            solutions = [round(x, 6) for x in solutions]
            solution_str = ", ".join([f"x{i+1} = {sol}" for i, sol in enumerate(solutions)])
        except ValueError as ve:
            solution_str = f"Error: {ve}"
        except Exception as e:
            solution_str = f"Error: {e}"

        self.linear_result.configure(state='normal')
        self.linear_result.delete("1.0", tk.END)
        self.linear_result.insert(tk.END, solution_str)
        self.linear_result.configure(state='disabled')

    # ---------------- Vector Operations Tab ---------------- #

    def create_vector_tab(self):
        frame = self.vector_tab

        # Vector 1 input
        v1_label = ttk.Label(frame, text="Vector 1 (space-separated):")
        v1_label.pack(pady=5)
        self.v1_entry = ttk.Entry(frame, width=50)
        self.v1_entry.pack()

        # Vector 2 input
        v2_label = ttk.Label(frame, text="Vector 2 (space-separated):")
        v2_label.pack(pady=5)
        self.v2_entry = ttk.Entry(frame, width=50)
        self.v2_entry.pack()

        # Scalar input
        scalar_label = ttk.Label(frame, text="Scalar (for multiplication):")
        scalar_label.pack(pady=5)
        self.scalar_entry = ttk.Entry(frame, width=20)
        self.scalar_entry.pack()

        # Operation buttons
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(pady=10)

        add_button = ttk.Button(operations_frame, text="Add Vectors", command=self.add_vectors)
        add_button.grid(row=0, column=0, padx=5, pady=5)

        sub_button = ttk.Button(operations_frame, text="Subtract Vectors", command=self.subtract_vectors)
        sub_button.grid(row=0, column=1, padx=5, pady=5)

        dot_button = ttk.Button(operations_frame, text="Dot Product", command=self.dot_product)
        dot_button.grid(row=0, column=2, padx=5, pady=5)

        scalar_button = ttk.Button(operations_frame, text="Scalar Multiply", command=self.scalar_multiply)
        scalar_button.grid(row=0, column=3, padx=5, pady=5)

        # Result display
        self.vector_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.vector_result.pack(pady=10)

    def parse_vector(self, entry):
        return [float(x) for x in entry.strip().split()]

    def add_vectors(self):
        try:
            v1 = self.parse_vector(self.v1_entry.get())
            v2 = self.parse_vector(self.v2_entry.get())
            la = LinearAlgebra()
            result = la.vector_add(v1, v2)
            result_str = f"v1 + v2 = {result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_vector_result(result_str)

    def subtract_vectors(self):
        try:
            v1 = self.parse_vector(self.v1_entry.get())
            v2 = self.parse_vector(self.v2_entry.get())
            la = LinearAlgebra()
            result = la.vector_sub(v1, v2)
            result_str = f"v1 - v2 = {result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_vector_result(result_str)

    def dot_product(self):
        try:
            v1 = self.parse_vector(self.v1_entry.get())
            v2 = self.parse_vector(self.v2_entry.get())
            la = LinearAlgebra()
            result = la.dot_product(v1, v2)
            result_str = f"v1 · v2 = {result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_vector_result(result_str)

    def scalar_multiply(self):
        try:
            scalar = float(self.scalar_entry.get())
            v = self.parse_vector(self.v1_entry.get())
            la = LinearAlgebra()
            result = la.scalar_multiply(scalar, v)
            result_str = f"{scalar} * v1 = {result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_vector_result(result_str)

    def display_vector_result(self, text):
        self.vector_result.configure(state='normal')
        self.vector_result.delete("1.0", tk.END)
        self.vector_result.insert(tk.END, text)
        self.vector_result.configure(state='disabled')

    # ---------------- Matrix Operations Tab ---------------- #

    def create_matrix_tab(self):
        frame = self.matrix_tab

        # Matrix size
        size_frame = ttk.Frame(frame)
        size_frame.pack(pady=10)
        size_label = ttk.Label(size_frame, text="Size of Matrix (n for n x n):")
        size_label.pack(side=tk.LEFT)
        self.matrix_size_entry = ttk.Entry(size_frame, width=5)
        self.matrix_size_entry.pack(side=tk.LEFT, padx=5)
        size_button = ttk.Button(size_frame, text="Set", command=self.set_matrix_operations_size)
        size_button.pack(side=tk.LEFT, padx=5)

        # Matrix A input
        matrix_a_label = ttk.Label(frame, text="Matrix A:")
        matrix_a_label.pack(pady=5)
        self.matrix_a_frame = ttk.Frame(frame)
        self.matrix_a_frame.pack()

        # Matrix B input
        matrix_b_label = ttk.Label(frame, text="Matrix B:")
        matrix_b_label.pack(pady=5)
        self.matrix_b_frame = ttk.Frame(frame)
        self.matrix_b_frame.pack()

        # Operation buttons
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(pady=10)

        add_button = ttk.Button(operations_frame, text="A + B", command=self.add_matrices)
        add_button.grid(row=0, column=0, padx=5, pady=5)

        sub_button = ttk.Button(operations_frame, text="A - B", command=self.subtract_matrices)
        sub_button.grid(row=0, column=1, padx=5, pady=5)

        mul_button = ttk.Button(operations_frame, text="A * B", command=self.multiply_matrices)
        mul_button.grid(row=0, column=2, padx=5, pady=5)

        transpose_button = ttk.Button(operations_frame, text="Transpose A", command=self.transpose_matrix_a)
        transpose_button.grid(row=0, column=3, padx=5, pady=5)

        det_button = ttk.Button(operations_frame, text="Determinant A", command=self.determinant_matrix_a)
        det_button.grid(row=1, column=0, padx=5, pady=5)

        inverse_button = ttk.Button(operations_frame, text="Inverse A", command=self.inverse_matrix_a)
        inverse_button.grid(row=1, column=1, padx=5, pady=5)

        # Result display
        self.matrix_result = tk.Text(frame, height=15, width=80, state='disabled')
        self.matrix_result.pack(pady=10)

    def set_matrix_operations_size(self):
        size = self.matrix_size_entry.get()
        if not size.isdigit() or int(size) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for matrix size.")
            return
        self.matrix_size = int(size)
        # Clear previous matrix entries
        for widget in self.matrix_a_frame.winfo_children():
            widget.destroy()
        for widget in self.matrix_b_frame.winfo_children():
            widget.destroy()
        # Create new matrix entries for A
        self.matrix_a_entries = []
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = ttk.Entry(self.matrix_a_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_a_entries.append(row_entries)
        # Create new matrix entries for B
        self.matrix_b_entries = []
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = ttk.Entry(self.matrix_b_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_b_entries.append(row_entries)

    def get_matrix(self, entries, size):
        matrix = []
        for row_entries in entries:
            row = []
            for entry in row_entries:
                val = float(entry.get())
                row.append(val)
            matrix.append(row)
        return matrix

    def add_matrices(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            B = self.get_matrix(self.matrix_b_entries, self.matrix_size)
            result = la.matrix_add(A, B)
            result_str = f"A + B =\n{result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def subtract_matrices(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            B = self.get_matrix(self.matrix_b_entries, self.matrix_size)
            result = la.matrix_sub(A, B)
            result_str = f"A - B =\n{result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def multiply_matrices(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            B = self.get_matrix(self.matrix_b_entries, self.matrix_size)
            result = la.matrix_multiply(A, B)
            result_str = f"A * B =\n{result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def transpose_matrix_a(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            result = la.transpose(A)
            result_str = f"Transpose of A =\n{result}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def determinant_matrix_a(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            det = la.determinant(A)
            result_str = f"Determinant of A = {det}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def inverse_matrix_a(self):
        try:
            la = LinearAlgebra()
            A = self.get_matrix(self.matrix_a_entries, self.matrix_size)
            inv = la.inverse(A)
            result_str = f"Inverse of A =\n{inv}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.display_matrix_result(result_str)

    def display_matrix_result(self, text):
        self.matrix_result.configure(state='normal')
        self.matrix_result.delete("1.0", tk.END)
        self.matrix_result.insert(tk.END, text)
        self.matrix_result.configure(state='disabled')

    # ---------------- Polynomial Roots Tab ---------------- #

    def create_poly_tab(self):
        frame = self.poly_tab

        # Coefficients input
        coeffs_label = ttk.Label(frame, text="Enter Polynomial Coefficients (constant first, highest degree last, space-separated):")
        coeffs_label.pack(pady=10)
        self.coeffs_entry = ttk.Entry(frame, width=50)
        self.coeffs_entry.pack()

        # Solve button
        solve_button = ttk.Button(frame, text="Find Roots", command=self.find_roots)
        solve_button.pack(pady=10)

        # Result display
        self.poly_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.poly_result.pack(pady=10)

    def find_roots(self):
        coeffs_str = self.coeffs_entry.get()
        try:
            coeffs = [float(c) for c in coeffs_str.strip().split()]
            roots = polynomial_roots(coeffs)
            if not roots:
                result_str = "No real roots."
            else:
                roots = [round(r, 6) for r in roots]
                roots_str = ", ".join([str(r) for r in roots])
                result_str = f"Roots: {roots_str}"
        except Exception as e:
            result_str = f"Error: {e}"

        self.poly_result.configure(state='normal')
        self.poly_result.delete("1.0", tk.END)
        self.poly_result.insert(tk.END, result_str)
        self.poly_result.configure(state='disabled')

    # ---------------- Eigenvalues and Eigenvectors Tab ---------------- #

    def create_eigen_tab(self):
        frame = self.eigen_tab

        # Matrix size
        size_frame = ttk.Frame(frame)
        size_frame.pack(pady=10)
        size_label = ttk.Label(size_frame, text="Size of Matrix (n for n x n, up to 3):")
        size_label.pack(side=tk.LEFT)
        self.eigen_size_entry = ttk.Entry(size_frame, width=5)
        self.eigen_size_entry.pack(side=tk.LEFT, padx=5)
        size_button = ttk.Button(size_frame, text="Set", command=self.set_eigen_matrix_size)
        size_button.pack(side=tk.LEFT, padx=5)

        # Matrix input
        self.eigen_matrix_frame = ttk.Frame(frame)
        self.eigen_matrix_frame.pack(pady=10)

        # Solve button
        solve_button = ttk.Button(frame, text="Find Eigenvalues", command=self.find_eigen)
        solve_button.pack(pady=10)

        # Result display
        self.eigen_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.eigen_result.pack(pady=10)

    def set_eigen_matrix_size(self):
        size = self.eigen_size_entry.get()
        if not size.isdigit() or int(size) <= 0 or int(size) > 3:
            messagebox.showerror("Invalid Input", "Please enter a positive integer (1-3) for matrix size.")
            return
        self.eigen_matrix_size = int(size)
        # Clear previous matrix entries
        for widget in self.eigen_matrix_frame.winfo_children():
            widget.destroy()
        # Create new matrix entries
        self.eigen_matrix_entries = []
        for i in range(self.eigen_matrix_size):
            row_entries = []
            for j in range(self.eigen_matrix_size):
                entry = ttk.Entry(self.eigen_matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.eigen_matrix_entries.append(row_entries)

    def find_eigen(self):
        try:
            if not hasattr(self, 'eigen_matrix_size'):
                raise ValueError("Please set the matrix size first.")
            # Extract matrix
            A = []
            for row_entries in self.eigen_matrix_entries:
                row = []
                for entry in row_entries:
                    val = float(entry.get())
                    row.append(val)
                A.append(row)
            # Find eigenvalues
            lambdas, _ = eigenvalues_eigenvectors(A)
            lambdas = [round(l, 6) for l in lambdas]
            lambdas_str = ", ".join([str(l) for l in lambdas])
            result_str = f"Eigenvalues: {lambdas_str}"
        except Exception as e:
            result_str = f"Error: {e}"
        self.eigen_result.configure(state='normal')
        self.eigen_result.delete("1.0", tk.END)
        self.eigen_result.insert(tk.END, result_str)
        self.eigen_result.configure(state='disabled')

    # ---------------- Gram-Schmidt Orthogonalization Tab ---------------- #

    def create_gram_schmidt_tab(self):
        frame = self.gram_schmidt_tab

        # Vectors input
        vectors_label = ttk.Label(frame, text="Enter Vectors (each vector separated by ';' and elements by space):")
        vectors_label.pack(pady=10)
        self.gram_vectors_entry = ttk.Entry(frame, width=80)
        self.gram_vectors_entry.pack()

        # Orthogonalize button
        orthogonalize_button = ttk.Button(frame, text="Orthogonalize", command=self.orthogonalize_vectors)
        orthogonalize_button.pack(pady=10)

        # Result display
        self.gram_result = tk.Text(frame, height=15, width=80, state='disabled')
        self.gram_result.pack(pady=10)

    def orthogonalize_vectors(self):
        vectors_str = self.gram_vectors_entry.get()
        try:
            vectors = []
            for vec_str in vectors_str.strip().split(';'):
                vec = [float(x) for x in vec_str.strip().split()]
                vectors.append(vec)
            orthogonal_vectors = gram_schmidt(vectors)
            orthogonal_vectors = [[round(x, 6) for x in vec] for vec in orthogonal_vectors]
            result_str = "Orthogonal Vectors:\n"
            for vec in orthogonal_vectors:
                result_str += f"{vec}\n"
        except Exception as e:
            result_str = f"Error: {e}"

        self.gram_result.configure(state='normal')
        self.gram_result.delete("1.0", tk.END)
        self.gram_result.insert(tk.END, result_str)
        self.gram_result.configure(state='disabled')

    # ---------------- Projection Tab ---------------- #

    def create_projection_tab(self):
        frame = self.projection_tab

        # Vector input
        v_label = ttk.Label(frame, text="Vector v (space-separated):")
        v_label.pack(pady=5)
        self.proj_v_entry = ttk.Entry(frame, width=50)
        self.proj_v_entry.pack()

        # Subspace input
        subspace_label = ttk.Label(frame, text="Subspace Vectors (each vector separated by ';' and elements by space):")
        subspace_label.pack(pady=5)
        self.proj_subspace_entry = ttk.Entry(frame, width=80)
        self.proj_subspace_entry.pack()

        # Project button
        project_button = ttk.Button(frame, text="Project", command=self.project_vector)
        project_button.pack(pady=10)

        # Result display
        self.proj_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.proj_result.pack(pady=10)

    def project_vector(self):
        v_str = self.proj_v_entry.get()
        subspace_str = self.proj_subspace_entry.get()
        try:
            v = [float(x) for x in v_str.strip().split()]
            subspace = []
            for vec_str in subspace_str.strip().split(';'):
                vec = [float(x) for x in vec_str.strip().split()]
                subspace.append(vec)
            projection = project_onto_subspace(v, subspace)
            projection = [round(x, 6) for x in projection]
            result_str = f"Projection of v onto subspace: {projection}"
        except Exception as e:
            result_str = f"Error: {e}"

        self.proj_result.configure(state='normal')
        self.proj_result.delete("1.0", tk.END)
        self.proj_result.insert(tk.END, result_str)
        self.proj_result.configure(state='disabled')

# ---------------- Main Function ---------------- #

def main():
    root = tk.Tk()
    app = MathCalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
