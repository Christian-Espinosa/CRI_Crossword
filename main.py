from Tablero import *
from Palabra import *
import numpy as np

def BuscaParaulesHor(M):
    words = []
    #L = 8
    #while L > 1:
    for i in range(6):
        zcount = 0
        for e in range(6):
            m = M[i][e]
            if m =='#':
                if zcount > 1:
                    words.append(zcount)
                zcount = 0
            elif m==0:
                zcount=zcount+1
            e=e+1
        if zcount > 1:
            words.append(zcount)
        zcount=0
        i=i+1
    return words

def BuscaParaulesVer(M):
    words = []
    for e in range(6):
        zcount = 0
        for i in range(6):
            m = M[i][e]
            if m =='#':
                if zcount > 1:
                    words.append(zcount)
                zcount = 0
            elif m==0:
                zcount=zcount+1
            i=i+1
        if zcount > 1:
            words.append(zcount)
        zcount=0
        e=e+1
    return words


def getDicWords(loc):
    f = open(loc)
    l = [l.strip() for l in f]
    return l
def listOfLists(l):
    d = {}
    for i in l:
        d.setdefault(len(i),[]).append(i)
    return d

def build(l):
    tablero =[]
    l_palabras = []
    palabra_max = 0;

    fila = 0
    for i in range(len(l)):
        w_l = []
        p = 0
        col = 0
        for c in l[i]:
            if c == "0":
                col = col + 1
                w_l.append(" ")
                p = p+1
                if palabra_max < p:
                    palabra_max = p
            if col==(len(l[i])-(col-1)):
                if p > 1:
                    l_palabras.append(Palabra(fila-p, col, p, True))
            if (c=="#"):
                if p > 1:
                    l_palabras.append(Palabra(fila-p, col, p, True))
                col = col + 1
                w_l.append("#")

                if palabra_max < p:
                    palabra_max = p
                p = 0

        fila = fila + 1
        tablero.append(w_l)

    #Buscar palabras por columnas
    p = 0
    for col in range(len(tablero[0])):
        for fila in range(len(tablero)):
            c = tablero[fila][col]
            if (c == "#" or fila == len(tablero)-1):
                if c == " ":
                    p = p + 1
                if p > 1:
                    l_palabras.append(Palabra(fila, col-p, p, False))
                if palabra_max < p:
                    palabra_max = p
                p = 0
            elif(c==" "):
                p = p + 1

    return tablero, palabra_max, l_palabras


""" funció que retornarà una llista de dominis assignats a cada variable. Assignarà un domini propi d'entre totes les 
    paraules del nostre alfabet (possible_words) a cada variable.
"""


def assign_domains(variables, possible_words):
    return False

"""
LVA:llista de variables assignades, inicialment està buida
LVNA:llista de variables no assignades, inicialment conté totes les variables
R: conjunt de restriccions que s'han de complir per poder assignar un valor a una variable
D:llista dels dominis de cadascuna de les variables, aquests s'aniran reduïnt amb el forward checking
var_plus_value: tupla variable-valor que conté la variable var a la que se li assignarà el valor value
"""

""" funcio que actualitza el domini de les variables no assignades, segons l'assignació que acabem de fer"""

def update_domain(var_plus_value,LVNA,R):
    return False


"""funcio que comprova si un determinat valor value assignat a la variable var compleix les restriccions amb la 
resta de les variables assignades"""

def meets_restrictions(var_plus_value,LVA,R):
    return False


"""funció que donada una solució comprova si es completa, és a dir si han sigut assignades totes les variables"""


def is_complete(solution):
    return False

"""funció que resoldrà el problema aplicant l'algorisme de Backtracking amb l'heurística de forward-checking aplicada
    que ens permetrà evitar fallades mitjançant l'eliminació de valors del domini de les variables quan s'assigna un
    valor a una d'elles"""

def BackForwardChecking(LVA,LVNA,R,D):
    #Si LVNA buida llavors retornar LVA
    if len(LVNA) == 0:
        return LVA
    # guardem en una variable la primera de les variables de la llista LVNA
    var = LVNA[0]

    # per cada valor en el domini de var
    for value in D[var]:
        #si el valor que volem assignar a la variable satisfà les restriccions
        if meets_restrictions([var,value],LVA,R):
            """si el domini s'ha actualitzat correctament ( no hi han hagut variables que es quedin sense valors al seu 
                domini) update_domain() retorna true, si eliminant aquest value del domini alguna variable s'ha quedat
                sense possibles valors retorna false"""
            if update_domain([var,value],LVNA,R,D):
                """ cridem recursivament a la funció BackForwardChecking amb les llistes LVA i LVNA actualitzades
                segons la nova assignació. Passem LVA amb un nou element i passem LVNA sense la variable que acabem
                d'assignar"""
            solution = BackForwardChecking(np.append(LVA,[var,value]),LVNA[1:],R,D)
            # si solution es una solució completa retornem solution
            if is_complete(solution):
                return solution
    # fallada
    return False

def main():
    file_dic = "MaterialsPractica1/diccionari_CB_v2.txt"
    file_cross = "MaterialsPractica1/crossword_CB_v2.txt"
    #Diccionario de palabras por length
    dic = listOfLists(getDicWords(file_dic))

    #t = tablero donde vamos a poner las palabras
    #max_p = length palabra maxima
    #l_palabras = lista de posibles palabras que pueden haber en el tablero

    t, max_p, l_palabras = build(getDicWords(file_cross))
    print(t)
    print(max_p)
    print(len(l_palabras))

    #Tablero
    Tablero(t, max_p)

    #search palabra grande y probar



if __name__ == '__main__':
    main()