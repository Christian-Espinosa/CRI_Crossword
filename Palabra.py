
class Palabra:
    #Principio de palabra
    coordenadas = []
    longitud = 0
    #Horizontal=True/Vertical=False
    orientacion = True
    p = []
    #dar la vuelta a p
    flip = False

    def __init__(self, coord, l,o,p):
        self.coordenadas=coord
        self.longitud=l
        self.orientacion=o
        self.paraula=p

    def Flip(self):
        self.flip = True
