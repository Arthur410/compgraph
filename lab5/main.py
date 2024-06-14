import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, radians, sin

class FractalAnimation:
    def __init__(self):
        self.angle_z = 180  # Начальный угол для начала с освещенной стороны
        self.light_angle = 0
        self.amplitude = 0.5  # Амплитуда изменения цвета
        self.frequency = 0.05  # Увеличенная частота изменения цвета
        self.phase = 0  # Начальная фаза
        self.rotation_speed = 0.2  # Скорость вращения фрактала

    def recursive_string(self, string, iterations):
        prev_string = string
        result = string

        for _ in range(iterations):
            if _ % 2 == 0:
                new_string = prev_string.replace('+', 'temp').replace('-', '+').replace('temp', '-')
                result = f'+{new_string}-F-{new_string}'
            else:
                new_string = prev_string.replace('+', 'temp').replace('-', '+').replace('temp', '-')
                if new_string[0] == '-':
                    new_string = new_string[1:]
                result = f'{new_string}--F--{new_string}'

            prev_string = result

        return result

    def draw_fractal(self, angle, length):
        initial_string = "F"
        num_iterations = 8
        real_iterations = num_iterations - 1
        inst = self.recursive_string(initial_string, real_iterations)

        glPushMatrix()
        glTranslatef(0, 0, 0)  # Центр экрана
        glRotatef(self.angle_z, 0, 0.1, 0)  # Вращение вокруг оси Z
        glLineWidth(2.0)
        glBegin(GL_LINE_STRIP)
        x, y = 0, 0
        for cmd in inst:
            if cmd == 'F':
                x += length * cos(radians(angle))
                y += length * sin(radians(angle))
                glVertex3f(x, y, 0)  # Используем z=0 для плоскости XY
            elif cmd == '+':
                angle += 45
            elif cmd == '-':
                angle -= 45
        glEnd()
        glPopMatrix()

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Черный фон
        glClearColor(0, 0, 0, 1)

        # Устанавливаем вид
        glOrtho(-300, 300, -300, 300, -300, 300)  # Используем координату z

        angle = 0
        length = 8
        self.draw_fractal(angle, length)

        # Вычисляем цвет света по синусоидальной функции
        r = self.amplitude * cos(self.frequency * self.light_angle + self.phase) + 0.5  # Красный компонент
        g = self.amplitude * cos(self.frequency * self.light_angle + self.phase + 2 * 3.14 / 3) + 0.5  # Зеленый компонент
        b = self.amplitude * cos(self.frequency * self.light_angle + self.phase + 4 * 3.14 / 3) + 0.5  # Синий компонент

        # Устанавливаем цвет диффузного света
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [r, g, b, 1.0])

        # Устанавливаем свойства материала
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [r, g, b, 1.0])

        # Инкрементируем угол света для следующего кадра
        self.light_angle += 0.1

        glutSwapBuffers()

    def animate(self, value):
        self.angle_z += self.rotation_speed  # Замедляем прокрутку
        if self.angle_z > 360:
            self.angle_z -= 360

        glutPostRedisplay()
        glutTimerFunc(10, self.animate, 0)

    def main(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(600, 600)
        glutCreateWindow("Ivanov A. S. 5LR")
        glEnable(GL_DEPTH_TEST)
        glutDisplayFunc(self.draw)
        glutTimerFunc(25, self.animate, 0)

        # Устанавливаем свойства света
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)  # Включаем использование цветов материала

        # Устанавливаем режим материала цвета для управления окружающим и диффузным цветом материала
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Запускаем главный цикл
        glutMainLoop()

if __name__ == "__main__":
    animation = FractalAnimation()
    animation.main()
