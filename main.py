from Tablero import *
from Palabra import *


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