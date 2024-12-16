import math
import re
import tkinter as tk
from tkinter import ttk, messagebox

#----------------------------------------------------------
# Helper Functions
#----------------------------------------------------------

def is_square_matrix(M):
    return len(M) > 0 and all(len(row) == len(M) for row in M)

def copy_matrix(M):
    return [row[:] for row in M]

def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def matrix_multiply(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    result = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            s = 0
            for k in range(n):
                s += A[i][k]*B[k][j]
            result[i][j] = s
    return result

def matrix_minor(M, i, j):
    return [row[:j] + row[j+1:] for idx, row in enumerate(M) if idx != i]

def matrix_determinant(M):
    n = len(M)
    if n == 1:
        return M[0][0]
    if n == 2:
        return M[0][0]*M[1][1] - M[0][1]*M[1][0]
    det = 0
    for j in range(n):
        det += ((-1)**j)*M[0][j]*matrix_determinant(matrix_minor(M,0,j))
    return det

def matrix_identity(n):
    return [[1 if i==j else 0 for j in range(n)] for i in range(n)]

def matrix_swap_rows(M, r1, r2):
    M[r1], M[r2] = M[r2], M[r1]

def matrix_scale_row(M, r, s):
    M[r] = [x*s for x in M[r]]

def matrix_add_multiple_of_row(M, r1, r2, s):
    M[r1] = [x1 + s*x2 for x1, x2 in zip(M[r1], M[r2])]

def RREF(M):
    A = copy_matrix(M)
    if len(A)==0 or len(A[0])==0:
        return A
    rows = len(A)
    cols = len(A[0])
    r = 0
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if abs(A[i][c]) > 1e-14:
                pivot = i
                break
        if pivot is None:
            continue
        if pivot != r:
            matrix_swap_rows(A, r, pivot)
        pivot_val = A[r][c]
        matrix_scale_row(A, r, 1.0/pivot_val)
        for i in range(rows):
            if i!=r:
                if abs(A[i][c])>1e-14:
                    factor = -A[i][c]
                    matrix_add_multiple_of_row(A, i, r, factor)
        r += 1
        if r == rows:
            break
    return A

def solve_linear_system(A, b):
    M = [A[i] + b[i] for i in range(len(A))]
    M = RREF(M)
    n = len(A[0])
    x = [0]*n
    for i in range(n):
        x[i] = M[i][n]
    return x

def solve_cramers_rule(A, b):
    detA = matrix_determinant(A)
    if abs(detA)<1e-14:
        return None
    n = len(A)
    x = []
    for i in range(n):
        Ai = [row[:] for row in A]
        for j in range(n):
            Ai[j][i] = b[j][0]
        x.append(matrix_determinant(Ai)/detA)
    return x

def change_of_basis(v, old_basis, new_basis):
    n = len(old_basis)
    v_std = [0]*n
    for i in range(n):
        for j in range(n):
            v_std[j] += v[i]*old_basis[i][j]
    b = [[x] for x in v_std]
    x = solve_linear_system(new_basis, b)
    return x

def char_poly_coefficients(A):
    n = len(A)
    if n == 1:
        return [-A[0][0], 1]
    elif n == 2:
        trace = A[0][0]+A[1][1]
        detA = matrix_determinant(A)
        return [detA, -trace, 1]
    elif n == 3:
        tr = A[0][0]+A[1][1]+A[2][2]
        m1 = matrix_determinant([[A[1][1],A[1][2]],[A[2][1],A[2][2]]])
        m2 = matrix_determinant([[A[0][0],A[0][2]],[A[2][0],A[2][2]]])
        m3 = matrix_determinant([[A[0][0],A[0][1]],[A[1][0],A[1][1]]])
        sum_2x2 = m1+m2+m3
        detA = matrix_determinant(A)
        return [-detA, sum_2x2, -tr, 1]
    else:
        raise NotImplementedError("Characteristic polynomial only implemented up to 3x3 matrices.")

def polynomial_roots(coeffs):
    n = len(coeffs)-1
    if n == 1:
        return [-coeffs[0]/coeffs[1]]
    elif n == 2:
        a=coeffs[2]; b=coeffs[1]; c=coeffs[0]
        disc = b*b -4*a*c
        if disc<0:
            return []
        elif abs(disc)<1e-14:
            return [-b/(2*a)]
        else:
            sqrt_disc = math.sqrt(disc)
            return [(-b+sqrt_disc)/(2*a), (-b - sqrt_disc)/(2*a)]
    elif n == 3:
        # Simple numeric approach (approx)
        def poly_val(x):
            val=0
            for i,c in enumerate(coeffs):
                val+=c*(x**i)
            return val
        xs=[-10+i*0.5 for i in range(41)]
        vals=[poly_val(x) for x in xs]
        roots=[]
        for i in range(len(xs)-1):
            if vals[i]*vals[i+1]<0:
                low=xs[i]; high=xs[i+1]
                for _ in range(50):
                    mid=(low+high)/2
                    vm=poly_val(mid)
                    if abs(vm)<1e-12:
                        roots.append(mid)
                        break
                    if vals[i]*vm<0:
                        high=mid
                    else:
                        low=mid
                else:
                    roots.append((low+high)/2)
        return roots
    else:
        raise NotImplementedError("Roots only implemented up to cubic.")

def eigenvalues_eigenvectors(A):
    coeffs = char_poly_coefficients(A)
    lambdas = polynomial_roots(coeffs)
    eigenvals = []
    eigenvecs = []
    n=len(A)
    for lam in lambdas:
        M=[row[:] for row in A]
        for i in range(n):
            M[i][i]=M[i][i]-lam
        M=RREF(M)
        rank=0
        for row in M:
            if any(abs(x)>1e-14 for x in row):
                rank+=1
        # number of free variables:
        free_vars_count = n - rank
        # Construct a basis for the nullspace:
        # Let's pick free variables as needed.
        # For simplicity, let’s just pick one eigenvector if possible.
        if free_vars_count<1:
            # No free variable means maybe all zero? This would be strange, might mean lam not eigenvalue.
            # We skip if we can't find an eigenvector
            continue

        # Identify pivot columns
        pivot_positions=[]
        for i,row in enumerate(M):
            pivot_col=None
            for j,val in enumerate(row[:-1]):
                if abs(val)>1e-14:
                    pivot_col=j
                    break
            if pivot_col is not None:
                pivot_positions.append(pivot_col)

        # Free columns are those not in pivot positions
        all_cols=set(range(n))
        pivot_cols=set(pivot_positions)
        free_cols=list(all_cols - pivot_cols)
        # Set one free variable = 1, others =0 for simplicity
        xvec=[0]*n
        if len(free_cols)>0:
            xvec[free_cols[0]]=1.0

        # Solve for pivot variables
        # Back substitution
        # M is in RREF: each pivot row looks like [0...1...rest... | last]
        for i in reversed(range(rank)):
            row=M[i]
            # find pivot
            pivot_col=None
            for j,val in enumerate(row[:-1]):
                if abs(val)>1e-14:
                    pivot_col=j
                    break
            if pivot_col is None:
                # no pivot in this row, skip
                continue
            s=0
            for k in range(pivot_col+1,n):
                s+=row[k]*xvec[k]
            xvec[pivot_col]= -s

        norm = math.sqrt(sum(e*e for e in xvec))
        if abs(norm)<1e-14:
            # Try another free variable if norm=0
            for fc in free_cols[1:]:
                xvec=[0]*n
                xvec[fc]=1.0
                for i in reversed(range(rank)):
                    row=M[i]
                    pivot_col=None
                    for j,val in enumerate(row[:-1]):
                        if abs(val)>1e-14:
                            pivot_col=j
                            break
                    if pivot_col is not None:
                        s=0
                        for k in range(pivot_col+1,n):
                            s+=row[k]*xvec[k]
                        xvec[pivot_col]= -s
                norm=math.sqrt(sum(e*e for e in xvec))
                if abs(norm)>1e-14:
                    break

        if abs(norm)>1e-14:
            xvec=[e/norm for e in xvec]
        else:
            # If still norm is zero, fallback:
            xvec=[1 if i==0 else 0 for i in range(n)]

        eigenvals.append(lam)
        eigenvecs.append(xvec)
    return eigenvals, eigenvecs

def LU_decomposition(A):
    n = len(A)
    L = matrix_identity(n)
    U = [[0]*n for _ in range(n)]
    for i in range(n):
        for k in range(i,n):
            s=0
            for r in range(i):
                s+=L[i][r]*U[r][k]
            U[i][k]=A[i][k]-s
        for k in range(i+1,n):
            s=0
            for r in range(i):
                s+=L[k][r]*U[r][i]
            if abs(U[i][i])<1e-14:
                raise ValueError("LU decomposition failed: zero pivot")
            L[k][i]=(A[k][i]-s)/U[i][i]
    return L,U

def gram_schmidt(V):
    U=[]
    for v in V:
        v_copy=v[:]
        for u in U:
            dot_vu=sum(x*y for x,y in zip(v_copy,u))
            v_copy = [x - dot_vu*u_el for x,u_el in zip(v_copy,u)]
        norm=math.sqrt(sum(x*x for x in v_copy))
        if abs(norm)>1e-14:
            U.append([x/norm for x in v_copy])
    return U

def project_onto_subspace(v, subspace):
    Q=gram_schmidt(subspace)
    proj=[0]*len(v)
    for q in Q:
        dot_vq=sum(x*y for x,y in zip(v,q))
        proj=[pv+dot_vq*qv for pv,qv in zip(proj,q)]
    return proj

def SVD(A):
    At = [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]
    AtA = matrix_multiply(At,A)
    vals, vecs = eigenvalues_eigenvectors(AtA)
    sorted_eigs = sorted(zip(vals,vecs), key=lambda x: x[0], reverse=True)
    vals = [x[0] for x in sorted_eigs]
    vecs = [x[1] for x in sorted_eigs]
    svals=[math.sqrt(abs(v)) for v in vals]
    V = [list(v) for v in zip(*vecs)]
    invS = [[0]*len(V) for _ in range(len(A))]
    for i in range(min(len(A), len(V))):
        if abs(svals[i])>1e-14:
            invS[i][i]=1.0/svals[i]
    AV = matrix_multiply(A,V)
    U = matrix_multiply(AV,invS)
    Σ = [[0]*len(V[0]) for _ in range(len(U))]
    for i in range(min(len(U), len(V[0]))):
        Σ[i][i]=svals[i]
    return U, Σ, V

def jordan_normal_form(A):
    vals, vecs = eigenvalues_eigenvectors(A)
    n = len(A)
    # If we don't have enough eigenvectors, just form a Jordan block
    if len(vecs)<n:
        lam=vals[0] if len(vals)>0 else 0
        if n==2:
            J=[[lam,1],[0,lam]]
        elif n==3:
            J=[[lam,1,0],[0,lam,1],[0,0,lam]]
        else:
            raise NotImplementedError("Jordan form only implemented for up to 3x3.")
        return J
    else:
        # Diagonal if full set of eigenvectors
        J=[[0]*n for _ in range(n)]
        for i,lam in enumerate(vals):
            J[i][i]=lam
        return J

def solve_conic_equation(A,B,C,D,E,F, var='y', x_val=None, y_val=None):
    if var=='y' and x_val is not None:
        a = C
        b = B*x_val + E
        c = A*(x_val**2) + D*x_val + F
        if abs(a)<1e-14:
            if abs(b)<1e-14:
                return [] if abs(c)>1e-14 else ['All y']
            return [-c/b]
        disc = b*b - 4*a*c
        if disc<0:
            return []
        elif abs(disc)<1e-14:
            return [-b/(2*a)]
        else:
            sq=math.sqrt(disc)
            return [(-b+sq)/(2*a), (-b - sq)/(2*a)]
    elif var=='x' and y_val is not None:
        a = A
        b = B*y_val + D
        c = C*(y_val**2) + E*y_val + F
        if abs(a)<1e-14:
            if abs(b)<1e-14:
                return [] if abs(c)>1e-14 else ['All x']
            return [-c/b]
        disc = b*b -4*a*c
        if disc<0:
            return []
        elif abs(disc)<1e-14:
            return [-b/(2*a)]
        else:
            sq=math.sqrt(disc)
            return [(-b+sq)/(2*a), (-b - sq)/(2*a)]
    else:
        return []

# Polynomial formatting
def polynomial_to_string_desc(rev_coeffs):
    # rev_coeffs: [c_n, c_{n-1}, ..., c_0]
    # corresponds to c_n*x^n + ... + c_1*x + c_0
    terms = []
    n = len(rev_coeffs)-1
    for i, c in enumerate(rev_coeffs):
        power = n - i
        if abs(c) < 1e-14:
            continue
        abs_c = abs(c)
        # Construct term
        if power == 0:
            term = f"{abs_c}"
        elif power == 1:
            term = (f"x" if abs_c==1 else f"{abs_c}x")
        else:
            term = (f"x^{power}" if abs_c==1 else f"{abs_c}x^{power}")

        # Determine sign
        if i == 0:
            # first term
            if c<0:
                terms.append(f"- {term}")
            else:
                terms.append(f"{term}")
        else:
            if c<0:
                terms.append(f"- {term}")
            else:
                terms.append(f"+ {term}")
    poly_str = " ".join(terms)
    poly_str = poly_str.replace("+ -","- ")
    return poly_str.strip()

#----------------------------------------------------------
# GUI with Tkinter
#----------------------------------------------------------

class LinearAlgebraApp:
    def __init__(self, master):
        self.master = master
        master.title("Linear Algebra Solver")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill='both', expand=True)

        self.tabs = {}
        operations = [
            ("Matrix Sum/Multiply", self.build_sum_mult_tab),
            ("Determinant", self.build_det_tab),
            ("Solve SLE (RREF/Cramer)", self.build_sle_tab),
            ("Change of Basis", self.build_cob_tab),
            ("Characteristic Poly/Eig", self.build_eig_tab),
            ("SVD/LU", self.build_svd_lu_tab),
            ("Projection (Gram-Schmidt)", self.build_proj_tab),
            ("Jordan Form", self.build_jordan_tab),
            ("Conic Solver", self.build_conic_tab)
        ]
        for op, builder in operations:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=op)
            self.tabs[op]=frame
            builder(frame)

    def parse_matrix(self, text):
        text = text.strip()
        if not text:
            return []
        rows = text.split(';')
        M=[]
        for row in rows:
            if row.strip()=='':
                continue
            vals = [float(x.strip()) for x in row.strip().split(',') if x.strip()!='']
            M.append(vals)
        return M

    def parse_vector(self, text):
        text=text.strip()
        if not text:
            return []
        return [float(x.strip()) for x in text.split(',') if x.strip()!='']

    def build_sum_mult_tab(self, frame):
        ttk.Label(frame, text="Matrix A (rows separated by ';' and columns by ',')").pack()
        self.A_sum_mult = tk.Text(frame, height=5)
        self.A_sum_mult.pack()
        ttk.Label(frame, text="Matrix B").pack()
        self.B_sum_mult = tk.Text(frame, height=5)
        self.B_sum_mult.pack()

        button_frame = ttk.Frame(frame)
        button_frame.pack()

        ttk.Button(button_frame, text="A+B", command=self.compute_A_plus_B).pack(side='left', padx=5)
        ttk.Button(button_frame, text="A*B", command=self.compute_A_times_B).pack(side='left', padx=5)

        self.result_sum_mult = tk.Text(frame, height=5, bg='lightyellow')
        self.result_sum_mult.pack()

    def compute_A_plus_B(self):
        A = self.parse_matrix(self.A_sum_mult.get("1.0", tk.END))
        B = self.parse_matrix(self.B_sum_mult.get("1.0", tk.END))
        if len(A)==0 or len(B)==0:
            messagebox.showerror("Error","Empty matrix")
            return
        if len(A)!=len(B) or len(A[0])!=len(B[0]):
            messagebox.showerror("Error","Matrices must have same dimension")
            return
        R=matrix_add(A,B)
        self.result_sum_mult.delete("1.0",tk.END)
        self.result_sum_mult.insert(tk.END, R)

    def compute_A_times_B(self):
        A = self.parse_matrix(self.A_sum_mult.get("1.0", tk.END))
        B = self.parse_matrix(self.B_sum_mult.get("1.0", tk.END))
        if len(A)==0 or len(B)==0:
            messagebox.showerror("Error","Empty matrix")
            return
        if len(A[0])!=len(B):
            messagebox.showerror("Error","Inner dimensions must match")
            return
        R=matrix_multiply(A,B)
        self.result_sum_mult.delete("1.0",tk.END)
        self.result_sum_mult.insert(tk.END, R)

    def build_det_tab(self, frame):
        ttk.Label(frame, text="Matrix M").pack()
        self.M_det = tk.Text(frame, height=5)
        self.M_det.pack()
        ttk.Button(frame, text="Compute Determinant", command=self.compute_det).pack()
        self.res_det = tk.Label(frame, text="")
        self.res_det.pack()

    def compute_det(self):
        M = self.parse_matrix(self.M_det.get("1.0", tk.END))
        if not is_square_matrix(M):
            messagebox.showerror("Error","Matrix must be square")
            return
        d = matrix_determinant(M)
        self.res_det.config(text=f"Det = {d}")

    def build_sle_tab(self, frame):
        ttk.Label(frame, text="Coefficient Matrix A").pack()
        self.A_sle = tk.Text(frame, height=5)
        self.A_sle.pack()
        ttk.Label(frame, text="Vector b").pack()
        self.b_sle = tk.Text(frame, height=2)
        self.b_sle.pack()
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        ttk.Button(button_frame, text="Solve (RREF)", command=self.solve_SLE_rref).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Solve (Cramer)", command=self.solve_SLE_cramer).pack(side='left', padx=5)
        self.res_sle = tk.Label(frame, text="")
        self.res_sle.pack()

    def solve_SLE_rref(self):
        A = self.parse_matrix(self.A_sle.get("1.0", tk.END))
        b_vec = self.parse_vector(self.b_sle.get("1.0",tk.END))
        if len(A)==0 or len(b_vec)==0:
            messagebox.showerror("Error","Empty input")
            return
        if len(A)!=len(b_vec):
            messagebox.showerror("Error","Dimensions mismatch")
            return
        b = [[x] for x in b_vec]
        x = solve_linear_system(A,b)
        self.res_sle.config(text=f"Solution: {x}")

    def solve_SLE_cramer(self):
        A = self.parse_matrix(self.A_sle.get("1.0", tk.END))
        b_vec = self.parse_vector(self.b_sle.get("1.0",tk.END))
        if len(A)==0 or len(b_vec)==0:
            messagebox.showerror("Error","Empty input")
            return
        if len(A)!=len(b_vec):
            messagebox.showerror("Error","Dimensions mismatch")
            return
        b = [[x] for x in b_vec]
        x = solve_cramers_rule(A,b)
        self.res_sle.config(text=f"Solution: {x}")

    def build_cob_tab(self, frame):
        ttk.Label(frame, text="Old Basis (rows of basis vectors)").pack()
        self.old_basis_txt = tk.Text(frame, height=5)
        self.old_basis_txt.pack()
        ttk.Label(frame, text="New Basis").pack()
        self.new_basis_txt = tk.Text(frame, height=5)
        self.new_basis_txt.pack()
        ttk.Label(frame, text="Vector v in old basis coords (comma separated)").pack()
        self.v_cob_txt = tk.Entry(frame)
        self.v_cob_txt.pack()

        ttk.Button(frame, text="Change Basis", command=self.compute_cob).pack()
        self.res_cob = tk.Label(frame, text="")
        self.res_cob.pack()

    def compute_cob(self):
        old_b = self.parse_matrix(self.old_basis_txt.get("1.0", tk.END))
        new_b = self.parse_matrix(self.new_basis_txt.get("1.0", tk.END))
        v = self.parse_vector(self.v_cob_txt.get())
        if len(old_b)!=len(v) or len(new_b)!=len(v):
            messagebox.showerror("Error","Dimension mismatch")
            return
        v_new = change_of_basis(v, old_b, new_b)
        self.res_cob.config(text=f"v in new basis: {v_new}")

    def build_eig_tab(self, frame):
        ttk.Label(frame, text="Matrix A").pack()
        self.A_eig = tk.Text(frame, height=5)
        self.A_eig.pack()
        ttk.Button(frame, text="Compute Characteristic Poly", command=self.comp_charpoly).pack()
        ttk.Button(frame, text="Eigenvalues/Eigenvectors", command=self.comp_eig).pack()
        self.res_eig = tk.Label(frame, text="")
        self.res_eig.pack()

    def comp_charpoly(self):
        A = self.parse_matrix(self.A_eig.get("1.0", tk.END))
        if not A:
            messagebox.showerror("Error","Empty matrix")
            return
        try:
            coeffs = char_poly_coefficients(A)
            # coeffs are in ascending order: c0 + c1*x + c2*x^2 ...
            # We want to print in descending order:
            rev_coeffs = list(reversed(coeffs))
            poly_str = polynomial_to_string_desc(rev_coeffs)
            self.res_eig.config(text=f"Char poly: {poly_str}")
        except NotImplementedError as e:
            self.res_eig.config(text=str(e))

    def comp_eig(self):
        A = self.parse_matrix(self.A_eig.get("1.0", tk.END))
        try:
            vals, vecs = eigenvalues_eigenvectors(A)
            self.res_eig.config(text=f"Eigenvalues: {vals}\nEigenvectors: {vecs}")
        except NotImplementedError as e:
            self.res_eig.config(text=str(e))

    def build_svd_lu_tab(self, frame):
        ttk.Label(frame, text="Matrix A").pack()
        self.A_svd = tk.Text(frame, height=5)
        self.A_svd.pack()
        button_frame = ttk.Frame(frame)
        button_frame.pack()
        ttk.Button(button_frame, text="SVD", command=self.comp_svd).pack(side='left', padx=5)
        ttk.Button(button_frame, text="LU Decomposition", command=self.comp_lu).pack(side='left', padx=5)
        self.res_svd = tk.Label(frame, text="")
        self.res_svd.pack()

    def comp_svd(self):
        A = self.parse_matrix(self.A_svd.get("1.0", tk.END))
        U,S,V = SVD(A)
        self.res_svd.config(text=f"U={U}\nS={S}\nV={V}")

    def comp_lu(self):
        A = self.parse_matrix(self.A_svd.get("1.0", tk.END))
        L,U = LU_decomposition(A)
        self.res_svd.config(text=f"L={L}\nU={U}")

    def build_proj_tab(self, frame):
        ttk.Label(frame, text="Subspace vectors (rows)").pack()
        self.subspace_txt = tk.Text(frame, height=5)
        self.subspace_txt.pack()
        ttk.Label(frame, text="Vector v").pack()
        self.v_proj_txt = tk.Entry(frame)
        self.v_proj_txt.pack()
        ttk.Button(frame, text="Project", command=self.compute_projection).pack()
        self.res_proj = tk.Label(frame, text="")
        self.res_proj.pack()

    def compute_projection(self):
        sub = self.parse_matrix(self.subspace_txt.get("1.0", tk.END))
        v = self.parse_vector(self.v_proj_txt.get())
        p = project_onto_subspace(v, sub)
        self.res_proj.config(text=f"Projection: {p}")

    def build_jordan_tab(self, frame):
        ttk.Label(frame, text="Matrix A").pack()
        self.A_jord = tk.Text(frame, height=5)
        self.A_jord.pack()
        ttk.Button(frame, text="Jordan Normal Form", command=self.compute_jordan).pack()
        self.res_jord = tk.Label(frame, text="")
        self.res_jord.pack()

    def compute_jordan(self):
        A = self.parse_matrix(self.A_jord.get("1.0", tk.END))
        try:
            J = jordan_normal_form(A)
            self.res_jord.config(text=f"Jordan form: {J}")
        except NotImplementedError as e:
            self.res_jord.config(text=str(e))
        except Exception as e:
            self.res_jord.config(text=f"Error: {e}")

    def build_conic_tab(self, frame):
        ttk.Label(frame, text="Conic: A x² + B x y + C y² + D x + E y + F =0").pack()
        entries_frame = ttk.Frame(frame)
        entries_frame.pack()
        self.conic_A = tk.Entry(entries_frame,width=5)
        self.conic_B = tk.Entry(entries_frame,width=5)
        self.conic_C = tk.Entry(entries_frame,width=5)
        self.conic_D = tk.Entry(entries_frame,width=5)
        self.conic_E = tk.Entry(entries_frame,width=5)
        self.conic_F = tk.Entry(entries_frame,width=5)
        for i,(lbl,e) in enumerate([("A",self.conic_A),("B",self.conic_B),("C",self.conic_C),("D",self.conic_D),("E",self.conic_E),("F",self.conic_F)]):
            ttk.Label(entries_frame,text=lbl).grid(row=0,column=2*i)
            e.grid(row=0,column=2*i+1)

        solve_frame = ttk.Frame(frame)
        solve_frame.pack()
        ttk.Label(solve_frame, text="Solve for: ").pack(side='left')
        self.var_conic = tk.StringVar()
        self.var_conic.set('y')
        tk.Radiobutton(solve_frame, text='y', variable=self.var_conic, value='y').pack(side='left')
        tk.Radiobutton(solve_frame, text='x', variable=self.var_conic, value='x').pack(side='left')

        ttk.Label(solve_frame, text="Given value:").pack(side='left')
        self.conic_val_entry = tk.Entry(solve_frame,width=10)
        self.conic_val_entry.pack(side='left')

        ttk.Button(frame, text="Solve Conic", command=self.solve_conic).pack()
        self.res_conic = tk.Label(frame, text="")
        self.res_conic.pack()

    def solve_conic(self):
        try:
            A=float(self.conic_A.get())
            B=float(self.conic_B.get())
            C=float(self.conic_C.get())
            D=float(self.conic_D.get())
            E=float(self.conic_E.get())
            F=float(self.conic_F.get())
        except:
            messagebox.showerror("Error","Invalid conic coefficients")
            return
        var=self.var_conic.get()
        val_str=self.conic_val_entry.get().strip()
        if not val_str:
            messagebox.showerror("Error","Please provide a value")
            return
        val=float(val_str)
        if var=='y':
            solutions = solve_conic_equation(A,B,C,D,E,F,var='y', x_val=val)
        else:
            solutions = solve_conic_equation(A,B,C,D,E,F,var='x', y_val=val)
        self.res_conic.config(text=f"Solutions: {solutions}")


if __name__ == "__main__":
    root = tk.Tk()
    app = LinearAlgebraApp(root)
    root.mainloop()
