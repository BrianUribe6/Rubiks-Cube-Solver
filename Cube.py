from random import randint
import kociemba


class Cube:
    def __init__(self):
        self.white = ['%dU' % (w + 1) for w in range(9)]
        self.red = ['%d%s' % (r + 1, 'R') for r in range(9)]
        self.green = ['%d%s' % (g + 1, 'F') for g in range(9)]
        self.yellow = ['%d%s' % (y + 1, 'D') for y in range(9)]
        self.orange = ['%d%s' % (o + 1, 'L') for o in range(9)]
        self.blue = ['%d%s' % (b + 1, 'B') for b in range(9)]

    def get_nivel(self, nivel=0):
        """Retorna un string que contiene una linea(nivel) con las piezas naranjas, blancas, rojas, amarillas
        respectivamente. primer nivel = 0, segundo nivel = 3, tercer nivel = 6 en un cubo 3x3"""
        linea = ""
        final = nivel + 3
        for o in range(nivel, final):
            linea += self.orange[o] + '  '
        for g in range(nivel, final):
            linea += self.green[g] + '  '
        for r in range(nivel, final):
            linea += self.red[r] + '  '
        for b in range(nivel, final):
            linea += self.blue[b] + '  '
        return linea

    def show(self):
        """ Muestra el estado actual de cada una de las caras en 2D, esta funcion es temporal para comprobar
        el funcionamiento de los algoritmos y sera eliminada una vez implementemos una GUI"""

        # Contador para indicar cuando ir a la siguiente linea
        row_size = 3
        # Mostrando las azules
        for w in self.white:
            # si la linea finalizo
            if row_size == 0:
                #  Reiniciar contador y continuar en la siguiente linea
                row_size = 3
                print('')
            #  Posicionar la capa
            if row_size == 3:
                blk = ' ' * row_size * 4  # El 4 es = Index+Caracter + (dos espacios vacios que dejas)
                print(blk, end='')
            print(w, ' ', end='')
            row_size -= 1
        print('')
        # Mostrando las naranjas, blancas, rojas y amarillas
        for nivel in range(0, 9, 3):
            print(self.get_nivel(nivel))

        row_size = 3  # Reinicio el contador para evitar problemas al imprimir las verdes
        # Mostrando las verdes
        for y in self.yellow:
            # si la linea finalizo
            if row_size == 0:
                #  Reiniciar contador y continuar en la siguiente linea
                row_size = 3
                print('')
            if row_size == 3:
                blk = ' ' * row_size * 4  # El 4 es = Index+Caracter + (dos espacios vacios que dejas)
                print(blk, end='')
            print(y, ' ', end='')
            row_size -= 1
        print('')

    def mov(self, letra):
        if letra == 'R':
            # var temporal para almacenar el valor de la verde
            self.green[2::3], self.yellow[2::3], self.blue[::3], self.white[2::3] = \
                self.yellow[2::3], reversed(self.blue[::3]), reversed(self.white[2::3]), self.green[2::3]
            self.red = rot(self.red)

        elif letra == 'L':
            self.yellow[::3], self.green[::3], self.white[::3], self.blue[2::3] = \
                self.green[::3], self.white[::3], reversed(self.blue[2::3]), reversed(self.yellow[::3])
            self.orange = rot(self.orange, 90)

        elif letra == 'U':
            self.green[:3], self.red[:3], self.blue[:3], self.orange[:3] = \
                self.red[:3], self.blue[:3], self.orange[:3], self.green[:3]
            self.white = rot(self.white)

        elif letra == 'D':
            self.orange[6:], self.blue[6:], self.red[6:], self.green[6:] = \
                self.blue[6:], self.red[6:], self.green[6:], self.orange[6:]
            self.yellow = rot(self.yellow)

        elif letra == "R'":
            self.white[2::3], self.blue[::3], self.yellow[2::3], self.green[2::3] = \
                reversed(self.blue[::3]), reversed(self.yellow[2::3]), self.green[2::3], self.white[2::3]
            self.red = rot(self.red, -90)

        elif letra == "L'":
            self.green[::3], self.yellow[::3], self.blue[2::3], self.white[::3] = \
                self.yellow[::3], reversed(self.blue[2::3]), reversed(self.white[::3]), self.green[0::3]
            self.orange = rot(self.orange, -90)

        elif letra == "U'":
            self.green[:3], self.orange[:3], self.blue[:3], self.red[:3] = \
                self.orange[0:3], self.blue[0:3], self.red[0:3], self.green[:3]
            self.white = rot(self.white, -90)

        elif letra == "D'":
            self.green[6:], self.red[6:], self.blue[6:], self.orange[6:] = \
                self.red[6:], self.blue[6:], self.orange[6:], self.green[6:]
            self.yellow = rot(self.yellow, -90)

        elif letra == 'F':
            self.white[6:], self.orange[2::3], self.yellow[:3], self.red[::3] = \
                reversed(self.orange[2::3]), self.yellow[:3], reversed(self.red[::3]), self.white[6:]
            self.green = rot(self.green)

        elif letra == 'B':
            self.white[:3], self.red[2::3], self.yellow[6:], self.orange[::3] = \
                self.red[2::3], reversed(self.yellow[6:]), self.orange[::3], reversed(self.white[:3])
            self.blue = rot(self.blue)

        elif letra == "F'":
            self.white[6:], self.red[::3], self.yellow[:3], self.orange[2::3] = \
                self.red[::3], reversed(self.yellow[:3]), self.orange[2::3], reversed(self.white[6:])
            self.green = rot(self.green, -90)

        elif letra == "B'":
            self.white[:3], self.orange[::3], self.yellow[6:], self.red[2::3] = \
                reversed(self.orange[::3]), self.yellow[6:], reversed(self.red[2::3]), self.white[:3]
            self.blue = rot(self.blue, -90)

        elif letra == "U2":
            self.green[:3], self.blue[:3] = self.blue[:3], self.green[:3]
            self.red[:3], self.orange[:3] = self.orange[:3], self.red[:3]
            self.white = rot(self.white, 180)
        elif letra == "R2":
            self.white[2::3], self.yellow[2::3] = self.yellow[2::3], self.white[2::3]
            self.green[2::3], self.blue[0::3] = reversed(self.blue[0::3]), reversed(self.green[2::3])
            self.red = rot(self.red, 180)
        elif letra == "L2":
            self.white[::3], self.yellow[::3] = self.yellow[::3], self.white[::3]
            self.green[::3], self.blue[2::3] = reversed(self.blue[2::3]), reversed(self.green[::3])
            self.orange = rot(self.orange, 180)
        elif letra == "D2":
            self.green[6:], self.blue[6:] = self.blue[6:], self.green[6:]
            self.red[6:], self.orange[6:] = self.orange[6:], self.red[6:]
            self.yellow = rot(self.yellow, 180)
        elif letra == "F2":
            self.white[6:], self.yellow[:3] = reversed(self.yellow[:3]), reversed(self.white[6:])
            self.red[::3], self.orange[2::3] = reversed(self.orange[2::3]), reversed(self.red[::3])
            self.green = rot(self.green, 180)
        elif letra == "B2":
            self.white[:3], self.yellow[6:] = reversed(self.yellow[6:]), reversed(self.white[:3])
            self.red[2::3], self.orange[::3] = reversed(self.orange[::3]), reversed(self.red[2::3])
            self.blue = rot(self.blue, 180)
        else:
            print("ERROR")

    def mov_sq(self, sequence):
        pasos = sequence.split()
        for p in pasos:
            self.mov(p)

    def shuffle(self):
        """Ejecuta el scramble generado por la funcion y deja el cubo en un estado no resuelto"""
        secuencia = scramble()
        self.mov_sq(secuencia)
        return secuencia

    def solve(self):
        """
        Enumera los elementos de cada cara en el orden: blanco rojo, verde, amarillo, naranja y azul respectivamente
        y retorna un string con dichos elementos. un cubo resuelto produciria el siguiente string:
        UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
        Una vez obtenido el patron del cubo se utiliza el algoritmo de kociemba para obtener la solucion y se ejecuta
        el mismo.
        """

        kociemba_sequence = ''
        for u in self.white:
            kociemba_sequence += u[1]
        for r in self.red:
            kociemba_sequence += r[1]
        for f in self.green:
            kociemba_sequence += f[1]
        for d in self.yellow:
            kociemba_sequence += d[1]
        for l in self.orange:
            kociemba_sequence += l[1]
        for b in self.blue:
            kociemba_sequence += b[1]

        solution = kociemba.solve(kociemba_sequence)
        self.mov_sq(solution)
        return solution


