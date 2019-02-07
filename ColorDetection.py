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


# Crea las mascaras uniendo los rangos bajos y altos
mascara_azul = cv2.inRange(hsv, (100, 65, 75), (130, 255, 255))
mascara_verde = cv2.inRange(hsv, (49, 50, 50),(90, 255, 255))
mascara_rojo1 = cv2.inRange(hsv, (0, 75, 75), (5, 255, 255))
mascara_rojo2 = cv2.inRange(hsv, (160,50,50), (180,255,255))
mascara_blanca = cv2.inRange(hsv,(0, 0, 178),(255, 50, 255))
mascara_amarilla = cv2.inRange(hsv,(19, 191, 125),(42, 255, 255))
mascara_naranja = cv2.inRange(hsv,(5, 100 , 200),(15, 255 , 255))
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

def iscolor(region,size = 25, accuracy = .7):
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
    """Toma las regiones, de todas las mascaras, y las pasa por la funcion iscolor para crea un string con los colores"""
    face = ''
    color = ['U','L','F','R','B','D'] # Para evitar poner 6 if
    for i in range(9):
        for j in range(6):
            reg = regiones(mascaras[j])
            if iscolor(reg[i]):
                face += color[j]
    return face

# Mostrar las mascara y la imagen original
# cv2.imshow('Mask_White',mascara_blanca)
# cv2.imshow('Mask_Blue',mascara_azul)
# cv2.imshow('Mask_Green',mascara_verde)
# cv2.imshow('Mask_Yellow',mascara_amarilla)
# cv2.imshow('Mask_Orange',mascara_naranja)
# cv2.imshow('Mask_Red',mascara_rojo)
# cv2.imshow('Original',resized_image)

# print(masktoarr(mascaras))

# Salir con ESC para los "visores" de imagen
# while (1):
#     tecla = cv2.waitKey(5) & 0xFF
#     if tecla == 27:
#         break
#
# cv2.destroyAllWindows()