# painter_modular.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys
from painter_algorithm import render_scene_painter
from polygons import create_random_polygons

# ------------------------------------------------------
# Variáveis globais
# ------------------------------------------------------
width, height = 800, 600
angle = 0.0
camera_pos = np.array([0.0, 0.0, 5.0])
camera_target = np.array([0.0, 0.0, 0.0])
camera_up = np.array([0.0, 1.0, 0.0])
polygons = create_random_polygons()

# ------------------------------------------------------
# Callbacks GLUT
# ------------------------------------------------------
def display():
    global polygons, camera_pos, camera_target, camera_up, angle
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle)

def idle():
    global angle
    #angle += 0.2
    if angle >= 360: 
        angle -= 360
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
    global camera_pos
    if key == b'\x1b':  # ESC
        sys.exit(0)
    if key == b'w':
        camera_pos[2] -= 0.2
    if key == b's':
        camera_pos[2] += 0.2
    glutPostRedisplay()

# ------------------------------------------------------
# Main
# ------------------------------------------------------
def execTest():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Painter's Algorithm Modular Demo")
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glutMainLoop()

if __name__ == "__main__":
    execTest()
