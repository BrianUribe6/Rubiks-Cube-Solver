import cv2
import numpy as np

imagen = cv2.imread('cube.jpg',cv2.IMREAD_COLOR)
# Esto es para facilitar las coordenades de las regiones
resized_image = cv2.resize(imagen, (250, 178))
hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV) # Pasa la imagen escalada al formato HSV

# Dibujando las regiones
# img = cv2.rectangle(resized_image,(25,15),(50,40),(126,255,11),2)
# img = cv2.rectangle(resized_image,(110,15),(135,40),(126,255,11),2)
# img = cv2.rectangle(resized_image,(195,15),(220,40),(126,255,11),2)
#
# img = cv2.rectangle(resized_image,(25,75),(50,100),(126,255,11),2)
# img = cv2.rectangle(resized_image,(110,75),(135,100),(126,255,11),2)
# img = cv2.rectangle(resized_image,(195,75),(220,100),(126,255,11),2)
#
# img = cv2.rectangle(resized_image,(25,135),(50,160),(126,255,11),2)
# img = cv2.rectangle(resized_image,(110,135),(135,160),(126,255,11),2)
# img = cv2.rectangle(resized_image,(195,135),(220,160),(126,255,11),2)


# Rango de colores detectados:
# Verdes:
verde_bajos = np.array([49, 50, 50], dtype=np.uint8) # np.unit8 es para un rango de colores de 8bits (0-255)
verde_altos = np.array([90, 255, 255], dtype=np.uint8)
# Azules:
azul_bajos = np.array([100, 65, 75], dtype=np.uint8)
azul_altos = np.array([130, 255, 255], dtype=np.uint8)
# Rojos:
rojo_bajos1 = np.array([0, 75, 75], dtype=np.uint8)
rojo_altos1 = np.array([5, 255, 255], dtype=np.uint8)
rojo_bajos2 = np.array([160,50,50], dtype=np.uint8)
rojo_altos2 = np.array([180,255,255], dtype=np.uint8)
# Amarillos
amarillos_altos = np.array([42, 255, 255], dtype=np.uint8)
amarillos_bajos = np.array([19, 191, 125], dtype=np.uint8)
#Blancos
blancos_altos = np.array([255, 50, 255], dtype=np.uint8)
blancos_bajos = np.array([0, 0, 178], dtype=np.uint8)
# Naranjas
naranjas_altos = np.array([15, 255 , 255], dtype=np.uint8)
naranjas_bajos = np.array([5, 100 , 200], dtype=np.uint8)

# Crear las mascaras
mascara_azul = cv2.inRange(hsv, azul_bajos, azul_altos)  # Crea las mascaras uniendo los rangos bajos y altos
mascara_verde = cv2.inRange(hsv, verde_bajos, verde_altos)
mascara_rojo1 = cv2.inRange(hsv, rojo_bajos1, rojo_altos1)
mascara_rojo2 = cv2.inRange(hsv, rojo_bajos2, rojo_altos2)
mascara_blanca = cv2.inRange(hsv,blancos_bajos,blancos_altos)
mascara_amarilla = cv2.inRange(hsv,amarillos_bajos,amarillos_altos)
mascara_naranja = cv2.inRange(hsv,naranjas_bajos,naranjas_altos)
# Juntar los rojos
''' Esto es porque el rojo se divide en dos rangos, los de la izquierda de la escala (cercanos al amarillo) y los de la
derecha (cercanos al azul)'''
mascara_rojo = cv2.add(mascara_rojo1, mascara_rojo2)

# Array con todas las mascaras
mascaras= [mascara_blanca, mascara_naranja, mascara_verde, mascara_rojo, mascara_azul,mascara_amarilla]

def regiones(mascara):
    """Esta función toma las regiones(trozos de la imagen) y las convierte en un array"""
    mapa = [mascara[15:40,25:50], mascara[15:40,110:135], mascara[15:40,195:220],
            mascara[75:100,25:50], mascara[75:100,110:135], mascara[75:100,195:220],
            mascara[135:160,25:50], mascara[135:160,110:135], mascara[135:160,195:220]]
    return  mapa

def iscolor(region,size = 25, accuracy = 0.7):
    """ Esta función toma una region de la imagen y compara los pixeles individualmente y luego retorna true o false si
    si los pixeles superan la precision establecida"""
    n = 0
    for w in range(size):
        for h in range(size):
            if np.all(region[w,h] == [255, 255, 255]):
                n += 1
    if n >= size * size * accuracy:
        return True
    else:
        return False

def masktoarr(mascaras):
    """Toma las regiones, de todas las mascaras, y las pasa por la funcion iscolor para crea un array con los colores"""
    arr = []
    color = ['W','O','G','R','B','Y'] # Para evitar poner 6 if
    for i in range(9):
        for j in range(6):
            reg = regiones(mascaras[j])
            if iscolor(reg[i]):
                arr.append(color[j])
    return arr

# Mostrar las mascara y la imagen original
cv2.imshow('Mask_White',mascara_blanca)
cv2.imshow('Mask_Blue',mascara_azul)
cv2.imshow('Mask_Green',mascara_verde)
cv2.imshow('Mask_Yellow',mascara_amarilla)
cv2.imshow('Mask_Orange',mascara_naranja)
cv2.imshow('Mask_Red',mascara_rojo)
cv2.imshow('Original',resized_image)

print(masktoarr(mascaras))

# Salir con ESC para los "visores" de imagen
while (1):
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        break

cv2.destroyAllWindows()

