from math import *

def tri(a, b, c):
    if a < b + c and b < a + c and c < a + b:
        return True

def check_45(a, b, c):
    deg_bc = degrees(acos((pow(b, 2) + pow(c, 2) - pow(a, 2))/(2 * b * c)))
    deg_ab = degrees(acos((pow(b, 2) + pow(a, 2) - pow(c, 2))/(2 * b * a)))
    deg_ca = degrees(acos((pow(a, 2) + pow(c, 2) - pow(b, 2))/(2 * a * c)))
    if 44.9999999999<deg_bc<45.0000000001 or 44.9999999999<deg_ab<45.0000000001  or 44.9999999999<deg_ca<45.0000000001 :
        return True

def num_tri(K, X):
    result = 0
    for k in range(1, K + 1):
        for a in range(-X, X + 1):
            for b in range(-X, X + 1):
                for c in range(-X, X + 1):
                    if a < b < c:
                        dist_ab = dist([a, pow(a, 2)/k], [b, pow(b, 2)/k])
                        dist_bc = dist([b, pow(b, 2)/k], [c, pow(c, 2)/k])
                        dist_ca = dist([c, pow(c, 2)/k], [a, pow(a, 2)/k])
                        if tri(dist_ab, dist_bc, dist_ca) and check_45(dist_ab, dist_bc, dist_ca):
                            result += 1
                                    
    print(result)

num_tri(1, 10) #41 
# number_of_triangles(10, 100) 12492