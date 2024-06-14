import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

# Глобальные переменные для управления камерой и загруженными данными
gCamAng = 0.
gCamHeight = 3.
vertices = None
normals = None
faces = None
dropped = 0
modeFlag = 0
distanceFromOrigin = 45


# Функция обратного вызова для загрузки .obj файла
def dropCallback(window, paths):
    global vertices, normals, faces, dropped, gVertexArraySeparate
    numberOfFacesWith3Vertices = 0
    numberOfFacesWith4Vertices = 0
    numberOfFacesWithMoreThan4Vertices = 0
    dropped = 1
    fileName = paths[0].split('\\')[-1]

    with open(paths[0]) as f:
        lines = f.readlines()
        vStrings = [x.strip('v') for x in lines if x.startswith('v ')]
        vertices = convertVertices(vStrings)
        if np.amax(vertices) <= 1.2:
            vertices /= np.amax(vertices)
        else:
            vertices /= np.amax(vertices) / 2
        vnStrings = [x.strip('vn') for x in lines if x.startswith('vn')]
        if not vnStrings:
            normals = fillNormalsArray(len(vStrings))
        else:
            normals = convertVertices(vnStrings)
        faces = [x.strip('f') for x in lines if x.startswith('f')]
    for face in faces:
        if len(face.split()) == 3:
            numberOfFacesWith3Vertices += 1
        elif len(face.split()) == 4:
            numberOfFacesWith4Vertices += 1
        else:
            numberOfFacesWithMoreThan4Vertices += 1
    print("Имя файла:", fileName, "\nОбщее количество граней:", len(faces),
          "\nКоличество граней с 3 вершинами:", numberOfFacesWith3Vertices,
          "\nКоличество граней с 4 вершинами:", numberOfFacesWith4Vertices,
          "\nКоличество граней с более чем 4 вершинами:", numberOfFacesWithMoreThan4Vertices)

    if numberOfFacesWith4Vertices > 0 or numberOfFacesWithMoreThan4Vertices > 0:
        faces = triangulate()
    gVertexArraySeparate = createVertexArraySeparate()


# Функция для вычисления нормалей вершин
def fillNormalsArray(numberOfVertices):
    normals = np.zeros((numberOfVertices, 3))
    i = 0
    for vertice in vertices:
        normals[i] = normalized(vertice)
        i += 1
    return normals


# Функция для преобразования строк вершин в массив numpy
def convertVertices(verticesStrings):
    v = np.zeros((len(verticesStrings), 3))
    i = 0
    for vertice in verticesStrings:
        j = 0
        for t in vertice.split():
            try:
                v[i][j] = (float(t))
            except ValueError:
                pass
            j += 1
        i += 1
    return v


# Функция для триангуляции многоугольников
def triangulate():
    facesList = []
    nPolygons = []
    for face in faces:
        if (len(face.split()) >= 4):
            nPolygons.append(face)
        else:
            facesList.append(face)
    for face in nPolygons:
        for i in range(1, len(face.split()) - 1):
            seq = [str(face.split()[0]), str(face.split()[i]), str(face.split()[i + 1])]
            string = ' '.join(seq)
            facesList.append(string)
    return facesList


# Функция для создания массива вершин и нормалей
def createVertexArraySeparate():
    global vertices, normals, faces
    varr = np.zeros((len(faces) * 6, 3), 'float32')
    i = 0
    normalsIndex = 0
    verticeIndex = 0
    for face in faces:
        for f in face.split():
            if '//' in f:
                verticeIndex = int(f.split('//')[0]) - 1
                normalsIndex = int(f.split('//')[1]) - 1
            elif '/' in f:
                if len(f.split('/')) == 2:
                    verticeIndex = int(f.split('/')[0]) - 1
                    normalsIndex = int(f.split('/')[0]) - 1
                else:
                    verticeIndex = int(f.split('/')[0]) - 1
                    normalsIndex = int(f.split('/')[2]) - 1
            else:
                verticeIndex = int(f.split()[0]) - 1
                normalsIndex = int(f.split()[0]) - 1
            varr[i] = normals[normalsIndex]
            varr[i + 1] = vertices[verticeIndex]
            i += 2

    return varr


# Функция для отрисовки сцены
def render(ang):
    global gCamAng, gCamHeight, distanceFromOrigin, dropped
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(distanceFromOrigin, 1, 1, 10)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5 * np.sin(gCamAng), gCamHeight, 5 * np.cos(gCamAng), 0, 0, 0, 0, 1, 0)

    drawFrame()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    # Позиции и интенсивности освещения
    glPushMatrix()
    lightPos0 = (1., 2., 3., 1.)
    lightPos1 = (3., 2., 1., 1.)
    lightPos2 = (2., 3., 1., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)
    glPopMatrix()
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Установка белого цвета для света и материала
    glColor3f(1.0, 1.0, 1.0)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

    # Отрисовка объекта
    glPushMatrix()
    if dropped == 1:
        draw_glDrawArray()
    glPopMatrix()

    glDisable(GL_LIGHTING)


