# painter_modular.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import sys
from painter_algorithm import render_scene_painter
from polygons import create_polygons_3D

# ------------------------------------------------------
# Variáveis globais
# ------------------------------------------------------
width, height = 800, 600
angle = 0.0  # Ângulo de rotação para animação
camera_pos = np.array([0.0, 0.0, 5.0])      # Posição inicial da câmera
camera_target = np.array([0.0, 0.0, 0.0])   # Alvo da câmera
camera_up = np.array([0.0, 1.0, 0.0])       # Vetor "para cima"
polygons = create_polygons_3D()             # Cria cena 3D básica

def draw_polygons(polygons):
    """
    Função personalizada de desenho que aplica iluminação e materiais aos polígonos.
    Substitui a função padrão do Painter's Algorithm para suportar iluminação.
    """
    for p in polygons:
        color = p.get("color", (1, 1, 1))  # Cor padrão branca se não especificada
        normal = p.get("normal", [0, 1, 0])  # Normal padrão se não especificada
        
        # Extrai componentes RGB da cor
        r, g, b = color[0], color[1], color[2]
        
        # Define propriedades do material para iluminação:
        material_ambient = [r * 0.2, g * 0.2, b * 0.2, 1.0]    # Cor sob luz ambiente (20%)
        material_diffuse = [r * 0.8, g * 0.8, b * 0.8, 1.0]    # Cor sob luz difusa (80%)
        material_specular = [0.5, 0.5, 0.5, 1.0]               # Cor do brilho especular
        material_shininess = [50.0]                            # Intensidade do brilho
        
        # Aplica as propriedades do material
        glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)
        
        # Define a normal do polígono para cálculos de iluminação
        glNormal3f(normal[0], normal[1], normal[2])
        
        # Desenha o polígono preenchido com iluminação
        glBegin(GL_POLYGON)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()
        
        # 🔄 Desenha o contorno em preto (sem iluminação)
        glDisable(GL_LIGHTING)        # Desabilita iluminação temporariamente
        glColor3f(0, 0, 0)            # Cor preta para contorno
        glBegin(GL_LINE_LOOP)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()
        glEnable(GL_LIGHTING)         # Reabilita iluminação

def setup_materials():
    """Configura os materiais padrão para todos os objetos (não utilizado atualmente)"""
    material_ambient = [0.2, 0.2, 0.2, 1.0]    # Ambiente padrão
    material_diffuse = [0.8, 0.8, 0.8, 1.0]    # Difuso padrão
    material_specular = [1.0, 1.0, 1.0, 1.0]   # Especular intenso
    material_shininess = [100.0]                # Brilho alto
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def apply_material(color):
    """
    Aplica um material com cor específica a um polígono individual.
    (Função alternativa não utilizada na versão atual)
    """
    r, g, b = color[0], color[1], color[2]
    
    material_ambient = [r * 0.2, g * 0.2, b * 0.2, 1.0]
    material_diffuse = [r * 0.8, g * 0.8, b * 0.8, 1.0]
    material_specular = [0.5, 0.5, 0.5, 1.0]  # Especular menos intenso
    material_shininess = [30.0]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, material_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)

