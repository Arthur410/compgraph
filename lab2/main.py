import sys
import random
from OpenGL import GL as gl
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplitter
from PyQt6.QtWidgets import QComboBox
from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel, QGroupBox
from typing import List


# Control panel widget
class ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        primitives_label = QLabel("Primitive Selection", self)
        self.primitive_selector = Selector([
            gl.GL_POINTS, gl.GL_LINES, gl.GL_LINE_STRIP, gl.GL_LINE_LOOP, gl.GL_TRIANGLES,
            gl.GL_TRIANGLE_STRIP, gl.GL_TRIANGLE_FAN, gl.GL_QUADS, gl.GL_QUAD_STRIP, gl.GL_POLYGON
        ], self)

        # Clipping group
        scissors_box = QGroupBox("Clipping Test", self)
        scissors_layout = QVBoxLayout()
        scissors_box.setLayout(scissors_layout)
        sx_label = QLabel('x', self)
        self.scissors_x = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        sy_label = QLabel('y', self)
        self.scissors_y = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        sw_label = QLabel('Width w', self)
        self.scissors_w = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        sh_label = QLabel('Height h', self)
        self.scissors_h = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        for i in [sx_label, self.scissors_x, sy_label, self.scissors_y, sw_label, self.scissors_w, sh_label, self.scissors_h]:
            scissors_layout.addWidget(i)

        # Transparency group
        transparency_box = QGroupBox("Transparency Test", self)
        transparency_layout = QVBoxLayout()
        transparency_box.setLayout(transparency_layout)
        transparency_func_label = QLabel('Testing Function')
        self.transparency_func = Selector([
            gl.GL_ALWAYS, gl.GL_NEVER, gl.GL_LESS, gl.GL_EQUAL, gl.GL_LEQUAL,
            gl.GL_GREATER, gl.GL_NOTEQUAL, gl.GL_GEQUAL
        ], self)

        transparency_ref_label = QLabel('Reference Value')
        self.transparency_ref = QSlider(QtCore.Qt.Orientation.Horizontal, self)

        for i in [transparency_func_label, self.transparency_func, transparency_ref_label, self.transparency_ref]:
            transparency_layout.addWidget(i)

        # Blending group
        mix_box = QGroupBox("Blending Test", self)
        mix_layout = QVBoxLayout()
        mix_box.setLayout(mix_layout)
        s_factor_label = QLabel('Source Factor sfactor')
        self.s_factor = Selector([
            gl.GL_ONE, gl.GL_ZERO, gl.GL_DST_COLOR, gl.GL_ONE_MINUS_DST_COLOR, gl.GL_SRC_ALPHA,
            gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_DST_ALPHA, gl.GL_ONE_MINUS_DST_ALPHA, gl.GL_SRC_ALPHA_SATURATE
        ], self)

        d_factor_label = QLabel('Destination Factor dfactor (in frame buffer)')
        self.d_factor = Selector([
            gl.GL_ZERO, gl.GL_ONE, gl.GL_SRC_COLOR, gl.GL_ONE_MINUS_SRC_COLOR, gl.GL_SRC_ALPHA,
            gl.GL_ONE_MINUS_SRC_ALPHA, gl.GL_DST_ALPHA, gl.GL_ONE_MINUS_DST_ALPHA
        ], self)

        for i in [s_factor_label, self.s_factor, d_factor_label, self.d_factor]:
            mix_layout.addWidget(i)

        #
        for i in [
            primitives_label,
            self.primitive_selector,
            scissors_box,
            transparency_box,
            mix_box
        ]:
            layout.addWidget(i)

        layout.addStretch()


def random_color():
    return [random.uniform(-1, 1) for _ in range(3)]


def draw_points():
    gl.glBegin(gl.GL_POINTS)
    points = [
        (0, 0), (0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1), (0.5, 0.5)
    ]
    for i in points:
        gl.glColor3dv(random_color())
        gl.glVertex2dv(i)
    gl.glEnd()


def draw_lines():
    gl.glBegin(gl.GL_LINES)
    lines = [
        ((-0.5, 0), (0, 1)),
        ((1, 0), (-1, 0.5)),
        ((0.7, -1), (1, 1)),
        ((-0.5, -0.7), (0.8, 0.5)),
        ((-0.4, -0.7), (0.8, -0.5))
    ]
    for i in lines:
        for p in i:
            gl.glColor3dv(random_color())
            gl.glVertex2dv(p)
    gl.glEnd()


