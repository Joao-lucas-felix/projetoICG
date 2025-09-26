# polygons.py
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
    """
    Cria um cubo 3D composto por triângulos
    center: centro do cubo (x, y, z)
    size: tamanho do cubo
    color: cor RGB do cubo
    Retorna lista de polígonos triangulares
    """
    cx, cy, cz = center
    s = size / 2.0  # Metade do tamanho (raio)
    
    # 8 vértices do cubo
    vertices = [
        (cx-s, cy-s, cz-s), (cx+s, cy-s, cz-s), (cx+s, cy+s, cz-s), (cx-s, cy+s, cz-s),  # Face traseira
        (cx-s, cy-s, cz+s), (cx+s, cy-s, cz+s), (cx+s, cy+s, cz+s), (cx-s, cy+s, cz+s),  # Face frontal
    ]
    
    # 6 faces do cubo (cada face tem 4 vértices)
    faces = [
        (0,1,2,3),  # Face traseira
        (4,5,6,7),  # Face frontal
        (0,1,5,4),  # Face inferior
        (2,3,7,6),  # Face superior
        (1,2,6,5),  # Face direita
        (0,3,7,4),  # Face esquerda
    ]
    
    polys = []
    for f in faces:
        # Converte índices em vértices reais
        v = [np.array(vertices[i]) for i in f]
        # Divide cada face quadrada em 2 triângulos
        polys.append({"vertices":[v[0], v[1], v[2]], "color": color})
        polys.append({"vertices":[v[0], v[2], v[3]], "color": color})
    return polys

def create_sphere(center=(0,0,0), radius=1.0, slices=12, stacks=12, color=(0,0,1)):
    """
    Cria uma esfera usando aproximação por triângulos (UV sphere)
    center: centro da esfera
    radius: raio da esfera
    slices: número de divisões longitudinais (meridianos)
    stacks: número de divisões latitudinais (paralelos)
    """
    cx, cy, cz = center
    polys = []
    
    # Itera pelas fatias verticais (stacks)
    for i in range(stacks):
        # Calcula latitudes (ângulos verticais)
        lat0 = math.pi * (-0.5 + float(i) / stacks)    # Latitude inferior
        z0 = math.sin(lat0)    # Altura nesta latitude
        zr0 = math.cos(lat0)   # Raio horizontal nesta latitude
        
        lat1 = math.pi * (-0.5 + float(i+1) / stacks)  # Latitude superior
        z1 = math.sin(lat1)
        zr1 = math.cos(lat1)
        
        # Itera pelas fatias horizontais (slices)
        for j in range(slices):
            # Calcula longitudes (ângulos horizontais)
            lng0 = 2*math.pi * float(j) / slices      # Longitude esquerda
            x0, y0 = math.cos(lng0), math.sin(lng0)   # Coordenadas no círculo
            
            lng1 = 2*math.pi * float(j+1) / slices    # Longitude direita
            x1, y1 = math.cos(lng1), math.sin(lng1)
            
            # Calcula os 4 vértices do quadrilátero esférico
            v1 = np.array([cx + radius*x0*zr0, cy + radius*y0*zr0, cz + radius*z0])
            v2 = np.array([cx + radius*x1*zr0, cy + radius*y1*zr0, cz + radius*z0])
            v3 = np.array([cx + radius*x1*zr1, cy + radius*y1*zr1, cz + radius*z1])
            v4 = np.array([cx + radius*x0*zr1, cy + radius*y0*zr1, cz + radius*z1])
            
            # Divide o quadrilátero em 2 triângulos
            polys.append({"vertices":[v1,v2,v3], "color": color})
            polys.append({"vertices":[v1,v3,v4], "color": color})
    return polys

# Cria polígonos 3D e para mostrar que o algoritmo não se comporta bem com interseções
def create_polygons_3D(): 
    """
    Cria uma cena 3D simples com cubos e esferas para testar o Painter's Algorithm
    Mostra os limites do algoritmo com objetos 3D que se intersectam
    """
    polygons = []
    # Adiciona objetos em diferentes posições e tamanhos
    polygons += create_cube(center=(-2,0,-3), size=1.0, color=(1,0,0))    # Cubo vermelho
    polygons += create_cube(center=(2,0,-5), size=1.5, color=(0,1,0))     # Cubo verde
    polygons += create_sphere(center=(0,1,-4), radius=1.0, color=(0,0,1)) # Esfera azul
    polygons += create_sphere(center=(0,-1,-6), radius=0.7, color=(1,1,0))# Esfera amarela
    return polygons

