#
# Simulation des différents blocs du circuit WeeMet-all et calcul des valeurs optimales à utiliser
# On considère directement que la période de charge et de décharge sont les mêmes
# LEPL1502
# Groupe 11.21 FSA11BA 2023
#


import numpy as np
import matplotlib.pyplot as plt


def simulation_oscillateur(V_cc, R_D1, R_D2, R_D3, R_G, C_G, sr):

    # Autres variables qui vont nous être utilses
    tau = R_G * C_G
    start = 0.0
    end = 1.7*10**(-5)            # cas où le slew-rate arrive en end non traité
    long = 10000
    ti = np.linspace(start, end, long)

    # Périodes -> on considère, pour simplifier la suite, que les périodes de charge et de décharge sont les mêmes
    t0 = tau * np.log(1/(1-((R_D2*R_D3)/(R_D2*R_D3 + R_D1*(R_D2+R_D3)))))       # Quand V_G (charge) = V_D (décharge)
    t1 = tau * np.log(1/(1-(R_D2*(R_D1+R_D3))/(R_D1*R_D3 + R_D2*(R_D1+R_D3))))  # Quand V_G (charge) = V_D (charge)
    T = 2*(t1 - t0)                                                             # Période de charge = Période de décharge

    # Rajout du slew-rate de l'amplificateur opérationnel
    T_sr = V_cc / sr
    T_tot = T + 2*T_sr

    # Nombre de cycles
    demi_cycles = end//(T_tot/2)
    cycles = demi_cycles // 2
    vsfin = False
    if demi_cycles % 2 == 1:
        vsfin = True

    # Différents temps t qui s'étalent sur la période
    ti_demi_cycle = np.array([])
    ti_sr = np.array([])
    for t in ti:
        if t<T/2:
            ti_demi_cycle = np.append(ti_demi_cycle, t)
        else:
            break
    for t in ti:
        if t<T_sr:
            ti_sr = np.append(ti_sr, t)
        else:
            break

    # Comportement du slew-rate
    f_sr_montée = sr*ti_sr
    f_sr_descente = np.flip(f_sr_montée)

    # Valeurs constantes de V_D
    V_D1 = V_cc * ((R_D2*(R_D1+R_D3))/(R_D1*R_D3 + R_D2*(R_D1+R_D3)))
    V_D2 = V_cc * ((R_D2*R_D3)/(R_D2*R_D3 + R_D1*(R_D2+R_D3)))


    # V_S, V_D, V_G
    V_S = np.array([])
    V_D = np.array([])
    V_G = np.array([])
    ci = V_D2
    for i in range(int(cycles)):
        V_S = np.append(V_S, np.zeros_like(ti_demi_cycle) + float(V_cc))
        V_S = np.append(V_S, np.zeros_like(ti_sr) + f_sr_descente)
        V_S = np.append(V_S, np.zeros_like(ti_demi_cycle))
        V_S = np.append(V_S, np.zeros_like(ti_sr) + f_sr_montée)
        V_D = np.append(V_D, np.zeros_like(ti_demi_cycle) + float(V_D1))
        V_G = np.append(V_G, V_cc*(1-np.exp(-ti_demi_cycle/tau))+ci*np.exp(-ti_demi_cycle/tau))
        for t in range(len(ti_sr)):
            V_D = np.append(V_D, (V_cc*R_D3 + f_sr_descente[t]*R_D1)*R_D2/(R_D1*R_D2 + R_D1*R_D3 + R_D2*R_D3))

        ci = V_G[-1]
        t_intervalle = ti_sr[1]
        V_G = np.append(V_G, ci)
        for t in range(1,len(ti_sr)):
            V_G = np.append(V_G, f_sr_descente[t]+(ci-f_sr_descente[t])*np.exp(-(t_intervalle)/tau))
            ci = f_sr_descente[t]+(ci-f_sr_descente[t])*np.exp(-(t_intervalle)/tau)

        V_D = np.append(V_D, np.zeros_like(ti_demi_cycle) + float(V_D2))
        V_G = np.append(V_G, ci*np.exp(-ti_demi_cycle/tau))
        for t in range(len(ti_sr)):
            V_D = np.append(V_D, (V_cc*R_D3 + f_sr_montée[t]*R_D1)*R_D2/(R_D1*R_D2 + R_D1*R_D3 + R_D2*R_D3))

        ci = V_G[-1]
        V_G = np.append(V_G, ci)
        for t in range(1,len(ti_sr)):
            V_G = np.append(V_G, f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau))
            ci = f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau)
        
    if vsfin == False:
        ci =  V_G[-1]
        for j in range(len(ti)-len(V_S)):
            V_S = np.append(V_S, float(V_cc))
            V_D = np.append(V_D, float(V_D1))
            V_G = np.append(V_G, V_cc*(1-np.exp(-ti_demi_cycle[j]/tau))+ci*np.exp(-ti_demi_cycle[j]/tau))
    else:
        V_S = np.append(V_S, np.zeros_like(ti_demi_cycle) + float(V_cc))
        V_S = np.append(V_S, np.zeros_like(ti_sr) + f_sr_descente)
        V_D = np.append(V_D, np.zeros_like(ti_demi_cycle) + float(V_D1))
        V_G = np.append(V_G, V_cc*(1-np.exp(-ti_demi_cycle/tau))+ci*np.exp(-ti_demi_cycle/tau))
        for t in range(len(ti_sr)):
            V_D = np.append(V_D, (V_cc*R_D3 + f_sr_descente[t]*R_D1)*R_D2/(R_D1*R_D2 + R_D1*R_D3 + R_D2*R_D3))

        ci = V_G[-1]
        t_intervalle = ti_sr[1]
        V_G = np.append(V_G, ci)
        for t in range(1,len(ti_sr)):
            V_G = np.append(V_G, f_sr_descente[t]+(ci-f_sr_descente[t])*np.exp(-(t_intervalle)/tau))
            ci = f_sr_descente[t]+(ci-f_sr_descente[t])*np.exp(-(t_intervalle)/tau)

        for j in range(len(ti)-len(V_S)):
            V_S = np.append(V_S, 0.0)
            V_D = np.append(V_D, np.zeros_like(ti_demi_cycle[j]) + float(V_D2))
            V_G = np.append(V_G, ci*np.exp(-ti_demi_cycle[j]/tau))

    return V_S, V_D, V_G, T, T_tot, ti, ti_demi_cycle, ti_sr, f_sr_montée, f_sr_descente, cycles, vsfin


