# test_2D_100k_polys.py
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
width, height = 800, 600  # Dimensões da janela
angle = 0.0  # Ângulo de rotação (atualmente desativado)

# Configuração da câmera:
camera_pos = np.array([0.0, 0.0, 5.0])      # Câmera posicionada em Z=5 (afastada)
camera_target = np.array([0.0, 0.0, 0.0])   # Mirando para a origem
camera_up = np.array([0.0, 1.0, 0.0])       # Vetor "cima" apontando para Y+

# 🔥 CARGA PESADA: Gera 100.000 polígonos aleatórios (teste de estresse extremo)
polygons = create_random_polygons(num=100000)

# ------------------------------------------------------
# Callbacks GLUT
# ------------------------------------------------------

def display():
    """
    Callback de renderização - chamado a cada frame para desenhar a cena.
    Esta função será MUITO LENTA devido aos 100k polígonos.
    """
    global polygons, camera_pos, camera_target, camera_up, angle
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle)

def idle():
    """
    Callback de ociosidade - chamado quando o sistema não está processando outros eventos.
    Pode causar lentidão extrema se a animação estiver habilitada.
    """
    global angle
    # Ângulo comentado para evitar animação (seria muito lento com 100k polígonos)
    #angle += 0.2
    
    # Mantém o ângulo no range [0, 360)
    if angle >= 360: 
        angle -= 360
        
    # Força redesenho - CUIDADO: isso pode travar o sistema com 100k polígonos
    glutPostRedisplay()

def reshape(w, h):
    """
    Callback de redimensionamento - ajusta a viewport e projeção quando a janela muda de tamanho.
    """
    global width, height
    width, height = w, h
    
    # Define a área de renderização
    glViewport(0, 0, w, h)
    
    # Configura a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    # Projeção perspectiva:
    # - 60° campo de visão vertical
    # - Aspect ratio baseado na janela
    # - Plano próximo: 0.1, Plano distante: 100.0
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)
    
    # Volta para matriz de modelview
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    """
    Callback de teclado - processa entrada do usuário.
    """
    global camera_pos
    
    if key == b'\x1b':  # Tecla ESC - sai do programa
        sys.exit(0)
    
    # Controles simples de câmera:
    if key == b'w':  # W - move câmera para frente (zoom in)
        camera_pos[2] -= 0.2
        
    if key == b's':  # S - move câmera para trás (zoom out)
        camera_pos[2] += 0.2
        
    # Solicita redesenho (pode ser muito lento)
    glutPostRedisplay()

# ------------------------------------------------------
# Main
# ------------------------------------------------------

def execTest():
    """
    Função principal que inicializa e executa a aplicação OpenGL.
    AVISO: Este teste é extremamente pesado e pode travar sistemas menos potentes.
    """
    # Inicializa GLUT
    glutInit(sys.argv)
    
    # Configura modo de display:
    # - Double buffering (evita flickering)
    # - Modo RGBA
    # - Buffer de profundidade
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    
    # Define tamanho inicial da janela
    glutInitWindowSize(width, height)
    
    # Cria janela com título
    glutCreateWindow(b"Painter's Algorithm Modular Demo")
    
    # Registra callbacks:
    glutDisplayFunc(display)      # Renderização
    glutIdleFunc(idle)            # Tempo ocioso
    glutReshapeFunc(reshape)      # Redimensionamento
    glutKeyboardFunc(keyboard)    # Teclado
    
    # Define cor de fundo (cinza claro)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    
    # ⚠️ AVISO CRÍTICO: Loop principal pode ser extremamente lento
    glutMainLoop()

if __name__ == "__main__":
    # ⚠️ EXECUÇÃO PERIGOSA: Pode travar o sistema ou ser muito lenta
    execTest()