def create_polygons_3D_oclusion():
    """
    Cria uma cena 3D com objetos intencionalmente sobrepostos
    para demonstrar as limitações do Painter's Algorithm com oclusão complexa
    """
    polygons = []

    # 🔴 Cubo maior no fundo (vermelho)
    polygons += create_cube(center=(0, 0, -6), size=3.0, color=(1, 0, 0))

    # 🟢 Cubo médio parcialmente dentro do cubo maior (verde)
    polygons += create_cube(center=(0.5, 0.5, -5.5), size=2.0, color=(0, 1, 0))

    # 🔵 Esfera atravessando os dois cubos (azul)
    polygons += create_sphere(center=(-0.5, 0, -5.8), radius=1.5, color=(0, 0, 1))

    # 🟡 Esfera menor parcialmente dentro da verde (amarela)
    polygons += create_sphere(center=(1.0, -0.5, -5.2), radius=1.0, color=(1, 1, 0))

    return polygons

# Cria polígonos 2D no espaço 3D (cena plana)
def create_polygons_2D():
    """
    Cria uma cena 2D simples (casa com sol) para demonstrar 
    que o Painter's Algorithm funciona bem com objetos 2D
    """
    polygons = []
    
    # Corpo da casa (retângulo bege)
    house_body = [
        np.array([-1.0, -1.0, -3.0]),  # inferior esquerdo
        np.array([ 1.0, -1.0, -3.0]),  # inferior direito
        np.array([ 1.0,  1.0, -3.0]),  # superior direito
        np.array([-1.0,  1.0, -3.0]),  # superior esquerdo
    ]
    # Divide o retângulo em 2 triângulos
    polygons.append({"vertices":[house_body[0], house_body[1], house_body[2]], "color": (1.0, 0.8, 0.6)})
    polygons.append({"vertices":[house_body[0], house_body[2], house_body[3]], "color": (1.0, 0.8, 0.6)})

    # Telhado (triângulo vermelho)
    roof = [
        np.array([-1.2, 1.0, -3.0]),  # esquerda
        np.array([ 1.2, 1.0, -3.0]),  # direita
        np.array([ 0.0, 2.0, -3.0]),  # topo
    ]
    polygons.append({"vertices": roof, "color": (0.7, 0.1, 0.1)})

    # Porta (pequeno retângulo marrom) - ligeiramente à frente da casa (z = -2.99)
    door = [
        np.array([-0.3, -1.0, -2.99]),
        np.array([ 0.3, -1.0, -2.99]),
        np.array([ 0.3,  0.0, -2.99]),
        np.array([-0.3,  0.0, -2.99]),
    ]
    polygons.append({"vertices":[door[0], door[1], door[2]], "color": (0.4, 0.2, 0.0)})
    polygons.append({"vertices":[door[0], door[2], door[3]], "color": (0.4, 0.2, 0.0)})

    # Sol (círculo amarelo aproximado com triângulos)
    sun_center = np.array([2.5, 2.5, -4.0])
    sun_radius = 0.6
    slices = 20
    for i in range(slices):
        # Calcula ângulos para cada fatia do círculo
        theta1 = (i / slices) * 2 * math.pi
        theta2 = ((i+1) / slices) * 2 * math.pi
        
        # Vértices do triângulo da fatia
        v1 = sun_center  # Centro
        v2 = np.array([sun_center[0] + sun_radius*math.cos(theta1),
                       sun_center[1] + sun_radius*math.sin(theta1),
                       sun_center[2]])  # Ponto na circunferência 1
        v3 = np.array([sun_center[0] + sun_radius*math.cos(theta2),
                       sun_center[1] + sun_radius*math.sin(theta2),
                       sun_center[2]])  # Ponto na circunferência 2
        
        polygons.append({"vertices":[v1,v2,v3], "color": (1.0, 1.0, 0.0)})

    return polygons

