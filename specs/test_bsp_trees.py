from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import math

# ==========================================================
# Estruturas de dados
# ==========================================================
class Polygon3D:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color

    def centroid(self):
        x = sum(v[0] for v in self.vertices) / len(self.vertices)
        y = sum(v[1] for v in self.vertices) / len(self.vertices)
        z = sum(v[2] for v in self.vertices) / len(self.vertices)
        return (x, y, z)

class BSPNode:
    def __init__(self, polygon):
        self.polygon = polygon
        self.front = None
        self.back = None

# ==========================================================
# Funções para BSP
# ==========================================================
def build_bsp(polygons):
    if not polygons:
        return None

    root_poly = polygons[0]
    node = BSPNode(root_poly)

    front_list = []
    back_list = []

    cx_root, cy_root, cz_root = root_poly.centroid()

    for poly in polygons[1:]:
        cx, cy, cz = poly.centroid()
        if cz > cz_root:
            front_list.append(poly)
        else:
            back_list.append(poly)

    node.front = build_bsp(front_list)
    node.back = build_bsp(back_list)

    return node

def traverse_bsp(node, eye_z, draw_callback):
    if node is None:
        return
    _, _, cz = node.polygon.centroid()
    if eye_z < cz:
        traverse_bsp(node.front, eye_z, draw_callback)
        draw_callback(node.polygon)
        traverse_bsp(node.back, eye_z, draw_callback)
    else:
        traverse_bsp(node.back, eye_z, draw_callback)
        draw_callback(node.polygon)
        traverse_bsp(node.front, eye_z, draw_callback)

# ==========================================================
# Objetos: cubos e esferas
# ==========================================================
def create_cube(center, size, color):
    cx, cy, cz = center
    s = size / 2.0
    vertices = [
        (cx-s, cy-s, cz-s), (cx+s, cy-s, cz-s),
        (cx+s, cy+s, cz-s), (cx-s, cy+s, cz-s),  # traseira
        (cx-s, cy-s, cz+s), (cx+s, cy-s, cz+s),
        (cx+s, cy+s, cz+s), (cx-s, cy+s, cz+s)   # dianteira
    ]
    faces = [
        [0,1,2,3], [4,5,6,7], [0,1,5,4],
        [2,3,7,6], [1,2,6,5], [0,3,7,4]
    ]
    return [Polygon3D([vertices[i] for i in face], color) for face in faces]

def create_sphere(center, radius, color, slices=12, stacks=12):
    cx, cy, cz = center
    polys = []
    for i in range(stacks):
        lat0 = math.pi * (-0.5 + float(i) / stacks)
        z0 = radius * math.sin(lat0)
        zr0 = radius * math.cos(lat0)

        lat1 = math.pi * (-0.5 + float(i+1) / stacks)
        z1 = radius * math.sin(lat1)
        zr1 = radius * math.cos(lat1)

        for j in range(slices):
            lng0 = 2 * math.pi * float(j) / slices
            lng1 = 2 * math.pi * float(j+1) / slices
            x0, y0 = math.cos(lng0), math.sin(lng0)
            x1, y1 = math.cos(lng1), math.sin(lng1)

            v1 = (cx + x0*zr0, cy + y0*zr0, cz + z0)
            v2 = (cx + x1*zr0, cy + y1*zr0, cz + z0)
            v3 = (cx + x1*zr1, cy + y1*zr1, cz + z1)
            v4 = (cx + x0*zr1, cy + y0*zr1, cz + z1)

            polys.append(Polygon3D([v1, v2, v3, v4], color))
    return polys

# ==========================================================
# OpenGL: desenhar polígono
# ==========================================================
def draw_polygon(polygon):
    glColor3f(*polygon.color)
    glBegin(GL_POLYGON)
    for x, y, z in polygon.vertices:
        glVertex3f(x, y, z)
    glEnd()

# ==========================================================
# Controle de câmera
# ==========================================================
camera_pos = [0.0, 0.0, 5.0]
camera_rot = 0.0  # rotação no plano XZ
move_speed = 0.2
rot_speed = 5.0  # graus

def keyboard(key, x, y):
    global camera_pos, camera_rot
    key = key.decode("utf-8").lower()

    if key == "w":  # frente
        camera_pos[0] += move_speed * math.sin(math.radians(camera_rot))
        camera_pos[2] -= move_speed * math.cos(math.radians(camera_rot))
    elif key == "s":  # trás
        camera_pos[0] -= move_speed * math.sin(math.radians(camera_rot))
        camera_pos[2] += move_speed * math.cos(math.radians(camera_rot))
    elif key == "a":  # esquerda
        camera_pos[0] -= move_speed * math.cos(math.radians(camera_rot))
        camera_pos[2] -= move_speed * math.sin(math.radians(camera_rot))
    elif key == "d":  # direita
        camera_pos[0] += move_speed * math.cos(math.radians(camera_rot))
        camera_pos[2] += move_speed * math.sin(math.radians(camera_rot))
    elif key == "q":  # subir
        camera_pos[1] += move_speed
    elif key == "e":  # descer
        camera_pos[1] -= move_speed
    elif key == "j":  # rotacionar esquerda
        camera_rot -= rot_speed
    elif key == "l":  # rotacionar direita
        camera_rot += rot_speed

    glutPostRedisplay()

# ==========================================================
# Renderização
# ==========================================================
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # direção para onde a câmera olha
    lx = math.sin(math.radians(camera_rot))
    lz = -math.cos(math.radians(camera_rot))

    gluLookAt(
        camera_pos[0], camera_pos[1], camera_pos[2],
        camera_pos[0] + lx, camera_pos[1], camera_pos[2] + lz,
        0, 1, 0
    )

    traverse_bsp(bsp_tree, eye_z=camera_pos[2], draw_callback=draw_polygon)

    glutSwapBuffers()

# ==========================================================
# Inicialização OpenGL
# ==========================================================
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

# ==========================================================
# Programa principal
# ==========================================================
if __name__ == "__main__":
    polygons = []
    polygons += create_cube(center=(-1.0, 0.0, 0.0), size=1.0, color=(1.0, 0.0, 0.0))  # vermelho
    polygons += create_cube(center=(1.5, 0.0, -1.0), size=1.0, color=(0.0, 1.0, 0.0)) # verde
    polygons += create_sphere(center=(0.0, 0.0, 1.0), radius=0.5, color=(0.0, 0.0, 1.0)) # azul

    bsp_tree = build_bsp(polygons)

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"BSP Tree 3D - Camera Movement")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMainLoop()
