# test_2D.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys
from painter_algorithm import render_scene_painter
from polygons import create_polygons_2D_scene

# ------------------------------------------------------
# Variáveis globais
# ------------------------------------------------------
width, height = 800, 600  # Dimensões iniciais da janela
angle = 0.0  # Ângulo de rotação da cena (inicialmente 0)

# Configuração da câmera:
camera_pos = np.array([0.0, 0.0, 5.0])      # Posição da câmera (5 unidades afastada na direção Z)
camera_target = np.array([0.0, 0.0, 0.0])   # Ponto para onde a câmera está olhando (origem)
camera_up = np.array([0.0, 1.0, 0.0])       # Vetor que define a direção "para cima" (eixo Y)

# Cria uma cena 2D com múltiplos retângulos em diferentes profundidades
# Esta cena é ideal para testar o Painter's Algorithm com objetos 2D
polygons = create_polygons_2D_scene()

# ------------------------------------------------------
# Callbacks GLUT (Funções de callback do sistema OpenGL)
# ------------------------------------------------------

def display():
    """
    Função callback chamada quando a janela precisa ser redesenhada.
    É o coração da renderização - executa o Painter's Algorithm.
    """
    global polygons, camera_pos, camera_target, camera_up, angle
    # Renderiza a cena usando o algoritmo do pintor
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle)

def idle():
    """
    Função callback chamada quando o sistema está ocioso.
    Pode ser usada para animações contínuas.
    """
    global angle
    # A rotação automática está comentada - descomente para habilitar animação
    #angle += 0.2
    
    # Mantém o ângulo no intervalo [0, 360) graus
    if angle >= 360: 
        angle -= 360
        
    # Solicita que a janela seja redesenhada na próxima oportunidade
    glutPostRedisplay()

def reshape(w, h):
    """
    Função callback chamada quando a janela é redimensionada.
    Ajusta a viewport e a matriz de projeção para a nova dimensão.
    """
    global width, height
    width, height = w, h  # Atualiza as dimensões globais
    
    # Define a área de desenho (viewport) para cobrir toda a janela
    glViewport(0, 0, w, h)
    
    # Seleciona a matriz de projeção para configuração
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reseta a matriz de projeção
    
    # Configura uma projeção perspectiva:
    # - 60.0: campo de visão vertical em graus
    # - float(w)/float(h): aspect ratio (proporção largura/altura)
    # - 0.1: plano de corte próximo
    # - 100.0: plano de corte distante
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)
    
    # Volta para a matriz de modelview (para transformações de objetos)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    """
    Função callback chamada quando uma tecla é pressionada.
    Implementa controles interativos da câmera.
    """
    global camera_pos
    
    if key == b'\x1b':  # Tecla ESC (código ASCII 27) - sai do programa
        sys.exit(0)
    
    # Controles de movimento da câmera:
    if key == b'w':  # Tecla W - move a câmera para frente (zoom in)
        camera_pos[2] -= 0.2  # Diminui Z (no OpenGL, Z negativo significa "para frente")
        
    if key == b's':  # Tecla S - move a câmera para trás (zoom out)
        camera_pos[2] += 0.2  # Aumenta Z (move para trás)
    
    # Solicita um redesenho da cena para refletir as mudanças
    glutPostRedisplay()

# ------------------------------------------------------
# Main - Função principal do programa
# ------------------------------------------------------

def execTest():
    """
    Função principal que configura e inicia a aplicação OpenGL.
    Configura a janela, registra callbacks e inicia o loop principal.
    """
    # Inicializa o sistema GLUT
    glutInit(sys.argv)
    
    # Configura o modo de display da janela:
    # GLUT_DOUBLE: double buffering (evita flickering)
    # GLUT_RGBA: modo de cores RGBA
    # GLUT_DEPTH: habilita buffer de profundidade (Z-buffer)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    
    # Define o tamanho inicial da janela
    glutInitWindowSize(width, height)
    
    # Cria a janela com o título especificado
    glutCreateWindow(b"Painter's Algorithm Modular Demo")
    
    # Registra as funções callback:
    glutDisplayFunc(display)    # Chamada quando precisa renderizar
    glutIdleFunc(idle)          # Chamada quando o sistema está ocioso
    glutReshapeFunc(reshape)    # Chamada quando a janela é redimensionada
    glutKeyboardFunc(keyboard)  # Chamada quando uma tecla é pressionada
    
    # Define a cor de fundo (cinza claro)
    glClearColor(0.9, 0.9, 0.9, 1.0)
    
    # Inicia o loop principal do GLUT (esta função é bloqueante)
    glutMainLoop()

if __name__ == "__main__":
    # Ponto de entrada do programa - executa o teste quando o arquivo é rodado diretamente
    execTest()