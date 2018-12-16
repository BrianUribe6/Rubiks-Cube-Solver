class Cube:
    def __init__(self):
        self.white = ['W' for _ in range(9)]
        self.yellow = ['Y' for _ in range(9)]
        self.red = ['R' for _ in range(9)]
        self.orange = ['O' for _ in range(9)]
        #self.orange[6::1] = ['C', 'C', 'C']  # ---> para fines de prueba
        self.green = ['G' for _ in range(9)]
        self.blue = ['B' for _ in range(9)]

    def get_nivel(self, nivel=0):
        """Retorna un string que contiene una linea(nivel) con las piezas naranjas, blancas, rojas, amarillas
        respectivamente. primer nivel = 0, segundo nivel = 3, tercer nivel = 6 en un cubo 3x3"""
        linea = ""
        final = nivel + 3
        for o in range(nivel, final):
            linea += str(o) + self.orange[o] + '  '
        for w in range(nivel, final):
            linea += str(w) + self.white[w] + '  '
        for r in range(nivel, final):
            linea += str(r) + self.red[r] + '  '
        for y in range(nivel, final):
            linea += str(y) + self.yellow[y] + '  '
        return linea

    def show(self):
        """ Muestra el estado actual de cada una de las caras en 2D, esta funcion es temporal para comprobar
        el funcionamiento de los algoritmos y sera eliminada una vez implementemos una GUI"""

        # Contador para indicar cuando ir a la siguiente linea
        row_size = 3
        # Mostrando las azules
        for idx, b in enumerate(self.blue):
            # si la linea finalizo
            if row_size == 0:
                #  Reiniciar contador y continuar en la siguiente linea
                row_size = 3
                print('')
            #  Posicionar la capa
            if row_size == 3:
                blk = ' ' * row_size * 4  # El 4 es = Index+Caracter + (dos espacios vacios que dejas)
                print(blk, end='')
            print(str(idx) + b, ' ', end='')
            row_size -= 1
        print('')
        # Mostrando las naranjas, blancas, rojas y amarillas
        for nivel in range(0, 9, 3):
            print(self.get_nivel(nivel))

        row_size = 3  # Reinicio el contador para evitar problemas al imprimir las verdes
        # Mostrando las verdes
        for idx, g in enumerate(self.green):
            # si la linea finalizo
            if row_size == 0:
                #  Reiniciar contador y continuar en la siguiente linea
                row_size = 3
                print('')
            if row_size == 3:
                blk = ' ' * row_size * 4  # El 4 es = Index+Caracter + (dos espacios vacios que dejas)
                print(blk, end='')
            print(str(idx) + g, ' ', end='')
            row_size -= 1
        print('')

    def move(self, letra):
        if letra == 'R':
            col = self.green[2::3]  # var temporal para almacenar el valor de la verde
            self.green[2::3] = self.yellow[0::3]
            self.yellow[0::3] = self.blue[2::3]
            self.blue[2::3] = self.white[2::3]
            self.white[2::3] = col
            self.red = rot(self.red)

        elif letra == 'L':
            col = self.yellow[2::3]
            self.yellow[2::3] = self.green[0::3]
            self.green[0::3] = self.white[0::3]
            self.white[0::3] = self.blue[0::3]
            self.blue[0::3] = col
            self.orange = rot(self.orange, -90)

        elif letra == 'U':
            row = self.green[0:3]
            self.green[0:3] = self.red[0:3]
            self.red[0:3] = self.blue[0:3]
            self.blue[0:3] = self.orange[0:3]
            self.orange[0:3] = row
            self.white = rot(self.white)

        elif letra == 'D':
            row = self.orange[6:]
            self.orange[6:] = self.blue[6:]
            self.blue[6:] = self.red[6:]
            self.red[6:] = self.green[6:]
            self.green[6:] = row
            self.yellow = rot(self.yellow)
        elif letra == "R'":
            col = self.white[2::3]
            self.white[2::3] = self.blue[2::3]
            self.blue[0::3]= self.yellow[2::3]
            self.yellow[2::3] = self.green[2::3]
            self.green[2::3] = col
            self.red = rot(self.red, -90)
        elif letra == "L'":
            col = self.green[0::3]
            self.green[0::3]=self.yellow[0::3]
            self.yellow[0::3]=self.blue[2::3]
            self.blue[2::3]=self.white[0::3]
            self.white[0::3]=col
            self.orange = rot(self.orange, -90)
        elif letra == "U'":
           row = self.green[0:3]
           self.green[0:3] = self.orange[0:3]
           self.orange[0:3] = self.blue[0:3]
           self.blue[0:3] = self.red[0:3]
           self.red[0:3] = row
           self.white = rot(self.white, -90)
        elif letra == "D'":
            row = self.green[6:]
            self.green[6:] = self.red[6:]
            self.red[6:] = self.blue[6:]
            self.blue[6:]=self.orange[6:]
            self.orange[6:] = row
            self.yellow = rot(self.yellow)
        else:
            print("ERROR")
# Esta funcion rota una cara en 90 y -90 grados
def rot(face, deg=90):
    face_aux = []
    if deg == 90:
        for i in range(3):
            """ Transpone las las columnas, "volteadas" por las filas """
            face_aux.extend(reversed(face[i::3]))
    else:
        for i in range(3):
            """ Aquí coloco el 2-i par aque se intercambien las columnas en orden inverso al de las filas
            esto es porque la rotacion en scmr """
            face_aux.extend(face[2 - i::3])
    return face_aux


cubo = Cube()
#cubo.show()
cubo.move("D'")
cubo.show()