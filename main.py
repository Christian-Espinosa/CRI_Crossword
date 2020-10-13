from Tablero import *
from Palabra import *
import numpy as np
import copy as cp

def getDicWords(loc):
    f = open(loc)
    l = [l.strip() for l in f]
    return l
def listOfLists(l):
    d = {}
    for i in l:
        d.setdefault(len(i), []).append(i)
    return d


def build(l):
    tablero =[]
    l_palabras = []
    palabra_max = 0
    id = 0

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
            if col == (len(l[i])-(col-1)):
                if p > 1:
                    # l_palabras.append(Palabra(fila-p, col, p, True))
                    l_palabras.append(Palabra(fila, col-p, p, True, id))
                    id += 1
            if (c=="#"):
                if p > 1:
                    # l_palabras.append(Palabra(fila-p, col, p, True))
                    l_palabras.append(Palabra(fila, col-p, p, True, id))
                    id += 1
                col = col + 1
                w_l.append("#")

                if palabra_max < p:
                    palabra_max = p
                p = 0

        fila = fila + 1
        tablero.append(w_l)

    #Buscar palabras por columnas
    p = 0
    # problema: detecta paraules que no ho son
    for col in range(len(tablero[0])):
        for fila in range(len(tablero)):
            c = tablero[fila][col]
            if c == "#" or fila == len(tablero)-1:
                if c == " ":
                    p = p + 1
                if p > 1:
                    # l_palabras.append(Palabra(fila, col-p, p, False))
                    # comprovem si aquella fila ja té una paraula que passa per aquesta posició
                    w = Palabra(max([fila-p, 0]), col, p, False, id)
                    if not taken_row(w, l_palabras):
                        l_palabras.append(w)
                        id += 1
                if palabra_max < p:
                    palabra_max = p
                p = 0
            elif(c==" "):
                p = p + 1

    return tablero, palabra_max, l_palabras


"""funció que detectarà si ja hi ha alguna paraula en aquella fila i servirà per evitar que detectem com a paraules, coses
   que no ho son"""


def taken_row(possible_word, words):
    # farem un recorregut per les posicions on passa la paraula comprovant si per allà hi passa alguna altra paraula. Si
    # hi ha alguna fila on no hi hagi cap paraula en aquella posició, si que podrem afegir la paraula(False). Si no no podrem
    # (True)
    taken_rows = 0
    for row in range(possible_word.fila, possible_word.fila+possible_word.longitud+1):
        # passem per les diferents paraules ja detectades
        for word in words:
            # si aquella paraula està en la fila actual i es una paraula horitzontal
            if word.orientacion is True and word.fila == row:
                # si aquella paraula passa per la columna on es situa la nostre possible paraula, augmentem les files
                # ocupades en 1
                if word.col+word.longitud >= possible_word.col:
                    taken_rows += 1
    # si les files ocupades son iguals a la longitud de la possible paraula, llavors no hi pot haver paraula allà i retornem
    # True
    if taken_rows == possible_word.longitud:
        return True
    # si no retornem False, amb lo qual podrem afegir la paraula
    return False


""" métode que assignarà a cada variable les seves interseccions amb altres variables. """


def assign_intersections(variables):
    # covered_vars es una llista que anirà guardant aquelles variables ja procesades. I així aprofitant la simetria
    # de la intersecció (a intersectat amb b) == (b intersectat amb a) només recorrem un cop aquestes variables
    covered_vars = []
    # llista per a guardar les interseccions
    partial_list = []
    # recorrem la llista de variables
    for var in variables:
        # tornem a recorrer la llista, de manera que per a cada variable farem les comparacions amb totes les altres
        for var_ in variables:
            # comprovem que la variable var_ no estigui a covered_vars per evitar operacions innecesàries
            if var_.id not in covered_vars:
                # si var i var_ no son la mateixa variable
                if var.id != var_.id:
                    # comprovem que les orientacions de var i var_ siguin diferents. Si fossin iguals és impossible que
                    # hi hagi una intersecció
                    if var.orientacion != var_.orientacion:
                        # si var_ està orientada verticalment
                        if var_.orientacion is False:
                            # Primer hem de comprovar si la columna de var es més petita que la columna de var_.
                            # Si la columna de var més la seva longitud menys 1( hem de tenir en compte la columna 0)
                            # es més gran o igual que la columna on es troba var_sabem que la paraula de var passarà per
                            # la columna de var_. Hem de fer la comparació simètrica desde var_ pero en aquest cas sobre
                            # les files
                            if var.col <= var_.col and var.col+var.longitud-1 >= var_.col and \
                                    (var_.fila <= var.fila and var_.fila + var_.longitud-1 >= var.fila):
                                # assignem la intersecció a cada variable. La intersecció es produeix a la fila de var i a la
                                # columna de var_
                                var.intersect_list.append([var.fila, var_.col])
                                partial_list = cp.deepcopy(var.intersect_list)
        covered_vars.append(var.id)

    # necessitem fer això ja que cada cop que fem un append en la llista d'interseccions d'alguna de les variables es fa
    # en totes. Llavors aquí el que farem es seleccionar les interseccions per a cada variable

    # recorrem la llista de variables
    for varb in variables:
        # variables en horitzontal
        if varb.orientacion is True:
            varb.intersect_list = [intersection for intersection in partial_list if intersection[0] == varb.fila]
        # variables en vertical
        else:
            varb.intersect_list = [intersection for intersection in partial_list if intersection[1] == varb.col]




