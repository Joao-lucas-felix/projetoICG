# test_2D_1k_polys.py
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
angle = 0.0  # Ângulo de rotação para animação

# Parâmetros da câmera:
camera_pos = np.array([0.0, 0.0, 5.0])      # Posição da câmera (afastada 5 unidades)
camera_target = np.array([0.0, 0.0, 0.0])   # Ponto para onde a câmera olha (origem)
camera_up = np.array([0.0, 1.0, 0.0])       # Vetor "para cima" da câmera

# Gera 1000 polígonos aleatórios para teste de performance
polygons = create_random_polygons()

# ------------------------------------------------------
# Callbacks GLUT (funções de callback do OpenGL)
# ------------------------------------------------------

def display():
    """
    Função callback chamada quando a janela precisa ser redesenhada.
    É o coração da renderização - chamada a cada frame.
    """
    global polygons, camera_pos, camera_target, camera_up, angle
    # Renderiza a cena usando o Painter's Algorithm
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle)

def idle():
    """
    Função callback chamada quando o sistema está ocioso.
    Usada para animações e atualizações contínuas.
    """
    global angle
    # Descomentar a linha abaixo para habilitar rotação automática:
    # angle += 0.2  # Incrementa o ângulo de rotação
    
    # Mantém o ângulo no intervalo [0, 360)
    if angle >= 360: 
        angle -= 360
        
    # Solicita redesenho da janela
    glutPostRedisplay()

def reshape(w, h):
    """
    Função callback chamada quando a janela é redimensionada.
    Ajusta a viewport e a projeção perspectiva.
    """
    global width, height
    width, height = w, h  # Atualiza dimensões globais
    
    # Define a área de desenho (viewport) para cobrir toda a janela
    glViewport(0, 0, w, h)
    
    # Configura a matriz de projeção
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reseta a matriz
    
    # Define projeção perspectiva:
    # 60.0 - campo de visão vertical em graus
    # float(w)/float(h) - aspect ratio (proporção da janela)
    # 0.1 - plano de corte próximo
    # 100.0 - plano de corte distante
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)
    
    # Volta para a matriz de modelview (transformações de objetos)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    """
    Função callback chamada quando uma tecla é pressionada.
    key: tecla pressionada (em bytes)
    x, y: coordenadas do mouse quando a tecla foi pressionada
    """
    global camera_pos
    
    if key == b'\x1b':  # Tecla ESC (código ASCII 27)
        sys.exit(0)     # Sai do programa
    
    # Controles de câmera simples:
    if key == b'w':     # Tecla W - move câmera para frente
        camera_pos[2] -= 0.2  # Diminui Z (OpenGL: negativo = frente)
    
    if key == b's':     # Tecla S - move câmera para trás
        camera_pos[2] += 0.2  # Aumenta Z (OpenGL: positivo = trás)
    
    # Solicita redesenho para atualizar a cena
    glutPostRedisplay()

# ------------------------------------------------------
# Main - Ponto de entrada do programa
# ------------------------------------------------------
def execTest():
    """
    Função principal que inicializa e executa a aplicação OpenGL.
    Configura a janela, callbacks e inicia o loop principal.
    """
    # Inicializa o GLUT
    glutInit(sys.argv)
    
    # Configura o modo de display:
    # GLUT_DOUBLE - double buffering (evita flickering)
    # GLUT_RGBA - modo de cor RGBA
    # GLUT_DEPTH - buffer de profundidade
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    
    # Define tamanho inicial da janela
    glutInitWindowSize(width, height)
    
    # Cria a janela com título
    glutCreateWindow(b"Painter's Algorithm Modular Demo")
    
    # Registra funções callback:
    glutDisplayFunc(display)    # Chamada quando precisa redesenhar
    glutIdleFunc(idle)          # Chamada quando ocioso
    glutReshapeFunc(reshape)    # Chamada quando janela é redimensionada
    glutKeyboardFunc(keyboard)  # Chamada quando tecla é pressionada
    
    # Define cor de fundo (cinza claro)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    
    # Inicia o loop principal do GLUT (bloqueante)
    glutMainLoop()

if __name__ == "__main__":
    # Executa o teste quando o script é rodado diretamente
    execTest()