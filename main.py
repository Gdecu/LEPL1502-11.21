#
# Tous nos programmes python sont regroupés dans celui-ci
# LEPL1502
# Groupe 11.21 FSA11BA 2023
#


import mesures_circuit as b
import Caractèrisation_diamagtétique as C
import simulation_circuit as S
import R_optimal as R


if __name__ == '__main__' :
    
    # On plot les 5 blocs du circuit
    b.plot_bloc1()
    b.plot_bloc2()
    b.plot_bloc3()
    b.plot_bloc4()
    b.plot_bloc5()

    # On plot la caractèrisation avec une pièce diamagnétique
    C.plot_pièce()

    # On plot pour chaque blocs notre simulation du circuit
    S.simulation()
    S.simulation_2()

    # On calcule la valeur optimale de R_G
    R_opt = R.R_G_opt()
    print(R_opt)

    
