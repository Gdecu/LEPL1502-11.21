#
# Interpretation graphique des mesures du ciruit pour LEPL 1502
# Groupe 11.21 FSA11BA 2022-2023
#


import csv_reader as cs
import matplotlib.pyplot as plt


def plot_bloc1():
    '''
    On plot le bloc 1
    '''

    # On calcule V_cc et V_s
    (Title_1, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VccR_VsB\VccR_VsB_01.csv")
    (Title_11, Value_11) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VccR_VsB\VccR_VsB_02.csv")
    (Title_12, Value_12) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VccR_VsB\VccR_VsB_03.csv")
    # On fait la moyenne des trois mesures différente pour plus de précision
    Value_1 = cs.data_moy([Value_1, Value_11, Value_12])


    # On calcule V_G et V_D
    (Title_2, Value_2) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VdR_VgB\VdR_VgB_01.csv")
    (Title_21, Value_21) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VdR_VgB\VdR_VgB_02.csv")
    (Title_22, Value_22) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VdR_VgB\VdR_VgB_03.csv")
    # On fait la moyenne des trois mesures différente pour plus de précision
    Value_2 = cs.data_moy([Value_2, Value_21, Value_22])   
    
    
    # On plot les données dans un graphe
    Value_1[0] -= 5
    Value_2[0] += 1;  Value_2[0] *= 0.84
    Title = ['Bloc 1 : Oscillateur', 'V_cc',  'V_s', 'V_G', 'V_D']
    fig, ax = plt.subplots()
    fig.suptitle(Title[0])
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    ax.plot(Value_1[0], Value_1[1], color[0], label = Title[1])
    ax.plot(Value_1[0], Value_1[2], color[1], label = Title[2])
    ax.plot(Value_2[0], Value_2[1], color[2], label = Title[3])
    ax.plot(Value_2[0], Value_2[2], color[3], label = Title[4])
    ax.legend()
    ax.set_ylim(-1, 6)
    ax.set_xlim(0, 20)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    plt.show()

def plot_bloc2():
    '''
    On plot le bloc 2
    '''
    (Title, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VsB\VLR_VsB_01.csv")
    (Title, Value_11) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VsB\VLR_VsB_01.csv")
    (Title, Value_12) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VsB\VLR_VsB_01.csv")
    # On fait la moyenne des trois mesures différente pour plus de précision
    Value_moy = cs.data_moy([Value_1, Value_11, Value_12])
    
    # On plot les données dans un graphes
    Title = ['Bloc 2 : Circuit RL', 'V_s', 'V_L']
    cs.graph(Title, Value_moy)

def plot_bloc3():
    '''
    On plot le bloc 3
    '''
    (Title, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VcB\VLR_VcB_01.csv")
    (Title, Value_11) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VcB\VLR_VcB_02.csv")
    (Title, Value_12) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VLR_VcB\VLR_VcB_03.csv")
    # On fait la moyenne de V_C
    Value_moy = cs.data_moy([Value_1, Value_11, Value_12]);  Value_1[1] = Value_moy[1]
    
    # On plot les données dans un graphes
    Value_1[0] -= 7.5
    Title = ['Bloc 3 : Détecteur de crète sans détections','V_C','V_L']
    cs.graph(Title, Value_1)
plot_bloc3()
def plot_bloc4():
    '''
    On plot le bloc 4
    '''
    # On calcule V_F et V_C
    (Title, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VcR_VfB\VcR_VfB_01.csv")
    (Title, Value_11) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VcR_VfB\VcR_VfB_02.csv")
    (Title, Value_12) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VcR_VfB\VcR_VfB_03.csv")
    
    # On calcule V_sous    
    (Title, Value_2) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VcR_VsousB\VcR_VsousB_01.csv")
    
    # On plot les données dans un graphe
    Value_1[0] -= 2.5
    Title = ['Bloc 4 : Soustracteur','V_F','V_C', 'V_sous']
    fig, ax = plt.subplots()
    fig.suptitle(Title[0])
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    ax.plot(Value_1[0], Value_1[1], color[0], label = Title[1])
    ax.plot(Value_1[0] + 1, Value_1[2], color[1], label = Title[2])
    ax.plot(Value_2[0], Value_2[1], color[2], label = Title[3])
    ax.legend()
    ax.set_ylim(-1,3)
    ax.set_xlim(0, 25)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    plt.show()

def plot_bloc5():
    '''
    On plot le bloc 5
    '''
    # On calcule V_F et V_out
    (Title, Value_1) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VFR_VoutB\VFR_VoutB_01.csv")


    #Value_1 = cs.data_moy(Value)               
    
    # Calcule de V_ref
    (Title, Value_2) = cs.get_data(r"C:\Users\gasto\Downloads\Données final\VfR_VrefB\VfR_VrefB_01.csv")


    #Value_2 = cs.data_moy(Value_1)
    
    Title = ['Bloc 5 : Comparateur','V_F','V_out', 'V_ref']
    fig, ax = plt.subplots()
    fig.suptitle(Title[0])
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    ax.plot(Value_1[0], Value_1[1], color[0], label = Title[1])
    ax.plot(Value_1[0], Value_1[2], color[1], label = Title[2])
    ax.plot(Value_2[0], Value_2[1], color[2], label = Title[3])
    ax.legend()
    ax.set_ylim(-1, 3)
    ax.set_xlim(0, 100)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    plt.show()