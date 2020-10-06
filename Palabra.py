
class Palabra:
    #Principio de palabra
    fila = 0
    col = 0
    longitud = 0
    #Horizontal=True/Vertical=False
    orientacion = True

    def __init__(self, x, y, l, o):
        self.fila = x
        self.col = y
        self.longitud=l
        self.orientacion=o