# Функция для отрисовки объекта
def draw_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size / 6))


# Функция для отрисовки координатной оси
def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()


def increase_detail():
    global gVertexArraySeparate, faces, normals, vertices
    print('Увеличиваем количество вершин')
    new_faces = []
    new_vertices = vertices.copy()
    for face in faces:
        v1, v2, v3 = [int(idx.split('/')[0]) - 1 for idx in face.split()]
        # Найдем середины сторон треугольника
        v12 = (new_vertices[v1] + new_vertices[v2]) / 2
        v23 = (new_vertices[v2] + new_vertices[v3]) / 2
        v31 = (new_vertices[v3] + new_vertices[v1]) / 2
        # Добавим новые вершины в массив вершин
        new_vertices = np.vstack([new_vertices, v12, v23, v31])
        # Добавим новые треугольники
        new_faces.append(f"{v1+1} {len(new_vertices)-2+1} {len(new_vertices)-1+1}")
        new_faces.append(f"{len(new_vertices)-2+1} {v2+1} {len(new_vertices)-1+1}")
        new_faces.append(f"{len(new_vertices)-2+1} {len(new_vertices)-1+1} {v3+1}")
    vertices = new_vertices
    faces = new_faces
    # Обновим массив нормалей и вершин
    normals = fillNormalsArray(len(vertices))

    # Обновим массив вершин и нормалей
    gVertexArraySeparate = createVertexArraySeparate()

def decrease_detail():
    global gVertexArraySeparate, faces, normals, vertices
    print('Уменьшаем количество вершин')
    new_faces = []
    new_vertices = vertices.copy()
    for i, face in enumerate(faces):
        if i % 2 == 0:
            new_faces.append(face)
    faces = new_faces
    # Обновим массив вершин и нормалей
    gVertexArraySeparate = createVertexArraySeparate()

# Функция обработки клавиш
def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight, modeFlag, distanceFromOrigin, vertices, gVertexArraySeparate, normals, faces
    # Определение шага для изменения размера
    step = 0.1

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_A:
            gCamAng += np.radians(-10 % 360)
        elif key == glfw.KEY_D:
            gCamAng += np.radians(10 % 360)
        elif key == glfw.KEY_W:
            if gCamHeight < 9:
                gCamHeight += .1
        elif key == glfw.KEY_S:
            if gCamHeight > -9:
                gCamHeight += -.1
        elif key == glfw.KEY_Q:
            if distanceFromOrigin > 0:
                distanceFromOrigin -= 1
        elif key == glfw.KEY_E:
            if distanceFromOrigin < 180:
                distanceFromOrigin += 1
        elif key == glfw.KEY_V:
            gCamAng = 0.
            gCamHeight = 1.
            distanceFromOrigin = 45
        elif key == glfw.KEY_KP_ADD:  # Увеличение вершин
            increase_detail()
        elif key == glfw.KEY_KP_SUBTRACT:  # Уменьшение вершин
            decrease_detail()


gVertexArraySeparate = np.zeros((3, 3))

mouse_button_pressed = False  # переменная для отслеживания состояния нажатия кнопки мыши

def cursor_pos_callback(window, xpos, ypos):
    global gCamAng, mouse_button_pressed
    sensitivity = 0.1
    if mouse_button_pressed:  # проверяем, зажата ли кнопка мыши
        dx = xpos - 320  # половина ширины окна
        dy = ypos - 320  # половина высоты окна
        gCamAng += dx * sensitivity
        glfw.set_cursor_pos(window, 320, 320)  # сбрасываем положение курсора в центр окна

def mouse_button_callback(window, button, action, mods):
    global mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            mouse_button_pressed = True
        elif action == glfw.RELEASE:
            mouse_button_pressed = False

def main():
    global gVertexArraySeparate
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, '3D Obj File Viewer', None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_drop_callback(window, dropCallback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_mouse_button_callback(window, mouse_button_callback)  # добавляем обратный вызов для отслеживания нажатия кнопки мыши
    glfw.swap_interval(1)
    count = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        count += 1
        ang = count % 360
        render(ang)
        count += 1
        glfw.swap_buffers(window)
    glfw.terminate()



# Функция для вычисления длины вектора
def l2norm(v):
    return np.sqrt(np.dot(v, v))


# Функция для нормализации вектора
def normalized(v):
    l = l2norm(v)
    return 1 / l * np.array(v)


# Функция обратного вызова для изменения размера окна
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


if __name__ == "__main__":
    main()