def graphe_oscillateur(V_cc, V_S, V_D, V_G, ti):

    plt.figure("Oscillateur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, np.zeros_like(ti)+V_cc, "-b", linewidth=3.0, label="V_cc")
    plt.plot(ti*10**6, V_S, "-r", linewidth=3.0, label="V_S")
    plt.plot(ti*10**6, V_D, "-y", linewidth=3.0, label="V_D")
    plt.plot(ti*10**6, V_G, "-g", linewidth=3.0, label="V_G")
    plt.xlabel("Temps[µs]")
    plt.ylabel("Tension[V]")
    plt.xlim(-1, 17.5)
    plt.ylim(-1, V_cc + 1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def simulation_circuit_RL(V_cc, R_L, L, T, ti, ti_demi_cycle, ti_sr, f_sr_montée, f_sr_descente, cycles, vsfin):

    tau = L / R_L

    V_max = V_cc / (1 + np.exp(-T/(2*tau)))
    V_min = V_max * np.exp(-T/(2*tau))

    V_L = np.array([])
    ci = V_min
    # Calcul du vrai V_min (il va changer du au slew-rate)

    for i in range(10):
        V_L = np.append(V_L, (V_cc-ci)*(1-np.exp(-ti_demi_cycle/tau)) + ci)
        ci = V_L[-1]
        t_intervalle = ti_sr[1]
        V_L = np.append(V_L, ci)
        for t in range(1,len(ti_sr)):
            V_L = np.append(V_L, (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci)
            ci = (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci
            if V_L[-1] > V_L[-2]:
                Vrai_V_max = ci
        V_L = np.append(V_L, ci*np.exp(-ti_demi_cycle/tau))

        ci = V_L[-1]
        V_L = np.append(V_L, ci)
        for t in range(1,len(ti_sr)):
            V_L = np.append(V_L, f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau))
            ci = f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau)


    V_L = np.array([])
    for i in range(int(cycles)):
        V_L = np.append(V_L, (V_cc-ci)*(1-np.exp(-ti_demi_cycle/tau)) + ci)
        ci = V_L[-1]
        t_intervalle = ti_sr[1]
        V_L = np.append(V_L, ci)
        for t in range(1,len(ti_sr)):
            V_L = np.append(V_L, (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci)
            ci = (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci
 
        V_L = np.append(V_L, ci*np.exp(-ti_demi_cycle/tau))

        ci = V_L[-1]
        V_L = np.append(V_L, ci)
        for t in range(1,len(ti_sr)):
            V_L = np.append(V_L, f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau))
            ci = f_sr_montée[t]+(ci-f_sr_montée[t])*np.exp(-(t_intervalle)/tau)


    if vsfin == False:
        for j in range(len(ti)-len(V_L)):
            V_L = np.append(V_L, (V_cc-ci)*(1-np.exp(-ti_demi_cycle[j]/tau)) + ci)
    else:
        V_L = np.append(V_L, (V_cc-ci)*(1-np.exp(-ti_demi_cycle/tau)) + ci)

        ci = V_L[-1]
        t_intervalle = ti_sr[1]
        V_L = np.append(V_L, ci)
        for t in range(1,len(ti_sr)):
            V_L = np.append(V_L, (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci)
            ci = (f_sr_descente[t]-ci)*(1-np.exp(-t_intervalle/tau)) + ci
        
        for j in range(len(ti)-len(V_L)):
            V_L = np.append(V_L, ci*np.exp(-ti_demi_cycle[j]/tau))

    return V_L, Vrai_V_max


def graphe_circuit_RL(V_cc, ti, V_S, V_L):

    plt.figure("Ciruit RL")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_S, "-r", linewidth=3.0, label="V_S")
    plt.plot(ti*10**6, V_L, "-b", linewidth=3.0, label="V_L")
    plt.xlabel("Temps[µs]")
    plt.ylabel("Tension[V]")
    plt.xlim(-1, 17.5)
    plt.ylim(-1, V_cc + 1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def simulation_détecteur_de_crête(ti, T, V_cc, V_L, C_Det, R_Det, V_max, sr):
    # Calcul de la crête (en prenant en compte le slew rate)
    # Trois approximations sont faite : 
    # Que la décharge de la capa est constante
    # Que lorsque Vout arrive à son maximum (la crête), il retourne directement à 0
    # Que la diode est idéale
    # Grâce à celles-ci, calculons la crête avec une méthode de bissection
    A = np.array([3, 0, 0]) ; B = np.array([V_max-0.05, 0, 0]) ; X = np.array([(A[0] + B[0])/2, 0, 0]) ; tol_fin = 10**-2 ; nmax = 10000 ; n = 1 ; sr = sr/10**6
    t_T = 0
    for t in range(len(ti)):
        if ti[t] >= T:
            t_T = t
            break

    for t in range(len(ti)):
        if V_L[t] >= A[0]:
            A[1] = ti[t]*10**6
            break
    for t in range(t_T, 0, -1):
        if V_L[t] >= A[0]:
            A[1] = ti[t]*10**6 - A[1]
            break
    A[2] = sr - (A[0]+0.7)/A[1]       # signe positif

    for t in range(len(ti)):
        if V_L[t] >= B[0]:
            B[1] = ti[t]*10**6
            break
    for t in range(t_T, 0, -1):
        if V_L[t] >= B[0]:
            B[1] = ti[t]*10**6 - B[1]
            break
    B[2] = sr - (B[0]+0.7)/B[1]       # signe négatif

    for t in range(len(ti)):
        if V_L[t] >= X[0]:
            X[1] = ti[t]*10**6
            break
    for t in range(t_T, 0, -1):
        if V_L[t] >= X[0]:
            X[1] = ti[t]*10**6 - X[1]
            break
    X[2] = sr - (X[0]+0.7)/X[1]       # signe inconnu

    while abs(X[2]) > tol_fin and n < nmax:
        if X[2]*A[2] > 0:
            A = np.copy(X)
        else:
            B = np.copy(X)

        X = np.array([(A[0] + B[0])/2, 0, 0])
        for t in range(len(ti)):
            if V_L[t] >= X[0]:
                X[1] = ti[t]*10**6
                break
        for t in range(t_T, 0, -1):
            if V_L[t] >= X[0]:
                X[1] = ti[t]*10**6 - X[1]
                break
        X[2] = sr - (X[0]+0.7)/X[1]
        n += 1
    
    if n == nmax:
        return None
    crete = X[0]
    print(crete)
    if crete > V_cc - 0.7:
        crete = V_cc - 0.7

    # On considère que le signal est constant
    V_C = np.zeros_like(V_L) + crete

    return V_C


def graphe_détecteur_de_crête(V_cc, ti, V_C, V_L):

    plt.figure("Détecteur de crête")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_L, "-b", linewidth=3.0, label="V_L")
    plt.plot(ti*10**6, V_C, "-r", linewidth=3.0, label="V_C")
    plt.xlabel("Temps[µs]")
    plt.ylabel("Tension[V]")
    plt.xlim(-1, 17.5)
    plt.ylim(-1, V_cc + 1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()



def simulation():
    V_cc = 5 ; R_D1 = 10000 ; R_D2 = 10000 ; R_D3 = 10000
    sr = 7/(10**-6) ; R_G = 12000 ; C_G = 0.5 * (10**(-9))      #Bloc 1
    R_L = 330 ; L = 7.86*(10**(-4))     #Bloc 2
    C_Det = 10**-6 ; R_Det = 100000     #Bloc 3

    V_S, V_D, V_G, T, T_tot, ti, ti_demi_cycle, ti_sr, f_sr_montée, f_sr_descente, cycles, vsfin = simulation_oscillateur(V_cc, R_D1, R_D2, R_D3, R_G, C_G, sr)
    graphe_oscillateur(V_cc, V_S, V_D, V_G, ti)
    V_L, V_max = simulation_circuit_RL(V_cc, R_L, L, T, ti, ti_demi_cycle, ti_sr, f_sr_montée, f_sr_descente, cycles, vsfin)
    graphe_circuit_RL(V_cc, ti, V_S, V_L)
    V_C = simulation_détecteur_de_crête(ti, T, V_cc, V_L, C_Det, R_Det, V_max, sr)
    graphe_détecteur_de_crête(V_cc, ti, V_C, V_L)
    


def simulation_soustracteur(ti, V_Z, V_C, pR_sousp1, pR_sousp2, pR_sousm1, pR_sousm2):
    V_sous = np.ones_like(V_C) * (V_Z*pR_sousp2)/(pR_sousp1+pR_sousp2)
    V_F = np.zeros_like(ti)
    for t in range(len(ti)):
        a = V_sous[t]*(pR_sousm1+ pR_sousm2)/pR_sousm1-V_C[t]*pR_sousm2/pR_sousm1
        if a > V_Z:
            a = V_Z
        if a < 0:
            a = 0
        V_F[t] = a
    return (V_F, V_sous)


def graphe_soustracteur(V_cc, ti, V_C, V_F, V_sous):

    plt.figure("Soustracteur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_C, "-b", linewidth=3.0, label="V_C")
    plt.plot(ti*10**6, V_F, "-r", linewidth=3.0, label="V_F")
    plt.plot(ti*10**6, V_sous, "-g", linewidth=3.0, label="V_sous")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.5, V_cc + 0.5)
    plt.xlim(-1, 20)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()

def simulation_comparateur(V_cc, V_Z, V_F, pR_ref1, pR_ref2):
    V_ref = np.zeros_like(V_F) + (V_Z*pR_ref2)/(pR_ref1+pR_ref2)
    V_out = np.zeros_like(V_F)
    for t in range(len(V_F)):
        if V_ref[t] > V_F[t]:
            V_out[t] += V_cc
    return (V_out, V_ref)

def graphe_comparateur(V_cc, ti, V_out, V_ref, V_F):

    plt.figure("Comparateur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_out, "-r",  linewidth=3.0, label="V_out")
    plt.plot(ti*10**6, V_ref, "-g",  linewidth=3.0, label="V_ref")
    plt.plot(ti*10**6, V_F, "-b",  linewidth=3.0, label="V_F")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
    plt.xlim(-1, 180)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()

def simulation_2():
    pR_sousp1 = 40000 ; pR_sousp2 = 100000 - pR_sousp1 ; pR_sousm1 = 5000 ; pR_sousm2 = 100000 - pR_sousm1 ; V_cc = 2
    pR_ref1 = 50000 ; pR_ref2 = 100000 - pR_ref1
    ti = np.linspace(0, 180*(10**-6), 10000)
    V_C = np.r_[np.zeros(int(len(ti)/2)) + ti[:5000]*(2/(60*(10**-6))), np.zeros(int(len(ti)/2)) + 2 - (ti[5000:]-ti[5000])*(2/(10*(10**-6)))]
    V_F_2 = np.r_[np.zeros(3333) + ti[:3333]*(2/(60*(10**-6))), np.zeros(3333) + 2 - (ti[3333:6666]-ti[3333])*(2/(60*(10**-6))), np.zeros(3334) + (ti[6666:]-ti[6666])*(2/(60*(10**-6)))]
    (V_F, V_sous) = simulation_soustracteur(ti, V_cc, V_C, pR_sousp1, pR_sousp2, pR_sousm1, pR_sousm2)
    graphe_soustracteur(V_cc, ti, V_C, V_F, V_sous)
    (V_out, V_ref) = simulation_comparateur(V_cc, V_cc, V_F_2, pR_ref1, pR_ref2)
    graphe_comparateur(V_cc, ti, V_out, V_ref, V_F_2)
    
simulation()
simulation_2()