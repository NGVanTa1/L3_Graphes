"""
Lit le fichier au format CSV en paramètre et renvoie la matrice d'adjacence du graphe décrit
"""
from cgi import print_form
from curses import flash
from itertools import count
from operator import index, indexOf
from pickle import TRUE
from traceback import print_list
from turtle import clear
import time
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

mat_adj_test = [[0,1,1,1,1,1,0,0,0,0],[1,0,0,0,0,0,1,0,0,0],[1,0,0,1,1,0,0,0,0,0],[1,0,1,0,0,1,0,0,0,0],[1,0,1,0,0,1,1,0,0,0],[1,0,0,1,1,0,1,1,1,1],[0,1,0,0,1,1,0,1,0,0],[0,0,0,0,0,1,1,0,1,0],[0,0,0,0,0,1,0,1,0,0],[0,0,0,0,0,1,0,0,0,0]]
G = nx.Graph()

"""
Traduit un fichier CSV en une matrice d'adjacence de graphe
"""
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
            G.add_edge(a,b)
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
Renvoie la liste des élements qui ont les mêmes degrés
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
Supprime un sommet dans le graphe (met à 0 sa ligne/colonne)
"""
def delete_sommet(mat_adj,sommet):
    for j in range(len(mat_adj)) :
        mat_adj[sommet][j] =0
        mat_adj[j][sommet] =0
    return mat_adj


"""
Vérifie si le sommet est marqué comme déjà vérifié
"""
def test_cas(mat,int,marque):
    cond = False
    for i in mat:
        if (i <= int and marque[mat.index(i)] !=-1):
            cond=True
    return cond


"""
Calcul de la dégénérescence du graphe donné en paramètre, renvoie les numéros de centre des sommets du graphe
"""
def degenerescence(path_graphe):
    start=time.time()
    mat_adj = read_file(path_graphe)
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
                nb_adj = min_center(mat_adj)
        else :
            k +=1
    end=time.time()
    print("Le temps d'execution de l'algorithme de degenerescence est de",end-start)
    return numero_centre

"""Question 3 : Algorithmes de Matula & Beck"""
"""https://stringfixer.com/fr/Degeneracy_(graph_theory)"""
def same_degree_v2(mat,min,L):
    same = []
    mat_copie = mat.copy()
    for i in range (len(mat_copie)):
        if(min == mat[i] and mat_copie.index(min) not in L):
            same.append(mat_copie.index(mat_copie[i]))
            mat_copie[i]= 0
    return same

def list_same_degree(mat,L):
    liste = [[]]*len(mat)
    for i in mat:
        liste[i] = same_degree_v2(mat,i,L)
    return liste

def k_core(mat):
    list_k_core =[]
    for i in mat :
        if i :
            list_k_core.append(mat.index(i))
    return list_k_core[0]


def Algo_Matula_Beck(path_graphe):
    start = time.time()
    mat_adj = read_file(path_graphe)

    """Une liste de sortie L"""
    L = []
    """Liste numéro de centre"""
    k_center = [0]*len(mat_adj)
    """Nombre de voisin de sommet v"""
    d_v = min_center(mat_adj)

    """Un tableau D telque D[i] contient une list des sommets v qui ne sont pas déja dans L pour lesquels d_v =i"""
    D = list_same_degree(d_v,L)

    """Intialiser k à 0"""
    k = 0
    while(len(L)!=len(mat_adj)):
        """Balayez les cellules du tableau D[0,D[1] jusqu'à trouver un i pour le quel D[i] est non vide"""
        index_non_vide = k_core(D)
        """Mettre k à max(k,i)"""
        k = max(k,index_non_vide)
        """Sélectionnez un sommet v de D[i]. Ajoutez v au début de L et supprimez-le de D[i]"""
        for i in range (len(D[index_non_vide])):
            if(D[index_non_vide][i] not in L):
                L.append(D[index_non_vide][i])
                delete_sommet(mat_adj,D[index_non_vide][i])
                k_center[D[index_non_vide][i]]=k
        d_v = min_center(mat_adj)
        D = list_same_degree(d_v,L)
    end = time.time()
    print("Le temps d'execution de l'algorithme Mutala & Beck est de",end-start)
    return k_center


"""Question 3 : Un joli dessin du graphe"""

def diff_value(mat):
    lit=[]
    for i in mat :
        if (i not in lit):
            lit.append(i)
    return lit

def Dessin_Graph(path_graphe):
    pos={}
    tab_centre = degenerescence(path_graphe)
    diff = diff_value(tab_centre)
    index_diff = [1]*len(diff)
    for j in range (len(diff)):
        for i in range(len(tab_centre)):
            if (diff[j] == tab_centre[i]):
                """Remplit les positions de chaque sommet sur le cercle correspondant"""
                theta = (index_diff[j]*2*np.pi)/(tab_centre.count(tab_centre[i]))
                r = 1/np.sqrt(float(tab_centre[i]))
                x = r*np.cos(theta)
                y = r*np.sin(theta)

                pos.update({i :(x, y)})
                index_diff[j] +=1
    """Pour le dessin des cercles degenerescence"""
    H = nx.Graph()
    for i in range(100):
        if i <= 98:
            H.add_edge(i,i+1)
        else:
            H.add_edge(i,0)
    for i in diff :
        pos2 = {}
        alpha = np.linspace(0, 2*np.pi,101)
        r = 1/np.sqrt(i)
        for i in range(101):
            x1 = r*np.cos(alpha)
            x2 = r*np.sin(alpha)
            pos2.update({i :(x1[i], x2[i])})
        """Graphe H : les cercles de dégénéréscence et Graphe G : les sommets du graphe"""
        nx.draw_networkx_nodes(H,pos2,node_size=0)
        nx.draw_networkx_edges(H,pos2,edge_color='red')
        nx.draw_networkx_nodes(G,pos,node_size=200)
    nx.draw_networkx_edges(G,pos,edge_color='xblack')
    nx.draw_networkx_labels(G,pos,font_size=7)
    plt.show()

print("Algorithme Matula_beck : ",Algo_Matula_Beck("../graph/graphe1.csv"))
# print("Algorithme degenerescence : ",degenerescence("graph/graphe3.csv"))
Dessin_Graph("../graph/graphe1.csv")


