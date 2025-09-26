# test_curva_spline.py
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
width, height = 800, 600  # Dimensões da janela
t_global = 0.0  # Parâmetro de animação para a curva spline
camera_up = np.array([0.0, 1.0, 0.0])  # Vetor "para cima" fixo
polygons = []  # Lista de polígonos da cena
control_points = []  # Pontos de controle da curva spline

# ------------------------------------------------------
# Funções de spline (Catmull-Rom)
# ------------------------------------------------------

def catmull_rom(p0, p1, p2, p3, t):
    """
    Calcula um ponto na curva Catmull-Rom.
    Catmull-Rom é uma spline que passa por todos os pontos de controle (p1 e p2).
    
    Args:
        p0, p1, p2, p3: 4 pontos de controle consecutivos
        t: parâmetro entre 0 e 1 para interpolar entre p1 e p2
    
    Returns:
        Ponto interpolado na curva
    """
    t2, t3 = t*t, t*t*t  # t² e t³ para cálculo polinomial
    
    # Fórmula da spline Catmull-Rom:
    return 0.5 * (
        (2*p1) +  # Termo constante
        (-p0 + p2) * t +  # Termo linear
        (2*p0 - 5*p1 + 4*p2 - p3) * t2 +  # Termo quadrático
        (-p0 + 3*p1 - 3*p2 + p3) * t3  # Termo cúbico
    )

def spline_curve(points, t):
    """
    Calcula um ponto em uma curva spline fechada baseada em Catmull-Rom.
    
    Args:
        points: lista de pontos de controle (deve ter pelo menos 4 pontos)
        t: parâmetro que percorre a curva (pode ser maior que 1 para loops)
    
    Returns:
        Ponto na curva correspondente ao parâmetro t
    """
    n = len(points) - 3  # Número de segmentos da curva
    if n <= 0:
        return points[0]  # Caso degenerado
    
    # Determina qual segmento da curva usar baseado em t
    segment = int(t) % n  # Segmento atual (cíclico)
    local_t = t - int(t)  # Parâmetro local dentro do segmento [0, 1)
    
    # Pega 4 pontos de controle consecutivos para este segmento
    p0, p1, p2, p3 = points[segment:segment+4]
    
    # Calcula ponto na curva usando Catmull-Rom
    return catmull_rom(p0, p1, p2, p3, local_t)

# ------------------------------------------------------
# Cena com polígonos + pontos de controle
# ------------------------------------------------------

def setup_scene():
    """
    Configura a cena 3D e os pontos de controle para a animação da câmera.
    Cria um circuito fechado ao redor dos objetos.
    """
    global polygons, control_points

    # Cria a cena 3D básica com cubos e esferas
    polygons = create_polygons_3D()

    # 🔵 Pontos de controle formando um circuito fechado ao redor da cena
    control_points = [
        np.array([ -4.0,  2.0, -8.0]),  # canto superior esquerdo (traseiro)
        np.array([  0.0,  3.0, -10.0]), # topo central (mais distante)
        np.array([  4.0,  2.0, -8.0]),  # canto superior direito (traseiro)
        np.array([  5.0,  0.0, -5.0]),  # lado direito (intermediário)
        np.array([  4.0, -2.0, -3.0]),  # canto inferior direito (frontal)
        np.array([  0.0, -3.0, -5.0]),  # frente inferior
        np.array([ -4.0, -2.0, -3.0]),  # canto inferior esquerdo (frontal)
        np.array([ -5.0,  0.0, -5.0])   # lado esquerdo (intermediário)
    ]

    # 🔁 Técnica: repete pontos no início/fim para suavizar a spline Catmull-Rom
    # Isso cria uma curva fechada contínua sem quebras
    control_points = [control_points[-1]] + control_points + [control_points[0], control_points[1]]

# ------------------------------------------------------
# Callbacks GLUT
# ------------------------------------------------------

def display():
    """
    Callback de renderização - calcula a posição da câmera na spline e renderiza a cena.
    """
    global t_global, camera_up, polygons, control_points

    # 🎯 Calcula a posição da câmera na curva spline
    camera_pos = spline_curve(control_points, t_global)

    # 🎯 Define o alvo da câmera (centro aproximado da cena)
    camera_target = np.array([0.0, 0.0, -5.5])

    # 🎨 Renderiza a cena usando o Painter's Algorithm
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, 0.0)

def idle():
    """
    Callback de ociosidade - anima o parâmetro da curva para mover a câmera.
    """
    global t_global
    t_global += 0.002  # Velocidade da animação (ajuste para mais rápido/lento)
    glutPostRedisplay()  # Solicita redesenho

def reshape(w, h):
    """
    Callback de redimensionamento - ajusta viewport e projeção.
    """
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    """
    Callback de teclado - apenas permite sair com ESC.
    """
    if key == b'\x1b':  # Tecla ESC - sai do programa
        sys.exit(0)

# ------------------------------------------------------
# Main
# ------------------------------------------------------

def execTest():
    """
    Função principal que configura e executa a demonstração.
    """
    # Configura a cena e pontos de controle
    setup_scene()
    
    # Inicialização padrão do GLUT
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Camera Around Polygons")
    
    # Registra callbacks
    glutDisplayFunc(display)
    glutIdleFunc(idle)  # 🔄 Importante: habilita animação automática
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    
    glClearColor(0.9, 0.9, 0.9, 1.0)  # Cor de fundo cinza
    glutMainLoop()

if __name__ == "__main__":
    execTest()