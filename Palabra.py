
class Palabra:
    #Principio de palabra
    fila = 0
    col = 0
    longitud = 0
    #Horizontal=True/Vertical=False
    orientacion = True
    # afegim un atribut que serà una llista d'interseccions amb les quals està relacionada la paraula per controlar les
    # restriccions
    intersect_list = []
    # atribut que guardarà el valor que posarem finalment al taulell
    valor = ""
    # identificador de variable
    id = 0

    def __init__(self, x, y, l, o, id):
        self.fila = x
        self.col = y
        self.longitud=l
        self.orientacion=o
        self.id = id

    def set_value(self, string):
        self.valor = string

