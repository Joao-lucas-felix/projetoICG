# painter_modular.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import sys

# ------------------------------------------------------
# Funções para criar cubo e esfera
# ------------------------------------------------------
def create_cube(center=(0,0,0), size=1.0, color=(1,0,0)):
    cx, cy, cz = center
    s = size / 2.0
    vertices = [
        (cx-s, cy-s, cz-s), (cx+s, cy-s, cz-s), (cx+s, cy+s, cz-s), (cx-s, cy+s, cz-s),
        (cx-s, cy-s, cz+s), (cx+s, cy-s, cz+s), (cx+s, cy+s, cz+s), (cx-s, cy+s, cz+s),
    ]
    faces = [
        (0,1,2,3), (4,5,6,7), (0,1,5,4),
        (2,3,7,6), (1,2,6,5), (0,3,7,4),
    ]
    polys = []
    for f in faces:
        v = [np.array(vertices[i]) for i in f]
        polys.append({"vertices":[v[0], v[1], v[2]], "color": color})
        polys.append({"vertices":[v[0], v[2], v[3]], "color": color})
    return polys

def create_sphere(center=(0,0,0), radius=1.0, slices=12, stacks=12, color=(0,0,1)):
    cx, cy, cz = center
    polys = []
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        z0 = math.sin(lat0)
        zr0 = math.cos(lat0)
        lat1 = math.pi * (-0.5 + float(i+1) / stacks)
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)
        for j in range(slices):
            lng0 = 2*math.pi * float(j) / slices
            x0, y0 = math.cos(lng0), math.sin(lng0)
            lng1 = 2*math.pi * float(j+1) / slices
            x1, y1 = math.cos(lng1), math.sin(lng1)
            v1 = np.array([cx + radius*x0*zr0, cy + radius*y0*zr0, cz + radius*z0])
            v2 = np.array([cx + radius*x1*zr0, cy + radius*y1*zr0, cz + radius*z0])
            v3 = np.array([cx + radius*x1*zr1, cy + radius*y1*zr1, cz + radius*z1])
            v4 = np.array([cx + radius*x0*zr1, cy + radius*y0*zr1, cz + radius*z1])
            polys.append({"vertices":[v1,v2,v3], "color": color})
            polys.append({"vertices":[v1,v3,v4], "color": color})
    return polys


# Cria poligonos 3D e para mostar que o algoritmo não se comporta bem com interseções
def create_polygons_3D(): 
    # Criar lista de polígonos (triângulos + cubos + esferas)
    polygons = []
    polygons += create_cube(center=(-2,0,-3), size=1.0, color=(1,0,0))
    polygons += create_cube(center=(2,0,-5), size=1.5, color=(0,1,0))
    polygons += create_sphere(center=(0,1,-4), radius=1.0, slices=16, stacks=16, color=(0,0,1))
    polygons += create_sphere(center=(0,-1,-6), radius=0.7, slices=12, stacks=12, color=(1,1,0))
    return polygons

def create_polygons_3D_oclusion():
    polygons = []

    # 🔴 Cubo maior no fundo
    polygons += create_cube(center=(0, 0, -6), size=3.0, color=(1, 0, 0))

    # 🟢 Cubo médio parcialmente dentro do cubo maior
    polygons += create_cube(center=(0.5, 0.5, -5.5), size=2.0, color=(0, 1, 0))

    # 🔵 Esfera atravessando os dois cubos
    polygons += create_sphere(center=(-0.5, 0, -5.8), radius=1.5, slices=20, stacks=20, color=(0, 0, 1))

    # 🟡 Esfera menor parcialmente dentro da verde
    polygons += create_sphere(center=(1.0, -0.5, -5.2), radius=1.0, slices=16, stacks=16, color=(1, 1, 0))

    return polygons

