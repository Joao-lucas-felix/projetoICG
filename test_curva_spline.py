# camera_around_polygons.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys
from painter_algorithm import render_scene_painter
from polygons import create_polygons_3D

# ------------------------------------------------------
# Variáveis globais
# ------------------------------------------------------
width, height = 800, 600
t_global = 0.0
camera_up = np.array([0.0, 1.0, 0.0])
polygons = []
control_points = []

# ------------------------------------------------------
# Funções de spline (Catmull-Rom)
# ------------------------------------------------------
def catmull_rom(p0, p1, p2, p3, t):
    t2, t3 = t*t, t*t*t
    return 0.5 * (
        (2*p1) +
        (-p0 + p2) * t +
        (2*p0 - 5*p1 + 4*p2 - p3) * t2 +
        (-p0 + 3*p1 - 3*p2 + p3) * t3
    )

def spline_curve(points, t):
    n = len(points) - 3
    if n <= 0:
        return points[0]
    segment = int(t) % n
    local_t = t - int(t)
    p0, p1, p2, p3 = points[segment:segment+4]
    return catmull_rom(p0, p1, p2, p3, local_t)

# ------------------------------------------------------
# Cena com polígonos + pontos de controle
# ------------------------------------------------------
def setup_scene():
    global polygons, control_points

    polygons = create_polygons_3D()

    # 🔵 pontos ao redor da cena (um circuito fechado)
    control_points = [
        np.array([ -4.0,  2.0, -8.0]),  # canto superior esquerdo
        np.array([  0.0,  3.0, -10.0]), # cima, olhando p/ baixo
        np.array([  4.0,  2.0, -8.0]),  # canto superior direito
        np.array([  5.0,  0.0, -5.0]),  # lado direito
        np.array([  4.0, -2.0, -3.0]),  # canto inferior direito
        np.array([  0.0, -3.0, -5.0]),  # frente embaixo
        np.array([ -4.0, -2.0, -3.0]),  # canto inferior esquerdo
        np.array([ -5.0,  0.0, -5.0])   # lado esquerdo
    ]

    # repete 2 pontos extras no início/fim p/ suavizar spline Catmull-Rom
    control_points = [control_points[-1]] + control_points + [control_points[0], control_points[1]]

# ------------------------------------------------------
# Callbacks GLUT
# ------------------------------------------------------
def display():
    global t_global, camera_up, polygons, control_points

    # posição da câmera na curva
    camera_pos = spline_curve(control_points, t_global)

    # alvo = centro aproximado da cena
    camera_target = np.array([0.0, 0.0, -5.5])

    render_scene_painter(polygons, camera_pos, camera_target, camera_up, 0.0)

def idle():
    global t_global
    t_global += 0.002  # velocidade da câmera
    glutPostRedisplay()

def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    if key == b'\x1b':  # ESC
        sys.exit(0)

# ------------------------------------------------------
# Main
# ------------------------------------------------------
def execTest():
    setup_scene()
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Camera Around Polygons")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glutMainLoop()

if __name__ == "__main__":
    execTest()