def draw_line_strip():
    gl.glBegin(gl.GL_LINE_STRIP)
    points = [
        (-0.5, 0), (-0.7, 0.8),
        (0, 0.6), (1, 0.5),
        (0.7, 0.8), (0.9, -0.8),
        (-0.1, -0.7), (0, 0.95)
    ]
    for p in points:
        gl.glColor3dv(random_color())
        gl.glVertex2dv(p)
    gl.glEnd()


def draw_line_loop():
    gl.glBegin(gl.GL_LINE_LOOP)
    points = [
        (-0.5, 0), (-0.7, 0.8),
        (0, 0.6), (1, 0.5),
        (0.7, 0.8), (0.9, -0.8),
        (-0.1, -0.7), (0, 0.95)
    ]
    for p in points:
        gl.glColor3dv(random_color())
        gl.glVertex2dv(p)
    gl.glEnd()


def draw_triangles():
    gl.glBegin(gl.GL_TRIANGLES)
    triangles = [
        ((-0.9, -0.5), (0.4, 0.4), (-0.2, -0.9)),
        ((0.9, -0.5), (-0.4, 0.4), (0.2, -0.9)),
        ((-0.4, 0.9), (0.4, 0.9), (0, -0.4)),
    ]
    colors = [(0.9, 0.2, 0.1, 0.4), (0.2, 0.7, 0.1, 0.5), (0.1, 0.2, 0.8, 0.6)]
    for i, color in zip(triangles, colors):
        gl.glColor4dv(color)
        for p in i:
            gl.glVertex2dv(p)
    gl.glEnd()


def draw_triangle_strip():
    gl.glBegin(gl.GL_TRIANGLE_STRIP)
    points = [
        (-0.9, -0.5), (-0.3, 0.6), (-0.2, -0.9),
        (0.1, -0.1), (0.7, -0.8), (0.8, 0.8), (-0.9, -0.3)
    ]
    colors = [
        (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5),
        (0.2, 0.7, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5), (0.1, 0.2, 0.8, 0.5), (0.1, 0.2, 0.8, 0.5)
    ]
    for i, color in zip(points, colors):
        gl.glColor4dv(color)
        gl.glVertex2dv(i)
    gl.glEnd()


def draw_triangle_fan():
    gl.glBegin(gl.GL_TRIANGLE_FAN)
    points = [
        (0, 0), (-0.7, -0.8), (0, -0.9), (0.3, -0.4),
        (0.9, -0.3), (0.3, 0.8), (-0.5, 0.8), (-0.1, -0.99)
    ]
    colors = [
        (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5),
        (0.2, 0.7, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5), (0.1, 0.2, 0.8, 0.5),
        (0.1, 0.2, 0.8, 0.5), (0.1, 0.2, 0.8, 0.5)
    ]
    for i, color in zip(points, colors):
        gl.glColor4dv(color)
        gl.glVertex2dv(i)
    gl.glEnd()


def draw_quads():
    gl.glBegin(gl.GL_QUADS)
    quads = [
        ((-0.9, -0.8), (-0.8, -0.1), (-0.2, 0.0), (-0.1, -0.8)),
        ((0.9, -0.8), (0.8, -0.1), (0.2, 0.0), (0.1, -0.8)),
        ((-0.4, 0.8), (0.5, 0.7), (0.7, 0.2), (-0.6, 0.1)),
        ((0.1, 0.6), (-0.4, -0.4), (0.4, -0.4), (0.8, 0.1)),
    ]
    colors = [(0.9, 0.2, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5), (0.1, 0.2, 0.8, 0.5), (0.8, 0.9, 0.1, 0.5)]
    for i, color in zip(quads, colors):
        gl.glColor4dv(color)
        for p in i:
            gl.glVertex2dv(p)
    gl.glEnd()


def draw_quad_strip():
    gl.glBegin(gl.GL_QUAD_STRIP)
    quads = [
        (-0.9, -0.8), (-0.8, -0.1), (-0.1, -0.8), (-0.2, 0.0),
        (0.1, -0.8), (0.2, -0.1), (0.5, -0.8), (0.8, 0.1),
        (-0.4, 0.8), (0.5, 0.7),
    ]
    colors = [
        (0.1, 0.2, 0.8, 0.5), (0.1, 0.2, 0.8, 0.5), (0.1, 0.2, 0.8, 0.5), (0.8, 0.9, 0.1, 0.5),
        (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5),
        (0.2, 0.7, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5)
    ]
    for p, color in zip(quads, colors):
        gl.glColor4dv(color)
        gl.glVertex2dv(p)
    gl.glEnd()