def create_polygons_2D_scene():
    """
    Cria múltiplos retângulos 2D em diferentes profundidades
    para testar a ordenação por profundidade do Painter's Algorithm
    """
    polygons = []

    # Define retângulos em diferentes profundidades (coordenada Z)
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

    # Lista de retângulos com suas cores
    rects = [
        (rect1, (1, 0, 0)),   # vermelho (mais próximo)
        (rect2, (0, 1, 0)),   # verde
        (rect3, (0, 0, 1)),   # azul
        (rect4, (1, 1, 0)),   # amarelo
        (rect5, (1, 0, 1)),   # magenta
        (rect6, (0, 1, 1)),   # ciano
        (rect7, (0.7, 0.7, 0.7)) # cinza (mais distante)
    ]

    # Converte cada retângulo em 2 triângulos
    for rect, color in rects:
        v = [np.array(p) for p in rect]  # Converte para arrays numpy
        polygons.append({"vertices": [v[0], v[1], v[2]], "color": color})
        polygons.append({"vertices": [v[0], v[2], v[3]], "color": color})

    return polygons

def create_random_polygons(num=1000, spread=10.0, z_near=-1.0, z_far=-20.0):
    """
    Gera 'num' polígonos aleatórios no espaço 3D para teste de performance
    e estresse do Painter's Algorithm.
    
    Args:
        num (int): quantidade de polígonos
        spread (float): intervalo de variação em x e y
        z_near (float): profundidade mínima (mais próxima)
        z_far (float): profundidade máxima (mais distante)
    """
    polygons = []
    for _ in range(num):
        # Centro aleatório do polígono
        cx = np.random.uniform(-spread, spread)
        cy = np.random.uniform(-spread, spread)
        cz = np.random.uniform(z_far, z_near)  # z_far < z_near (coordenadas negativas)

        # Tamanho aleatório
        size = np.random.uniform(0.1, 1.0)

        # Cor aleatória
        color = (np.random.rand(), np.random.rand(), np.random.rand())

        # Criar um quadrilátero plano em torno do centro
        dx = size * np.random.uniform(0.5, 1.0)  # Largura
        dy = size * np.random.uniform(0.5, 1.0)  # Altura

        # 4 vértices do quadrilátero
        v1 = np.array([cx - dx, cy - dy, cz])
        v2 = np.array([cx + dx, cy - dy, cz])
        v3 = np.array([cx + dx, cy + dy, cz])
        v4 = np.array([cx - dx, cy + dy, cz])

        # Divide em dois triângulos
        polygons.append({"vertices": [v1, v2, v3], "color": color})
        polygons.append({"vertices": [v1, v3, v4], "color": color})

    return polygons

def create_random_3d_shapes(num_shapes=10, spread=15.0, z_near=-5.0, z_far=-30.0):
    """
    Gera 'num_shapes' figuras 3D aleatórias (cubos, esferas e pirâmides)
    para testar o Painter's Algorithm com geometria 3D complexa.
    
    Args:
        num_shapes (int): quantidade de figuras 3D
        spread (float): intervalo de variação em x e y
        z_near (float): profundidade mínima
        z_far (float): profundidade máxima
    """
    polygons = []
    
    for _ in range(num_shapes):
        # Posição aleatória
        x = np.random.uniform(-spread, spread)
        y = np.random.uniform(-spread/2, spread/2)  # Menor variação em y para realismo
        z = np.random.uniform(z_far, z_near)
        
        # Cor aleatória
        color = (np.random.rand(), np.random.rand(), np.random.rand())
        
        # Escolhe aleatoriamente o tipo de figura
        shape_type = np.random.choice(['cube', 'sphere', 'pyramid', 'cylinder'], 
                                     p=[0.4, 0.3, 0.2, 0.1])  # Probabilidades
        
        if shape_type == 'cube':
            size = np.random.uniform(0.3, 2.0)
            polygons += create_cube(center=(x, y, z), size=size, color=color)
            
        elif shape_type == 'sphere':
            radius = np.random.uniform(0.2, 1.5)
            slices = np.random.randint(8, 16)   # Resolução variável
            stacks = np.random.randint(8, 16)
            polygons += create_sphere(center=(x, y, z), radius=radius, 
                                    slices=slices, stacks=stacks, color=color)
            
        elif shape_type == 'pyramid':
            base_size = np.random.uniform(0.4, 1.5)
            height = np.random.uniform(0.5, 2.0)
            pyramid_polys = create_pyramid(center=(x, y, z), base_size=base_size, 
                                         height=height, color=color)
            polygons += pyramid_polys
            
        elif shape_type == 'cylinder':
            radius = np.random.uniform(0.3, 1.0)
            height = np.random.uniform(0.5, 2.0)
            cylinder_polys = create_cylinder(center=(x, y, z), radius=radius, 
                                           height=height, slices=12, color=color)
            polygons += cylinder_polys
    
    return polygons

