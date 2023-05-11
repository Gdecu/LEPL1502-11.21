# Simulation des différents blocs du circuit WeeMet-all
# Groupe 11.21


import numpy as np
import matplotlib.pyplot as plt


def simulation_oscillateur(V_cc, R_D1, R_D2, R_D3, R_G, C_G):

    # Définissons d'autres variables qui vont nous être utilses
    tau = R_G * C_G
    start = 0.0
    end = 2*10**(-5)
    long = 10000
    ti = np.linspace(start, end, long)

    # Calculons V_D pendant la charge et la décharge de la capacité
    y_Vcc = V_cc + np.zeros_like(ti)
    V_D1 = V_cc * ((R_D2*(R_D1+R_D3))/(R_D1*R_D3 + R_D2*(R_D1+R_D3)))      # V_D (charge)
    y_V_D1 = V_D1 + np.zeros_like(ti)
    V_D2 = V_cc * ((R_D2*R_D3)/(R_D2*R_D3 + R_D1*(R_D2+R_D3)))             # V_D (décharge)
    y_V_D2 = V_D2 + np.zeros_like(ti)

    # Calculons le nombre de périodes (le log de numpy est en base e, soit un ln)
    t1_0 = tau * np.log(1-((R_D2*R_D3)/(R_D2*R_D3 + R_D1*(R_D2+R_D3))))     # Quand V_G (charge) = V_D (décharge)
    t1_1 = tau * np.log(1-(R_D2*(R_D1+R_D3))/(R_D1*R_D3 + R_D2*(R_D1+R_D3)))# Quand V_G (charge) = V_D (charge)
    t2_0 = tau * np.log((R_D2*(R_D1+R_D3))/(R_D1*R_D3 + R_D2*(R_D1+R_D3)))  # Quand V_G (décharge) = V_D (charge)
    t2_1 = tau * np.log(((R_D2*R_D3)/(R_D2*R_D3 + R_D1*(R_D2+R_D3))))       # Quand V_G (décharge) = V_D (décharge)
    T1 = t1_0 - t1_1                                                        # Période de charge
    T2 = t2_0 - t2_1                                                        # Période de décharge
    T = T1 + T2                                                             # Période totale
    cycles = end//T                                                         # Nombre de périodes complètes
    demi_cylces = 2*cycles                                                  # Nombre de démi-périodes complètes
    if (end-T*(end//T))//T1 >= 1:
        demi_cylces += 1
    
    # Calculons V_G pendant la charge et la décharge
    ti1 = np.array([])
    ti2 = np.array([])
    for t in ti:
        if t < T1:
            ti1 = np.append(ti1, t)
        else:
            break
    for t in ti:
        if t < T2:
            ti2 = np.append(ti2, t)
    V_G1 = V_cc*(1-np.exp(-(ti1-t1_0)/tau))
    V_G2 = V_cc*np.exp(-(ti2-t2_0)/tau)

    # Calculons la courbe V_G, V_D et V_S au cours du temps
    V_S = np.array([])
    V_G = np.array([])
    V_D = np.array([])
    for i in range(int(cycles)):
        V_G = np.append(V_G, V_G1)
        V_S = np.append(V_S, np.zeros_like(V_G1) + float(V_cc))
        V_D = np.append(V_D, np.zeros_like(V_G1) + float(V_D1))
        V_G = np.append(V_G, V_G2)
        V_S = np.append(V_S, np.zeros_like(V_G2))
        V_D = np.append(V_D, np.zeros_like(V_G2) + float(V_D2))
    if demi_cylces - 2*cycles == 0:
        for j in range(len(ti)-len(V_G)):
            V_G = np.append(V_G, V_G1[j])
            V_S = np.append(V_S, float(V_cc))
            V_D = np.append(V_D, float(V_D1))
    else:
        V_G = np.append(V_G, V_G1)
        V_S = np.append(V_S, np.zeros_like(V_G1) + float(V_cc))
        V_D = np.append(V_D, np.zeros_like(V_G1) + float(V_D1))
        for j in range(len(ti)-len(V_G)):
            V_G = np.append(V_G, V_G2[j])
            V_S = np.append(V_S, 0.0)
            V_D = np.append(V_D, float(V_D2))

    # Et on plot tout ça dans la fonction d'après
    return (y_Vcc, y_V_D1, y_V_D2, V_D, V_G, V_S, ti, ti1, ti2, T1, T2, cycles, demi_cylces)


def graphe_oscillateur(y_Vcc, y_V_D1, y_V_D2, V_D, V_G, V_S, ti):

    plt.figure("Oscillateur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, y_Vcc, "-b", linewidth=3.0, label="Vcc")
    #plt.plot(ti*10**6, y_V_D1, label="V_D (charge)")
    #plt.plot(ti*10**6, y_V_D2, label="V_D (décharge)")
    plt.plot(ti*10**6, V_D, "-g", linewidth=3.0, label="V_D")
    plt.plot(ti*10**6, V_G, "-y", linewidth=3.0, label="V_G")
    plt.plot(ti*10**6, V_S, "-r", linewidth=3.0, label="V_S")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def simulation_circuit_RL(ti, V_cc, R_L, L, ti1, ti2, T1, cycles, demi_cylces):

    tau = L / R_L
    t1_0 = 0
    t2_0 = 0

    # Calculons V_L1 et V_L2 en "charge" / "décharge"
    V_L1 = V_cc*(1-np.exp(-(ti1-t1_0)/tau))
    V_L2 = V_cc*np.exp(-(ti2+t2_0)/tau) - V_cc*np.exp(-(T2)/tau)

    # Calculons maintenant V_L au cours du temps
    V_L= np.array([])
    for i in range(int(cycles)):
        V_L = np.append(V_L, V_L1)
        V_L = np.append(V_L, V_L2)
    if demi_cylces - 2*cycles == 0:
        for j in range(len(ti)-len(V_L)):
            V_L = np.append(V_L, V_L1[j])
    else:
        V_L = np.append(V_L, V_L1)
        for j in range(len(ti)-len(V_L)):
            V_L = np.append(V_L, V_L2[j])

    maxx = V_cc*(1-np.exp(-(T1-t1_0)/tau))

    return (V_L, maxx)


def graphe_circuit_RL(ti, V_S, V_L):

    plt.figure("Ciruit RL")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_S, "-b", linewidth=3.0, label="V_S")
    plt.plot(ti*10**6, V_L, "-r", linewidth=3.0, label="V_L")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def simulation_détecteur_de_crête(ti, T1, T2, cycles, demi_cycles, V_cc, V_L, C_Det, R_Det, maxx):
    
    tau = C_Det * R_Det
    t1_0 = 0

    V_C = np.zeros_like(V_L)
    V_C[0] = V_L[0]

    n = np.zeros_like(ti)
    for i in range(1,int(cycles)+2):
        for j in range(len(ti)):
            if ti[j] > i*T1 + (i-1)*T2:
                n[j] += 1

    for t in range(1, len(ti)):
        if V_L[t] > V_C[t-1]:
            V_C[t] = V_L[t]
        else:
            V_C[t] = maxx*np.exp(-(ti[t]+t1_0-(n[t]*T1+(n[t]-1)*T2))/tau)

    count = 0
    for k in range(len(ti)):
        if ti[k]>T1:
            count += k
            break
    
    ti_vrai = ti[count:] - T1
    V_C_vrai = V_C[count:]

        
    return (V_C, ti_vrai, V_C_vrai)


def graphe_détecteur_de_crête(ti, V_C, V_L):

    plt.figure("Détecteur de crête")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_L, "-b", linewidth=3.0, label="V_L")
    plt.plot(ti*10**6, V_C, "-r", linewidth=3.0, label="V_C")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()


def simulation_soustracteur(V_Z, V_C, pR_sousp1, pR_sousp2, pR_sousm1, pR_sousm2):
    V_sous = np.ones_like(V_C) * (V_Z*pR_sousp2)/(pR_sousp1+pR_sousp2)
    V_F = V_sous*(pR_sousm1+ pR_sousm2)/pR_sousm1-V_C*pR_sousm2/pR_sousm1
    return (V_F, V_sous)


def graphe_soustracteur(ti, V_C, V_F, V_sous):

    plt.figure("Soustracteur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_C, "-b", linewidth=3.0, label="V_C")
    plt.plot(ti*10**6, V_F, "-r", linewidth=3.0, label="V_F")
    plt.plot(ti*10**6, V_sous, "-g", linewidth=3.0, label="V_sous")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
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


def graphe_comparateur(ti, V_out, V_ref, V_F):

    plt.figure("Comparateur")
    plt.rcParams.update({'font.size': 25})
    plt.plot(ti*10**6, V_out, "-r",  linewidth=3.0, label="V_out")
    plt.plot(ti*10**6, V_ref, "-g",  linewidth=3.0, label="V_ref")
    plt.plot(ti*10**6, V_F, "-b",  linewidth=3.0, label="V_F")
    plt.xlabel("Temps(µs)")
    plt.ylabel("Tension(V)")
    plt.ylim(-0.1, V_cc + 0.1)
    plt.legend(loc ="upper right")
    manager = plt.get_current_fig_manager()
    manager.full_screen_toggle()
    plt.show()



if __name__ == '__main__' :
    V_cc = 5 ; R_D1 = 10000 ; R_D2 = 10000 ; R_D3 = 10000
    R_G = 10000                 # à déterminer
    C_G = 0.5 * (10**(-9))      # 0.5 ou 0.05 nF (si 0.05nF, il faut changer l'échelle de temps car sinon, les écarts devenants trop petits et il y a erreur)
    R_L = 330 ; L = 7*(10**(-4))
    C_Det = 10**-6 ; R_Det = 100000
    V_Z = V_cc
    pR_sousp1 = 50000 ; pR_sousp2 = 50000 ; pR_sousm1 = 50000 ; pR_sousm2 = 50000       # à déterminer
    pR_ref1 = 50000 ; pR_ref2 = 50000

    (y_Vcc, y_V_D1, y_V_D2, V_D, V_G, V_S, ti, ti1, ti2, T1, T2, cycles, demi_cylces) = simulation_oscillateur(V_cc, R_D1, R_D2, R_D3, R_G, C_G)
    graphe_oscillateur(y_Vcc, y_V_D1, y_V_D2, V_D, V_G, V_S, ti)
    (V_L, maxx) = simulation_circuit_RL(ti, V_cc, R_L, L, ti1, ti2, T1, cycles, demi_cylces)
    graphe_circuit_RL(ti, V_S, V_L)
    (V_C, ti_vrai, V_C_vrai) = simulation_détecteur_de_crête(ti, T1, T2, cycles, demi_cylces, V_cc, V_L, C_Det, R_Det, maxx)
    graphe_détecteur_de_crête(ti, V_C, V_L)
    (V_F, V_sous) = simulation_soustracteur(V_Z, V_C_vrai, pR_sousp1, pR_sousp2, pR_sousm1, pR_sousm2)
    graphe_soustracteur(ti_vrai, V_C_vrai, V_F, V_sous)
    (V_out, V_ref) = simulation_comparateur(V_cc, V_Z, V_F, pR_ref1, pR_ref2)
    graphe_comparateur(ti_vrai, V_out, V_ref, V_F)