def draw_polygon():
    gl.glBegin(gl.GL_POLYGON)
    points = [
        (-0.7, -0.8), (0, -0.1), (0.6, -0.6),
        (0.9, -0.0), (0.1, 0.8), (-0.5, 0.1),
    ]
    colors = [
        (0.9, 0.2, 0.1, 0.5), (0.9, 0.2, 0.1, 0.5), (0.2, 0.7, 0.1, 0.5),
        (0.2, 0.7, 0.1, 0.5), (0.1, 0.2, 0.8, 0.5), (0.1, 0.2, 0.8, 0.5),
    ]
    for i, color in zip(points, colors):
        gl.glColor4dv(color)
        gl.glVertex2dv(i)
    gl.glEnd()


# Rendering functions dictionary
renderers = dict([
    (gl.GL_POINTS, draw_points),
    (gl.GL_LINES, draw_lines),
    (gl.GL_LINE_STRIP, draw_line_strip),
    (gl.GL_LINE_LOOP, draw_line_loop),
    (gl.GL_TRIANGLES, draw_triangles),
    (gl.GL_TRIANGLE_STRIP, draw_triangle_strip),
    (gl.GL_TRIANGLE_FAN, draw_triangle_fan),
    (gl.GL_QUADS, draw_quads),
    (gl.GL_QUAD_STRIP, draw_quad_strip),
    (gl.GL_POLYGON, draw_polygon),
])

# OpenGL widget
class GLWidget(QOpenGLWidget):
    view_port_resized = QtCore.pyqtSignal((int, int))

    def __init__(self, parent=None):
        super().__init__(parent)
        # Rendering function called in the drawing loop (on updates)
        self.function = None

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)
        self.view_port_resized.emit(w, h)

    # Function called before any update
    def initializeGL(self):
        # Frame filling
        gl.glClearColor(1, 1, 1, 1)
        # Clearing buffers (color and depth)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    # Function called on update (via update or on size change)
    def paintGL(self):
        # Call the rendering function
        if self.function is not None:
            self.function()


# Selector widget for constants
class Selector(QComboBox):
    selected_signal = QtCore.pyqtSignal(gl.Constant)

    def __init__(self, objects: List[gl.Constant], parent=None):
        super().__init__(parent)
        self.objects = objects
        self.selected_object = objects[0]
        self.addItems(list(map(lambda p: p.name, objects)))
        self.currentIndexChanged.connect(self.on_selected)

    @QtCore.pyqtSlot(int)
    def on_selected(self, i):
        self.selected_object = self.objects[i]
        self.selected_signal.emit(self.selected_object)


# Main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("1303 Ivanov A. S. LR 2")
        self.control = ControlPanel(self)
        self.glwidget = GLWidget(self)
        sp = QSplitter(self)
        sp.addWidget(self.glwidget)
        sp.addWidget(self.control)
        sp.setStretchFactor(0, 1)

        self.setCentralWidget(sp)
        self.resize(900, 600)

        # Selected primitive
        self.primitive = None
        # Set the rendering function
        self.glwidget.function = self.render_function
        # Update sliders on window resize
        self.glwidget.view_port_resized.connect(self.on_gl_resize)

        c = self.control
        for i in [c.scissors_x, c.scissors_y, c.scissors_h, c.scissors_w, c.scissors_h, c.transparency_ref]:
            i.valueChanged.connect(self.redraw)
        for i in [c.primitive_selector, c.transparency_func, c.s_factor, c.d_factor]:
            i.selected_signal.connect(self.redraw)

        #
        self.on_gl_resize(9999, 9999)
        c.scissors_w.setValue(c.scissors_w.maximum())
        c.scissors_h.setValue(c.scissors_h.maximum())

    # Handle window resize
    @QtCore.pyqtSlot(int, int)
    def on_gl_resize(self, w, h):
        self.control.scissors_w.setMaximum(w)
        self.control.scissors_h.setMaximum(h)
        self.control.scissors_x.setMaximum(w)
        self.control.scissors_y.setMaximum(h)

    def render_function(self):
        # Color blending between vertices
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glLineWidth(10)
        gl.glPointSize(10)

        # Clipping
        gl.glEnable(gl.GL_SCISSOR_TEST)
        gl.glScissor(
            self.control.scissors_x.value(), self.control.scissors_y.value(),
            self.control.scissors_w.value(), self.control.scissors_h.value()
        )

        # Transparency
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glAlphaFunc(
            self.control.transparency_func.selected_object,
            self.control.transparency_ref.value() / self.control.transparency_ref.maximum()
        )

        # Blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(self.control.s_factor.selected_object, self.control.d_factor.selected_object)

        # Drawing
        renderers[self.control.primitive_selector.selected_object]()

    # Call image update
    @QtCore.pyqtSlot()
    def redraw(self):
        self.glwidget.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
