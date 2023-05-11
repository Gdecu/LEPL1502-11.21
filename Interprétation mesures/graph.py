def graph (Title, Value):
    '''
    On plot les listes de données dans des graphes matplotlib
    '''
    fig, ax = plt.subplots()
    fig.suptitle(Title[0])
    color = ['r', 'b', 'g', 'y', 'm', 'c', 'k']
    for i in range(len(Value)):
        d = 0
        for j in range (1,len(Value[i])):
            ax.plot(Value[i][0], Value[i][j], color[d], label = Title[i][j])
            d+=1
    ax.legend()
    ax.set_ylim(-1, 8)
    ax.set_xlabel('Temps [µs]')
    ax.set_ylabel('Tensions [V]')
    plt.show()s