def scramble():
    """Genera un algoritmo de 20 movimientos para barajar el cubo y retorna el mismo como un string
    separado por espacios. El algoritmo toma en cuenta el movimiento realizado anteriormente y evita repetirlo.
    Todos los movimientos que contengan la misma designacion son considerados iguales."""

    positions = ["R", "R'", "R2", "L", "L'", "L2", "U", "U'", "U2", "D", "D'", "D2", "F", "F'", "F2", "B", "B'",
                 "B2"]
    scramble_size = 20
    scramble_algo = ""

    # mantiene registro del ultimo movimiento realizado para evitar repeticiones
    # inicializado en 0 para tener un caracter con el que comparar el primer movimiento
    prev_move = '0'
    for move in range(scramble_size):
        random_idx = randint(0, len(positions) - 1)
        while prev_move[0] in positions[random_idx]:  # Si el movimiento es repetido
            random_idx = randint(0, len(positions) - 1)
        prev_move = positions[random_idx]  # actulizando movimiento anterior
        scramble_algo += positions[random_idx] + ' '

    return scramble_algo


def rot(face, deg=90):
    """Esta funcion rota las caras en 90, 180, -90"""
    face_aux = []
    if deg == 90:
        for i in range(3):
            # Transpone las las columnas, "volteadas" por las filas
            face_aux.extend(reversed(face[i::3]))
    elif deg == -90:
        for i in range(3):
            ''' Aquí coloco el 2-i par aque se intercambien las columnas en orden inverso al de las filas
            esto es porque la rotacion en scmr '''
            face_aux.extend(face[2 - i::3])
    elif deg == 180:
        # Rotacion de 180
        face_aux.extend(reversed(face))
    else:
        # Hmm ... por si acaso
        face_aux = face
    return face_aux


cubo = Cube()
scramble_alg = cubo.shuffle()
print("Scramble:", scramble_alg)
print('')
cubo.show()
print('')
solution = cubo.solve()
print("Solucion:", solution)
print('')
cubo.show()
