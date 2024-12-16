import math

def sintax(equation):
    equation=equation.replace(" ", "").split("=")[0] #remove spaces and defined positive and negative signs 

    equation=equation.replace("-", "+-")

    if equation.startswith("+"):
        equation=equation[1:]
    parts=equation.split("+")
    coefficients={"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

    for part in parts:
        if not part:
            continue
        if "x^2" in part:
            coefficients["A"]=float(part.replace("x^2", "1") if part in ["x^2", "-x^2"] else part.replace("x^2", ""))
        elif "xy" in part:
            coefficients["B"]=float(part.replace("xy", "1") if part in ["xy", "-xy"] else part.replace("xy", ""))
        elif "y^2" in part:
            coefficients["C"]=float(part.replace("y^2", "1") if part in ["y^2", "-y^2"] else part.replace("y^2", ""))
        elif "x" in part and "^" not in part:
            coefficients["D"]=float(part.replace("x", "1") if part in ["x", "-x"] else part.replace("x", ""))
        elif "y" in part and "^" not in part:
            coefficients["E"]=float(part.replace("y", "1") if part in ["y", "-y"] else part.replace("y", ""))
        else:
            coefficients["F"]=float(part)

    return coefficients["A"], coefficients["B"], coefficients["C"], coefficients["D"], coefficients["E"], coefficients["F"]

def classify_conic(A, B, C):
    disc=B**2-4*A*C    #classify the type of conic by discriminant
    if disc<0:
        if A==C and B==0:
            return "circle"
        return "ellipse"
    elif disc==0:
        return "parabola"
    else:
        return "hyperbola"

def rotate_conic(A, B, C):
    if B==0: #rotation to find Bxy term
        return A, B, C, 0
    angle=0.5*math.atan2(B,A-C)
    cos_t=math.cos(angle)
    sin_t=math.sin(angle)
    A_new=A*cos_t**2-B*cos_t*sin_t+C*sin_t**2
    C_new=A*sin_t**2+B*cos_t*sin_t+C*cos_t**2
    return A_new, 0, C_new, angle

def translate_conic(A, C, D, E, F):
    x0=-D/(2*A) if A != 0 else 0 #move the conic center to x0,y0
    y0=-E/(2*C) if C != 0 else 0
    F_new=F+A*x0**2+C*y0**2+D*x0+E*y0
    return F_new, x0, y0

def canonical_parabola(A, C, D, E, F):
    if A != 0 and C == 0:  # y^2 = 4px type
        x0 = -D / (2 * A)
        p = -E / (2 * A)
        return f"(y-{p})^2 = {4 * A}(x-{x0})"
    elif C != 0 and A == 0:  # x^2 = 4py type
        y0 = -E / (2 * C)
        p = -D / (2 * C)
        return f"(x-{p})^2 = {4 * C}(y-{y0})"
    else:
        return "can't simplify to canonical form"

def to_canonical_form(A, B, C, D, E, F):
    A_new, _, C_new, angle = rotate_conic(A, B, C)
    F_new, x0, y0 = translate_conic(A_new, C_new, D, E, F)
    return A_new, C_new, F_new, x0, y0, angle

def main():
    print("enter the equation like: Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0")
    equation = input("equation: ")
    
    try:
        A, B, C, D, E, F = sintax(equation)
        conic_type = classify_conic(A, B, C)
        print(f"conic type: {conic_type}")
        
        if conic_type == "circle":
            A_new, _, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
            radius = math.sqrt(-F_new / A_new)
            print(f"canonical equation: (x-{x0})^2 + (y-{y0})^2 = {radius**2}")

        elif conic_type == "ellipse":
            A_new, C_new, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
            a = math.sqrt(-F_new / A_new)
            b = math.sqrt(-F_new / C_new)
            print(f"canonical equation: (x-{x0})^2/{a**2} + (y-{y0})^2/{b**2} = 1")

        elif conic_type == "hyperbola":
            A_new, C_new, F_new, x0, y0, _ = to_canonical_form(A, B, C, D, E, F)
            a = math.sqrt(F_new / A_new)
            b = math.sqrt(-F_new / C_new)
            print(f"canonical equation: (x-{x0})^2/{a**2} - (y-{y0})^2/{b**2} = 1")

        elif conic_type == "parabola":
            print(f"canonical equation: {canonical_parabola(A, C, D, E, F)}")
    except Exception as e:
        print(f"error: {e}")

if __name__ == "__main__":
    main()


#4x^2-y^2-16x-6y+3=0 hyperbola
#9x^2+16y^2-54x+64y+1=0 ellipse
#x^2 + y^2 - 4 = 0
#-x^2+2x+7-y=0 parabola
#x^2+4x-8y+16=0 parabola
#y^2-4x-6y+9=0 parabola