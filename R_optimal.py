#
# Programme qui a comme but de trouver une résistance optimale pour avoir une différence de tension la plus importante possible
# LEPL1502
# Groupe 11.21 FSA11BA 2023
#


import numpy as np


def V_M_prime(T, L_1, L_2, R_L):
    return (np.exp(-(T*R_L)/(2*L_1))) / (L_1*(1+np.exp(-(T*R_L)/(2*L_1)))**2) - (np.exp(-(T*R_L)/(2*L_2))) / (L_2*(1+np.exp(-(T*R_L)/(2*L_2)))**2)

def bissection(a, b, tol, nmax, L_1, L_2, R_L):
    mess1 = "-- Rechoisir a et b --"
    mess2 = "-- Trop d'itération --"
    mess3 = "-- Ça marche de ouf --"
    fa = V_M_prime(a, L_1, L_2, R_L) ; fb = V_M_prime(b, L_1, L_2, R_L)
    n = 1
    if fa*fb > 0:
        return None, mess1
    else :
        x = (a+b)/2
        fx = V_M_prime(x, L_1, L_2, R_L)
        if fx*fa < 0:
            b = x
        else :
            a = x
        n += 1
        while n < nmax and abs(fx) >= tol:
            x = (a+b)/2
            fx = V_M_prime(x, L_1, L_2, R_L)
            if fx*fa < 0:
                b = x
            else :
                a = x
            n += 1
    if n == nmax:
        return None, mess2
    return x, mess3

def R(T, C_G, alpha):
    return T/(2*C_G*np.log(alpha))

def R_G_opt():
    L_1 = 0.7*(10**-3) ; L_2 = 0.69*(10**-3)
    R_L = 330
    C_G = 0.5 * (10**(-9)) ; alpha = 2
    (a, b) = (0, 10**-5)
    tol = 10**-10 ; nmax = 100000
    (T_opt, message) =  bissection(a, b, tol, nmax, L_1, L_2, R_L)
    R_opt = R(T_opt, C_G, alpha)
    return R_opt, message

print(R_G_opt())