""" funció que retornarà una llista de dominis assignats a cada variable. Assignarà un domini propi d'entre totes les 
    paraules del nostre alfabet (possible_words) a cada variable.
"""


def assign_domains(variables, possible_words):
    # creem un diccionari que contindrà un domini per a cada variable(Paraula). Les claus son els identificadors de cada
    # variable i el valor és el seu domini

    Domain = {}
    # recorrem la llista de variables i assignem a cada variable el seu domini( aquelles paraules que tenen la mateixa
    # longitud
    for var in variables:
        Domain[var.id] = possible_words[var.longitud]
    return Domain

"""
LVA:llista de variables assignades, inicialment està buida
LVNA:llista de variables no assignades, inicialment conté totes les variables
R: conjunt de restriccions que s'han de complir per poder assignar un valor a una variable
***RESTRICCIONS :
-Longitud de la paraula(Eliminada ja que usem un diccionari, i només accedirem a aquelles possibles paraules que estiguin al domini de cada variable)
-Interseccions: cal tindre en compte si hi ha intersecció en la variable a la que anem a donar el valor així com amb quina variable es produeix
la intersecció, si aquesta ja esta plena, i en quina posició de cada variable es troba la intersecció
Si la variable amb la que es comparteix la intersecció està plena s'haurà de filtrar el domini tenint en compte quina lletra
hi ha en aquella posició i per tant descartant aquelles paraules que no la contiguin. 
BÁSICAMENT SERÀN LES INTERSECCIONS, JA QUE LES LONGITUDS LES CONTROLEM AMB LA NOSTRA ESTRUCTURA DE DADES
***
D:llista dels dominis de cadascuna de les variables, aquests s'aniran reduïnt amb el forward checking
var_plus_value: tupla variable-valor que conté la variable var a la que se li assignarà el valor value
"""

""" funcio que actualitza el domini de les variables no assignades, segons l'assignació que acabem de fer"""


def update_domain(var_plus_value, LVNA, D):

    D = {dk: [value for value in dv if value is not var_plus_value[1]] for (dk, dv) in D.items()}
    # si var s'ha quedat sense valors en el seu domini retornem False
    for var in LVNA:
        if len(D[var.id]) == 0:
            return False, D
    return True, D


"""funcio que comprova si un determinat valor value assignat a la variable var compleix les restriccions amb la 
resta de les variables assignades"""


def meets_constraints(var_plus_value, LVA):
    #recorrem la llista de les variables assignades
    for var in LVA:
        # recorrem la llista d'interseccions de var
        for intersection in var.intersect_list:
            # si la intersecció està en la llista de var i de la variable que vol ser assignada
            if intersection in var_plus_value[0].intersect_list:
                # si var està situada horitzontalment
                if var.orientacion is True:
                    # si el valor(paraula) que volem assignar a la variable no conté la mateixa lletra que la paraula de var
                    #  en la posició de la intersecció retornem False. UNA DE LES RESTRICCIONS JA NO ES COMPLEIX
                    if var_plus_value[1][intersection[0]] != var.valor[intersection[1]]:
                        return False
                else:
                    if var_plus_value[1][intersection[1]] != var.valor[intersection[0]]:
                        return False


    # si s'ha complert totes les restriccions retornem True
    return True


"""funció que donada una solució comprova si es completa, és a dir si han sigut assignades totes les variables"""


def is_complete(solution, n_words):
    # recorrem les variables de la solució , si han sigut totes assignades retornem True, si alguna no ha sigut assignada
    # retornem False
    if len(solution) != n_words:
        return False
    for var in solution:
        if var.valor == "":
            return False
    return True

"""funció que resoldrà el problema aplicant l'algorisme de Backtracking amb l'heurística de forward-checking aplicada
    que ens permetrà evitar fallades mitjançant l'eliminació de valors del domini de les variables quan s'assigna un
    valor a una d'elles"""


def BackForwardChecking(LVA,LVNA,D,n_words):
    #Si LVNA buida llavors retornar LVA
    if len(LVNA) == 0:
        return LVA
    # guardem en una variable la primera de les variables de la llista LVNA
    var = LVNA[0]

    # per cada valor en el domini de var
    for value in D[var.id]:
        #si el valor que volem assignar a la variable satisfà les restriccions
        if meets_constraints([var, value], LVA):
            """si el domini s'ha actualitzat correctament ( no hi han hagut variables que es quedin sense valors al seu 
                domini) update_domain() retorna true, si eliminant aquest value del domini alguna variable s'ha quedat
                sense possibles valors retorna false"""
            fine_domains, D = update_domain([var, value], LVNA, D)
            if fine_domains:
                """ cridem recursivament a la funció BackForwardChecking amb les llistes LVA i LVNA actualitzades
                segons la nova assignació. Passem LVA amb un nou element i passem LVNA sense la variable que acabem
                d'assignar"""
                var.set_value(value)
                tmp = cp.deepcopy(LVA)
                tmp.append(var)
                solution = BackForwardChecking(tmp, LVNA[1:], D, n_words)
                # si solution es una solució completa retornem solution
                if is_complete(solution, n_words):
                    return solution
    # fallada
    return LVA


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
    Dom = assign_domains(l_palabras, dic)
    assign_intersections(l_palabras)

    resultat = BackForwardChecking([], l_palabras, Dom, len(l_palabras))
    print(resultat)
    #search palabra grande y probar



if __name__ == '__main__':
    main()