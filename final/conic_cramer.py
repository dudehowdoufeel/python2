import math
import re
import tkinter as tk
from tkinter import ttk, messagebox

#conic functions

def sintax(equation):
    #remove spaces and split at '=' to get the left-hand side
    equation = equation.replace(" ", "").split("=")[0]
    
    #replace '-' with '+-' to simplify splitting
    equation = equation.replace("-", "+-")
    
    #remove leading '+' if present
    if equation.startswith("+"):
        equation = equation[1:]
    
    #split the equation into parts based on '+'
    parts = equation.split("+")
    
    #initialize coefficients
    coefficients = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}
    
    #regex to identify terms
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
    disc = B**2 - 4*A*C  #discriminant
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
        return A, B, C, 0  #no rotation needed
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
        #determine the sign to place with a_sq
        if F_new / A_new > 0:
            canonical = f"((x - {x0})²) / {a_sq} - ((y - {y0})²) / {b_sq} = 1"
        else:
            canonical = f"((y - {y0})²) / {b_sq} - ((x - {x0})²) / {a_sq} = 1"
        return conic_type, canonical
    
    elif conic_type == "Parabola":
        canonical = canonical_parabola(A, C, D, E, F)
        return conic_type, canonical

#linear system solver func

def determinant(matrix):
    #recursive function to calculate determinant
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    
    det = 0
    for col in range(n):
        #create minor matrix
        minor = []
        for row in range(1, n):
            minor_row = []
            for c in range(n):
                if c != col:
                    minor_row.append(matrix[row][c])
            minor.append(minor_row)
        #recursive call
        det += ((-1) ** col) * matrix[0][col] * determinant(minor)
    return det

def cramer(matrix, constants):
    n = len(matrix)
    det_main = determinant(matrix)
    if det_main == 0:
        raise ValueError("Determinant is zero, the system has no unique solution.")
    
    solutions = []
    for col in range(n):
        #create modified matrix by replacing column 'col' with constants
        modified_matrix = []
        for row in range(n):
            modified_row = matrix[row].copy()
            modified_row[col] = constants[row]
            modified_matrix.append(modified_row)
        det_modified = determinant(modified_matrix)
        solutions.append(det_modified / det_main)
    return solutions

def input_system(size, matrix_entries, constants_entry):
    matrix = []
    try:
        for row_entries in matrix_entries:
            row = []
            for entry in row_entries:
                val = float(entry.get())
                row.append(val)
            matrix.append(row)
    except ValueError:
        raise ValueError("All matrix coefficients must be valid numbers.")
    
    constants = constants_entry.get().strip().split()
    if len(constants) != size:
        raise ValueError("Number of constants must match the matrix size.")
    try:
        constants = [float(c) for c in constants]
    except ValueError:
        raise ValueError("All constants must be valid numbers.")
    
    return matrix, constants

#interface by tkinter
class ConicSolverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conic & Linear System Solver")
        self.create_widgets()

    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)

        #tab for Conic Classification
        self.conic_tab = ttk.Frame(tab_control)
        tab_control.add(self.conic_tab, text='Conic Classification')
        self.create_conic_tab()

        #tab for Linear System Solver
        self.linear_tab = ttk.Frame(tab_control)
        tab_control.add(self.linear_tab, text='Linear System Solver')
        self.create_linear_tab()

        tab_control.pack(expand=1, fill="both")

#conic tab
    def create_conic_tab(self):
        frame = self.conic_tab

        #equation input
        equation_label = ttk.Label(frame, text="Enter Conic Equation:")
        equation_label.pack(pady=10)
        self.equation_entry = ttk.Entry(frame, width=50)
        self.equation_entry.pack()

        #solve button
        solve_button = ttk.Button(frame, text="Classify & Canonical Form", command=self.solve_conic)
        solve_button.pack(pady=10)

        #result display
        self.conic_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.conic_result.pack(pady=10)

    def solve_conic(self):
        equation = self.equation_entry.get()
        try:
            conic_type, canonical = get_conic_info(equation)
            result_text = f"Conic Type: {conic_type}\nCanonical Form: {canonical}"
        except Exception as e:
            result_text = f"Error: {e}"

        self.conic_result.configure(state='normal')
        self.conic_result.delete("1.0", tk.END)
        self.conic_result.insert(tk.END, result_text)
        self.conic_result.configure(state='disabled')

#cramer tab
    def create_linear_tab(self):
        frame = self.linear_tab

        #matrix size
        size_frame = ttk.Frame(frame)
        size_frame.pack(pady=10)
        size_label = ttk.Label(size_frame, text="Size of Matrix (n):")
        size_label.pack(side=tk.LEFT)
        self.size_entry = ttk.Entry(size_frame, width=5)
        self.size_entry.pack(side=tk.LEFT, padx=5)
        size_button = ttk.Button(size_frame, text="Set", command=self.set_matrix_size)
        size_button.pack(side=tk.LEFT, padx=5)

        #matrix input
        self.matrix_frame = ttk.Frame(frame)
        self.matrix_frame.pack(pady=10)

        #constants input
        constants_label = ttk.Label(frame, text="Constants (separated by space):")
        constants_label.pack()
        self.constants_entry = ttk.Entry(frame, width=50)
        self.constants_entry.pack()

        #solve button
        solve_button = ttk.Button(frame, text="Solve System", command=self.solve_linear_system)
        solve_button.pack(pady=10)

        #result display
        self.linear_result = tk.Text(frame, height=10, width=60, state='disabled')
        self.linear_result.pack(pady=10)

    def set_matrix_size(self):
        size = self.size_entry.get()
        if not size.isdigit() or int(size) <= 0:
            messagebox.showerror("Invalid Input", "Please enter a positive integer for matrix size.")
            return
        self.matrix_size = int(size)
        #clear previous matrix entries
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
        #create new matrix entries
        self.matrix_entries = []
        for i in range(self.matrix_size):
            row_entries = []
            for j in range(self.matrix_size):
                entry = ttk.Entry(self.matrix_frame, width=5)
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def solve_linear_system(self):
        try:
            if not hasattr(self, 'matrix_size'):
                raise ValueError("Please set the matrix size first.")
            matrix, constants = input_system(self.matrix_size, self.matrix_entries, self.constants_entry)
            solutions = cramer(matrix, constants)
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

#main
def main():
    root = tk.Tk()
    app = ConicSolverApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
#4x^2-y^2-16x-6y+3=0 hyperbola
#9x^2+16y^2-54x+64y+1=0 ellipse
#x^2 + y^2 - 4 = 0
#-x^2+2x+7-y=0 parabola
#x^2+4x-8y+16=0 parabola
#y^2-4x-6y+9=0 parabola