# Cria polígonos 2D no espaço 3D (cena plana)
def create_polygons_2D():
    polygons = []
    # Corpo da casa (retângulo)
    house_body = [
        np.array([-1.0, -1.0, -3.0]),
        np.array([ 1.0, -1.0, -3.0]),
        np.array([ 1.0,  1.0, -3.0]),
        np.array([-1.0,  1.0, -3.0]),
    ]
    polygons.append({"vertices":[house_body[0], house_body[1], house_body[2]], "color": (1.0, 0.8, 0.6)})
    polygons.append({"vertices":[house_body[0], house_body[2], house_body[3]], "color": (1.0, 0.8, 0.6)})

    # Telhado (triângulo)
    roof = [
        np.array([-1.2, 1.0, -3.0]),
        np.array([ 1.2, 1.0, -3.0]),
        np.array([ 0.0, 2.0, -3.0]),
    ]
    polygons.append({"vertices": roof, "color": (0.7, 0.1, 0.1)})

    # Porta (pequeno retângulo)
    door = [
        np.array([-0.3, -1.0, -2.99]),
        np.array([ 0.3, -1.0, -2.99]),
        np.array([ 0.3,  0.0, -2.99]),
        np.array([-0.3,  0.0, -2.99]),
    ]
    polygons.append({"vertices":[door[0], door[1], door[2]], "color": (0.4, 0.2, 0.0)})
    polygons.append({"vertices":[door[0], door[2], door[3]], "color": (0.4, 0.2, 0.0)})

    # Sol (círculo aproximado com triângulos)
    sun_center = np.array([2.5, 2.5, -4.0])
    sun_radius = 0.6
    slices = 20
    for i in range(slices):
        theta1 = (i / slices) * 2 * math.pi
        theta2 = ((i+1) / slices) * 2 * math.pi
        v1 = sun_center
        v2 = np.array([sun_center[0] + sun_radius*math.cos(theta1),
                       sun_center[1] + sun_radius*math.sin(theta1),
                       sun_center[2]])
        v3 = np.array([sun_center[0] + sun_radius*math.cos(theta2),
                       sun_center[1] + sun_radius*math.sin(theta2),
                       sun_center[2]])
        polygons.append({"vertices":[v1,v2,v3], "color": (1.0, 1.0, 0.0)})

    return polygons

def create_polygons_2D_scene():
    polygons = []

    # Retângulos próximos da câmera (z mais próximo = sobrepõem os outros)
    rect1 = [(-0.8, -0.2, -1.0), (0.0, -0.2, -1.0), (0.0, 0.5, -1.0), (-0.8, 0.5, -1.0)]
    rect2 = [(0.2, -0.4, -1.2), (0.9, -0.4, -1.2), (0.9, 0.3, -1.2), (0.2, 0.3, -1.2)]

    # Retângulos intermediários
    rect3 = [(-0.5, -0.6, -2.0), (0.3, -0.6, -2.0), (0.3, 0.1, -2.0), (-0.5, 0.1, -2.0)]
    rect4 = [(-1.0, -0.8, -2.5), (-0.3, -0.8, -2.5), (-0.3, -0.2, -2.5), (-1.0, -0.2, -2.5)]

    # Retângulos mais distantes
    rect5 = [(0.5, -0.7, -3.0), (1.2, -0.7, -3.0), (1.2, -0.1, -3.0), (0.5, -0.1, -3.0)]
    rect6 = [(-1.2, 0.6, -3.5), (-0.4, 0.6, -3.5), (-0.4, 1.0, -3.5), (-1.2, 1.0, -3.5)]
    rect7 = [(-0.2, 0.8, -4.0), (0.6, 0.8, -4.0), (0.6, 1.2, -4.0), (-0.2, 1.2, -4.0)]

    rects = [
        (rect1, (1, 0, 0)),   # vermelho
        (rect2, (0, 1, 0)),   # verde
        (rect3, (0, 0, 1)),   # azul
        (rect4, (1, 1, 0)),   # amarelo
        (rect5, (1, 0, 1)),   # magenta
        (rect6, (0, 1, 1)),   # ciano
        (rect7, (0.7, 0.7, 0.7)) # cinza
    ]

    for rect, color in rects:
        v = [np.array(p) for p in rect]
        polygons.append({"vertices": [v[0], v[1], v[2]], "color": color})
        polygons.append({"vertices": [v[0], v[2], v[3]], "color": color})

    return polygons

def create_random_polygons(num=1000, spread=10.0, z_near=-1.0, z_far=-20.0):
    """
    Gera 'num' polígonos aleatórios no espaço 3D.
    
    Args:
        num (int): quantidade de polígonos
        spread (float): intervalo de variação em x e y
        z_near (float): profundidade mínima
        z_far (float): profundidade máxima
    """
    polygons = []
    for _ in range(num):
        # Centro do polígono
        cx = np.random.uniform(-spread, spread)
        cy = np.random.uniform(-spread, spread)
        cz = np.random.uniform(z_far, z_near)

        # Tamanho aleatório
        size = np.random.uniform(0.1, 1.0)

        # Cor aleatória
        color = (np.random.rand(), np.random.rand(), np.random.rand())

        # Criar um quadrilátero plano em torno do centro
        dx = size * np.random.uniform(0.5, 1.0)
        dy = size * np.random.uniform(0.5, 1.0)

        v1 = np.array([cx - dx, cy - dy, cz])
        v2 = np.array([cx + dx, cy - dy, cz])
        v3 = np.array([cx + dx, cy + dy, cz])
        v4 = np.array([cx - dx, cy + dy, cz])

        # Dividir em dois triângulos
        polygons.append({"vertices": [v1, v2, v3], "color": color})
        polygons.append({"vertices": [v1, v3, v4], "color": color})

    return polygons