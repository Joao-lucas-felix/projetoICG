# painter_algorithm.py
from OpenGL.GL import *
import numpy as np

# ------------------------------------------------------
# Utilitários
# ------------------------------------------------------

def normalize(v):
    """Normaliza um vetor 3D (torna seu comprimento igual a 1)"""
    n = np.linalg.norm(v)  # Calcula a magnitude/norma do vetor
    return v / n if n else v  # Divide pelo comprimento, evita divisão por zero

def look_at(eye, target, up):
    """
    Cria uma matriz de visualização (view matrix) similar ao gluLookAt
    eye: posição da câmera
    target: ponto para onde a câmera está olhando
    up: vetor que define a direção "para cima" da câmera
    """
    f = normalize(target - eye)  # Vetor forward (direção da câmera)
    s = normalize(np.cross(f, up))  # Vetor right (direita da câmera)
    u = np.cross(s, f)  # Vetor up real (recalculado para garantir ortogonalidade)
    
    # Matriz de rotação da câmera
    M = np.identity(4, dtype=float)
    M[0, 0:3] = s  # Eixo X (right)
    M[1, 0:3] = u  # Eixo Y (up)
    M[2, 0:3] = -f # Eixo Z (forward negativo - OpenGL usa sistema right-handed)
    
    # Matriz de translação (move o mundo para a posição da câmera)
    T = np.identity(4, dtype=float)
    T[0:3, 3] = -eye  # Translação inversa da posição da câmera
    
    return M @ T  # Combina rotação e translação

def transform_point(mat4, v3):
    """Aplica uma transformação matricial 4x4 a um ponto 3D"""
    v4 = np.array([v3[0], v3[1], v3[2], 1.0], dtype=float)  # Converte para coordenadas homogêneas
    tv = mat4 @ v4  # Aplica a transformação matricial
    return tv[0:3] / (tv[3] if tv[3] != 0 else 1.0)  # Retorna para coordenadas 3D (perspectiva division)

# ------------------------------------------------------
# Painter's Algorithm - Implementação do algoritmo do pintor
# ------------------------------------------------------

def polygon_avg_depth(poly, view_mat):
    """
    Calcula a profundidade média de um polígono após transformação pela view matrix
    Usa a coordenada Z (profundidade) no espaço da câmera
    """
    verts = poly["vertices"]
    # Transforma cada vértice e extrai a coordenada Z (profundidade)
    depths = [transform_point(view_mat, v)[2] for v in verts]
    return np.mean(depths)  # Retorna a profundidade média

def sort_polygons(polygons, view_mat):
    """
    Ordena os polígonos por profundidade média (do mais distante para o mais próximo)
    O Painter's Algorithm requer desenhar dos objetos mais distantes para os mais próximos
    """
    return sorted(polygons, key=lambda p: polygon_avg_depth(p, view_mat))

def draw_polygons(polygons):
    """
    Função padrão para desenhar polígonos no OpenGL
    Desenha cada polígono com cor sólida e contorno preto
    """
    for p in polygons:
        # Define a cor do polígono (padrão: branco)
        color = p.get("color", (1,1,1))
        glColor3f(*color)
        
        # Desenha o polígono preenchido
        glBegin(GL_POLYGON)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()
        
        # Desenha o contorno do polígono em preto
        glColor3f(0,0,0)
        glBegin(GL_LINE_LOOP)
        for v in p["vertices"]:
            glVertex3f(v[0], v[1], v[2])
        glEnd()

def painter_algorithm(polygons, view_mat, angle=0.0, draw_func=draw_polygons):
    """
    Implementação principal do Painter's Algorithm
    polygons: lista de polígonos a serem desenhados
    view_mat: matriz de visualização para cálculo de profundidade
    angle: ângulo de rotação opcional para animação
    draw_func: função personalizada para desenho (padrão: draw_polygons)
    """
    # Ordena polígonos pela profundidade (mais distante primeiro)
    ordered = sort_polygons(polygons, view_mat)

    # Configurações específicas do Painter's Algorithm
    glDisable(GL_DEPTH_TEST)   # Desativa teste de profundidade (Z-buffer)
    glDisable(GL_LIGHTING)     # Desativa iluminação para usar cores sólidas

    # Aplica transformações (rotação para animação)
    glPushMatrix()
    glRotatef(angle, 0, 1, 0)  # Rotação em Y
    draw_func(ordered)          # Desenha polígonos ordenados
    glPopMatrix()
    
    # Restaura iluminação para outros elementos da cena
    glEnable(GL_LIGHTING)

def render_scene_painter(polygons, camera_pos, camera_target, camera_up, angle=0.0, draw_func=draw_polygons):
    """
    Função principal de renderização que integra o Painter's Algorithm
    com a configuração de câmera do OpenGL
    """
    from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT
    from OpenGL.GLU import gluLookAt
    from OpenGL.GLUT import glutSwapBuffers

    # Limpa os buffers de cor e profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Configura a matriz de modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Define a visualização da câmera usando gluLookAt
    gluLookAt(*(camera_pos.tolist() + camera_target.tolist() + camera_up.tolist()))
    
    # Calcula a matriz de visualização para o Painter's Algorithm
    view_mat = look_at(camera_pos, camera_target, camera_up)
    
    # Executa o Painter's Algorithm
    painter_algorithm(polygons, view_mat, angle, draw_func=draw_func)
    
    # Troca os buffers (double buffering)
    glutSwapBuffers()