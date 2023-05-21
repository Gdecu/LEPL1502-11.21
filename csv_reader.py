#
# Interpretation graphique des mesures du ciruit
# LEPL1502
# Groupe 11.21 FSA11BA 2023
#


import matplotlib.pyplot as plt
import numpy as np
import csv


def get_data(filename_csv):
    '''
    On récupère les données du fichier csv dans une array numpy
    '''
    with open(str(filename_csv), 'r') as f:
        data_csv = csv.reader(f, delimiter = ';')
        Time = [];    Canal_A = [];    Canal_B = [];    i = -1
        for row in data_csv:
            i+=1
            if i < 3 or i%2 == 0:           # On prend un points sur deux car au sinon le graphe est trop chargé
                try:
                    Time.append(row[0])
                    Canal_A.append(row[1])
                    Canal_B.append(row[2])
                except:
                    continue
        (Time_titel, t) = get_title(Time);    (Canal_A_titel, A) = get_title(Canal_A);    (Canal_B_titel, B) = get_title(Canal_B)
        transform_to_float(t, 8);    transform_to_float(A, 8);    transform_to_float(B, 8)
    return ([Time_titel, Canal_A_titel, Canal_B_titel], [np.array(t), np.array(A), np.array(B)])
    

def data_moy (Value):
    '''
    On fait la moyenne des différentes données qu'on a
    '''
    A = [];  B = [];  t = Value[0][0];  Canal_A_moy = 0;    Canal_B_moy = 0
    
    for j in range(len(Value)):
        A.append(Value[j][1])
        B.append(Value[j][2])
    
    for i in range(len(A)):
        Canal_A_moy += A[i]
        Canal_B_moy += B[i]
    
    return np.array([t, Canal_A_moy/len(A), Canal_B_moy/len(B)])

def get_title(lst):
    '''
    On récupère le titre et l'unité dans la liste (et on les ajoutess dans une nouvelle liste) et on les supprime de la liste
    '''
    title = str(lst[0]) + ' ' + str(lst[1])
    j=0 ; n = len(lst)
    for i in range (n):
        if i == n - j - 2:          # pour éviter le out of range
            break
        if lst[i].isdigit() == False:
            del lst[i-j]
            j+=1
    return (title,lst)

def transform_to_float(lst, n):
    '''
    On transforme un string avec n chiffres après la virgule en float
    '''
    for i in range(len(lst)):
        a = lst[i].split(',')
        lst[i] = a[0] + a[1]
        lst[i] = float(lst[i]) * 10**(-n)
    return lst

def graph (Title, Value):
    '''
    On plot les listes de données dans des graphes matplotlib
    '''
    fig, ax = plt.subplots()
    fig.suptitle(Title[0])
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    for i in range(1, len(Value)):
        ax.plot(Value[0], Value[i], color[i-1], label = Title[i])
    ax.legend()
    ax.set_ylim(-1, 6)
    ax.set_xlim(0, 17.75)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    plt.show()
