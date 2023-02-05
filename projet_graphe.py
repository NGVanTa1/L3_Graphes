"""
Lit le fichier au format CSV en paramètre et renvoie la matrice d'adjacence du graphe décrit
"""
from curses import flash
from operator import index, indexOf
from pickle import TRUE
from traceback import print_list

mat_adj_test = [[0,1,1,1,1,1,0,0,0,0],[1,0,0,0,0,0,1,0,0,0],[1,0,0,1,1,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0],[1,0,1,0,0,1,1,0,0,0],[1,0,0,1,1,0,1,1,1,1],[0,1,0,0,1,1,0,1,0,0],[0,0,0,0,0,1,1,0,1,0],[0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,1,0,0,0,0]]

def read_file(filename):
    size = max_vertex(filename)
    file = open(filename,"r")
    mat = [[0 for  i in range(size+1)]for j in range(size+1)]
    for x in file:
        y = x.replace("\n", "")
        splited = y.split(",")
        if(splited[0].isdigit() and splited[1].isdigit()):
            a = int(splited[0])
            b = int(splited[1])
            mat[a][b]  = 1
            mat[b][a]  = 1 
    file.close()
    return mat

"""
Renvoie le sommet ayant l'indice le plus grand parmis les sommets décrits dans un fichier CSV
"""
def max_vertex(filename):
    max = -1
    file = open(filename,"r")
    for x in file:
        y = x.replace("\n", "")
        splited = y.split(",")
        if(splited[0].isdigit() and splited[1].isdigit()):
            if int(splited[0]) > max:
                max = int(splited[0])
            if int(splited[1]) > max:
                max = int(splited[1])
    file.close()
    return max

"""
Renvoie l'indice du sommet ayant le moins d'arêtes dans la matrice d'adjacence en paramètre
"""
def min_centre(mat, centre, k):
    min = -1
    ind = -1
    for i in range(len(mat)):
        #Si le k de ce sommet n'a pas encore été trouvé
        if(centre[i] == -1):
            count = 0
            for j in range(len(mat)):
                count += mat[i][j]
            if min == -1 and count == k:
                min = count
                ind = i
            elif count < min and count == k:
                min = count
                ind = i
    return ind

"""
Crée et renvoie un tableau de la taille d'une ligne de la matrice d'adjacence passée en paramètre.
Contiendra les nombres k de chaque sommet
"""
def create_centre_array(mat):
    return [-1 for i in range(len(mat))]

"""
Met toutes les valeurs de la colonne d'indice ind à 0
"""
def set_index_null(ind, mat):
    for i in range(len(mat)):
        mat[i][ind] = 0

def compute_degeneracy(mat):
    centre = create_centre_array(mat)
    k = 0
    while -1 in centre:
        ind = min_centre(mat, centre, k)
        if ind != -1:
            centre[ind] = k
            set_index_null(ind, mat)
        k += 1
    return centre



"""Question 2 de VT"""

"""
Donne la liste de degré des sommets
"""
def min_center(mat):
    centre_min = []
    for i in mat :
        nb_arrete_adjacent = 0
        for j in i :
            nb_arrete_adjacent += j
        centre_min.append(nb_arrete_adjacent)
    return centre_min

"""
Envoie la liste des élements qui ont les mêmes degrés
"""
def same_degree(mat,min,marque):
    same = []
    for i in range (len(mat)):
        if(min >= mat[i] and marque[mat.index(mat[i])]!=-1):
            same.append(mat.index(mat[i]))
            mat[i]=-1
    return same
"""

Vérifie si la liste est bien rempli
"""
def checkList(list):
    cond = False
    for i in list :
        if (i == 0) :
            cond = True
    return cond
"""

Supprime un sommet dans le graphe
"""
def delete_sommet(mat_adj,sommet):
    for j in range(len(mat_adj)) :
        mat_adj[sommet][j] =0
        mat_adj[j][sommet] =0
    return mat_adj

"""

Teste le marque du sommet
"""
def test_cas(mat,int,marque):
    cond = False
    for i in mat:
        if (i <= int and marque[mat.index(i)] !=-1):
            cond=True
    return cond

"""

La fontion Dégénérescence d'un graphe
"""
def degenerescence(path_graphe):
    mat_adj = [[0,1,1,1,1,1,0,0,0,0],[1,0,0,0,0,0,1,0,0,0],[1,0,0,1,1,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0],[1,0,1,0,0,1,1,0,0,0],[1,0,0,1,1,0,1,1,1,1],[0,1,0,0,1,1,0,1,0,0],[0,0,0,0,0,1,1,0,1,0],[0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,1,0,0,0,0]]
    numero_centre = [0]*len(mat_adj)
    nb_adj = min_center(mat_adj)
    marque_cas =[0]*len(mat_adj)
    k = 1
    while (checkList(numero_centre)):
        nb_adj = min_center(mat_adj)
        if(test_cas(nb_adj,k,marque_cas)):
            nb_centre_iden = same_degree(nb_adj,k,marque_cas)
            for i in nb_centre_iden: 
                delete_sommet(mat_adj,i)
                numero_centre[i] = k
                marque_cas[i] =-1
                """nb_adj = min_center(mat_adj)"""
        else :
            k +=1
    return numero_centre

m = read_file("../graph/network_list.csv")
print(degenerescence("../graph/network_list.csv"))

