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

def main():
    filename = "MaterialsPractica1/diccionari_CB_v2.txt"
    dic = listOfLists(getDicWords(filename))
    

if __name__ == '__main__':
    main()