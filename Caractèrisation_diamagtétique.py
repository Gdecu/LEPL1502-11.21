#
# Interpretation graphique des mesures du ciruit
# LEPL1502
# Groupe 11.21 FSA11BA 2023
#


import csv_reader as cs
import matplotlib.pyplot as plt


def plot_pièce():
    '''
    On plot les quatre mesure de V_LED avec une pièce diamagnétique qui approche notre bobine
    '''
    (Title, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Caractèrisation\V0_3\V0_01.csv")
    (Title, Value_2) = cs.get_data(r"C:\Users\gasto\Downloads\Caractèrisation\V1_3\V1_3_01.csv")
    (Title, Value_3) = cs.get_data(r"C:\Users\gasto\Downloads\Caractèrisation\V2_3\V2_3_01.csv")
    (Title, Value_4) = cs.get_data(r"C:\Users\gasto\Downloads\Caractèrisation\V3_3\V1_01_01.csv")
    
    # On plot les données dans un graphes
    Value_1[0] -= 25    # On inititialise T_0 en t = 0
    Title = 'V_LED'
    fig, axes = plt.subplots(2,2, constrained_layout=True)
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    
    ax = axes[0][0]
    ax.set_title("Sans pièce")
    ax.set_ylim(-0.5,2.5)
    ax.set_xlim(0, 25)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    ax.plot(Value_1[0], Value_1[2], color[1], label = Title)
    ax.legend()

    ax = axes[0][1]
    ax.set_title("Un quart de la pièce sur la bobine")
    ax.set_ylim(-0.5,2.5)
    ax.set_xlim(0, 25)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    ax.plot(Value_1[0], Value_2[2], color[1], label = Title)
    ax.legend()
    
    ax = axes[1][0]
    ax.set_title("La moitié de la pièce sur la bobine")
    ax.set_ylim(-0.5,2.5)
    ax.set_xlim(0, 25)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    ax.plot(Value_1[0], Value_3[2], color[1], label = Title)
    ax.legend()

    ax = axes[1][1]
    ax.set_title("Toute la pièce sur la bobine")
    ax.set_ylim(-0.5,2.5)
    ax.set_xlim(0, 25)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    ax.plot(Value_1[0], Value_4[2], color[1], label = Title)
    ax.legend()
    plt.show()