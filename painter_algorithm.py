# painter_algorithm.py
from OpenGL.GL import *
import numpy as np

# ------------------------------------------------------
# Utilitários
# ------------------------------------------------------
def normalize(v):
    n = np.linalg.norm(v)
    return v / n if n else v

def look_at(eye, target, up):
    f = normalize(target - eye)
    s = normalize(np.cross(f, up))
    u = np.cross(s, f)
    M = np.identity(4, dtype=float)
    M[0, 0:3] = s
    M[1, 0:3] = u
    M[2, 0:3] = -f
    T = np.identity(4, dtype=float)
    T[0:3, 3] = -eye
    return M @ T

def transform_point(mat4, v3):
    v4 = np.array([v3[0], v3[1], v3[2], 1.0], dtype=float)
    tv = mat4 @ v4
    return tv[0:3] / (tv[3] if tv[3] != 0 else 1.0)

# ------------------------------------------------------
# Painter’s Algorithm
# ------------------------------------------------------
def polygon_avg_depth(poly, view_mat):
    verts = poly["vertices"]
    depths = [transform_point(view_mat, v)[2] for v in verts]
    return np.mean(depths)

def sort_polygons(polygons, view_mat):
    return sorted(polygons, key=lambda p: polygon_avg_depth(p, view_mat))

def draw_polygons(polygons):
    for p in polygons:
        color = p.get("color", (1,1,1))
        glColor3f(*color)
        glBegin(GL_POLYGON)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()
        # contorno
        glColor3f(0,0,0)
        glBegin(GL_LINE_LOOP)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()

def painter_algorithm(polygons, view_mat, angle=0.0):
    ordered = sort_polygons(polygons, view_mat)
    glDisable(GL_DEPTH_TEST)   # força uso do painter

    glPushMatrix()
    glRotatef(angle, 0, 1, 0)
    draw_polygons(ordered)
    glPopMatrix()

def render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle=0.0):
    from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
    from OpenGL.GLU import gluLookAt
    from OpenGL.GLUT import glutSwapBuffers

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(*(camera_pos.tolist() + camera_target.tolist() + camera_up.tolist()))
    view_mat = look_at(camera_pos, camera_target, camera_up)
    painter_algorithm(polygons, view_mat, angle)
    glutSwapBuffers()