def create_pyramid(center=(0,0,0), base_size=1.0, height=1.0, color=(1,0,0)):
    """Cria uma pirâmide (tetraedro) com base quadrada."""
    cx, cy, cz = center
    s = base_size / 2.0
    
    # Base da pirâmide (quadrado no plano Y fixo)
    base_vertices = [
        np.array([cx-s, cy, cz-s]),  # vértice traseiro esquerdo
        np.array([cx+s, cy, cz-s]),  # vértice traseiro direito
        np.array([cx+s, cy, cz+s]),  # vértice frontal direito
        np.array([cx-s, cy, cz+s])   # vértice frontal esquerdo
    ]
    
    # Topo da pirâmide (acima do centro)
    apex = np.array([cx, cy+height, cz])
    
    polygons = []
    
    # Base (dois triângulos)
    polygons.append({"vertices": [base_vertices[0], base_vertices[1], base_vertices[2]], "color": color})
    polygons.append({"vertices": [base_vertices[0], base_vertices[2], base_vertices[3]], "color": color})
    
    # Faces laterais (triângulos conectando base ao ápice)
    polygons.append({"vertices": [base_vertices[0], base_vertices[1], apex], "color": color})  # Face traseira
    polygons.append({"vertices": [base_vertices[1], base_vertices[2], apex], "color": color})  # Face direita
    polygons.append({"vertices": [base_vertices[2], base_vertices[3], apex], "color": color})  # Face frontal
    polygons.append({"vertices": [base_vertices[3], base_vertices[0], apex], "color": color})  # Face esquerda
    
    return polygons

def create_cylinder(center=(0,0,0), radius=1.0, height=1.0, slices=12, color=(0,1,0)):
    """Cria um cilindro composto por triângulos."""
    cx, cy, cz = center
    half_height = height / 2.0
    
    polygons = []
    bottom_vertices = []  # Vértices da base inferior
    top_vertices = []     # Vértices da base superior
    
    # Gera vértices para as laterais
    for i in range(slices):
        angle = 2 * math.pi * i / slices
        next_angle = 2 * math.pi * (i + 1) / slices
        
        # Calcula vértices na circunferência
        x1 = radius * math.cos(angle)
        z1 = radius * math.sin(angle)
        x2 = radius * math.cos(next_angle)
        z2 = radius * math.sin(next_angle)
        
        # Vértices da base inferior e superior
        bottom_v1 = np.array([cx + x1, cy - half_height, cz + z1])
        bottom_v2 = np.array([cx + x2, cy - half_height, cz + z2])
        top_v1 = np.array([cx + x1, cy + half_height, cz + z1])
        top_v2 = np.array([cx + x2, cy + half_height, cz + z2])
        
        bottom_vertices.append(bottom_v1)
        top_vertices.append(top_v1)
        
        # Face lateral (dois triângulos por segmento)
        polygons.append({"vertices": [bottom_v1, bottom_v2, top_v2], "color": color})
        polygons.append({"vertices": [bottom_v1, top_v2, top_v1], "color": color})
    
    # Centros das tampas
    bottom_center = np.array([cx, cy - half_height, cz])
    top_center = np.array([cx, cy + half_height, cz])
    
    # Cria as tampas (base inferior e superior)
    for i in range(slices):
        next_i = (i + 1) % slices  # Índice do próximo vértice (cíclico)
        
        # Tampa inferior
        polygons.append({"vertices": [bottom_center, bottom_vertices[i], bottom_vertices[next_i]], "color": color})
        
        # Tampa superior (ordem inversa para normal apontar para fora)
        polygons.append({"vertices": [top_center, top_vertices[next_i], top_vertices[i]], "color": color})
    
    return polygons