def setup_lighting():
    """
    Configura o sistema de iluminação do OpenGL com duas fontes de luz.
    """
    # 💡 Luz 1 - Luz principal (tipo lanterna/spotlight)
    light1_ambient = [0.2, 0.2, 0.2, 1.0]      # Componente ambiente
    light1_diffuse = [1.0, 1.0, 1.0, 1.0]      # Componente difusa (cor principal)
    light1_specular = [1.0, 1.0, 1.0, 1.0]     # Componente especular (brilho)
    light1_position = [-2.0, 2.0, 1.0, 1.0]    # Posição (w=1 → luz posicional)
    spot_direction = [-1.0, -1.0, 0.0]         # Direção do spotlight
    
    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    
    # Configura atenuação da luz (como a intensidade diminui com a distância)
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.5)   # Atenuação constante
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.5)     # Atenuação linear
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.2)  # Atenuação quadrática
    
    # Configurações de spotlight
    glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 45.0)           # Ângulo de abertura (45°)
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, spot_direction)  # Direção do foco
    glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)          # Intensidade do foco
    
    # 💡 Luz 2 - Luz de preenchimento (fill light)
    light2_ambient = [0.1, 0.1, 0.1, 1.0]      # Ambiente suave
    light2_diffuse = [0.4, 0.4, 0.4, 1.0]      # Difusa fraca (preenchimento)
    light2_specular = [0.2, 0.2, 0.2, 1.0]     # Especular mínimo
    light2_position = [3.0, 3.0, 3.0, 1.0]     # Posição diferente da luz principal
    
    glLightfv(GL_LIGHT2, GL_AMBIENT, light2_ambient)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, light2_diffuse)
    glLightfv(GL_LIGHT2, GL_SPECULAR, light2_specular)
    glLightfv(GL_LIGHT2, GL_POSITION, light2_position)
    
    # Habilita ambas as luzes
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

# ------------------------------------------------------
# Callbacks GLUT
# ------------------------------------------------------
def display():
    """Callback de renderização - desenha a cena a cada frame"""
    global polygons, camera_pos, camera_target, camera_up, angle
    # Usa a função personalizada de desenho com iluminação
    render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle, draw_func=draw_polygons)

def idle():
    """Callback de ociosidade - animação automática"""
    global angle
    angle += 0.5  # Velocidade de rotação
    if angle >= 360: 
        angle -= 360  # Mantém o ângulo no range [0, 360)
    glutPostRedisplay()

def reshape(w, h):
    """Callback de redimensionamento da janela"""
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 0.1, 100.0)  # Projeção perspectiva
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    """Callback de teclado - controles interativos"""
    global camera_pos
    
    if key == b'\x1b':  # ESC - sai do programa
        sys.exit(0)
    elif key == b'w':   # W - move câmera para frente
        camera_pos[2] -= 0.2
    elif key == b's':   # S - move câmera para trás
        camera_pos[2] += 0.2
    elif key == b'a':   # A - move câmera para esquerda
        camera_pos[0] -= 0.2
    elif key == b'd':   # D - move câmera para direita
        camera_pos[0] += 0.2
    elif key == b'q':   # Q - move câmera para cima
        camera_pos[1] += 0.2
    elif key == b'e':   # E - move câmera para baixo
        camera_pos[1] -= 0.2
    elif key == b'1':   # Tecla 1 - alterna luz principal
        if glIsEnabled(GL_LIGHT1):
            glDisable(GL_LIGHT1)
            print("Luz 1 desligada")
        else:
            glEnable(GL_LIGHT1)
            print("Luz 1 ligada")
    elif key == b'2':   # Tecla 2 - alterna luz de preenchimento
        if glIsEnabled(GL_LIGHT2):
            glDisable(GL_LIGHT2)
            print("Luz 2 desligada")
        else:
            glEnable(GL_LIGHT2)
            print("Luz 2 ligada")
    
    glutPostRedisplay()

# ------------------------------------------------------
# Main
# ------------------------------------------------------
def execTest():
    """Função principal que inicializa a aplicação"""
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"OpenGL Lighting Painter's Algorithm")
    
    # Registra callbacks
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    
    # ⚙️ Configurações avançadas do OpenGL
    glClearColor(0.0, 0.0, 0.0, 1.0)  # Fundo preto
    glEnable(GL_DEPTH_TEST)            # Teste de profundidade
    glEnable(GL_LIGHTING)              # Habilita sistema de iluminação
    glEnable(GL_NORMALIZE)             # Normaliza normais automaticamente
    
    # Configura iluminação
    setup_lighting()
    
    # Define modelo de sombreamento
    glShadeModel(GL_SMOOTH)            # Sombreamento suave (Gouraud)
    
    # Instruções para o usuário
    print("Controles:")
    print("WASD/QE: Mover câmera")
    print("1: Alternar luz principal")
    print("2: Alternar luz de preenchimento")
    print("ESC: Sair")
    
    glutMainLoop()

if __name__ == "__main__":
    execTest()