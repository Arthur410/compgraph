import sys
import random
from typing import List
from OpenGL import GL as gl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSplitter, QWidget, QVBoxLayout,
    QPushButton, QSlider, QLabel, QComboBox
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6 import QtCore


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.draw_function = None

    def initializeGL(self):
        gl.glClearColor(1, 1, 1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

    def paintGL(self):
        if self.draw_function is not None:
            self.draw_function()


class Lab1MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lab 1303 by Ivanov A. S. - Lab 1")
        self.control_panel = Lab1ControlPanel(self)
        self.gl_widget = GLWidget(self)
        splitter = QSplitter(self)
        splitter.addWidget(self.gl_widget)
        splitter.addWidget(self.control_panel)
        splitter.setStretchFactor(0, 1)
        self.setCentralWidget(splitter)
        self.resize(800, 600)

        self.primitive_count = dict([
            (gl.GL_POINTS, 1), (gl.GL_LINES, 2), (gl.GL_LINE_STRIP, 2),
            (gl.GL_LINE_LOOP, 2), (gl.GL_TRIANGLES, 3), (gl.GL_TRIANGLE_STRIP, 3),
            (gl.GL_TRIANGLE_FAN, 3), (gl.GL_QUADS, 4), (gl.GL_QUAD_STRIP, 4),
            (gl.GL_POLYGON, 1),
        ])

        self.generated_objects = []
        self.selected_primitive = None
        self.initialize()

    def initialize(self):
        self.selected_primitive = list(self.primitive_count.keys())[0]
        self.primitive_selected(self.selected_primitive)

        self.control_panel.primitive_selector.primitive_selected.connect(self.primitive_selected)
        self.control_panel.recreate_button.clicked.connect(self.regenerate_objects)
        self.control_panel.objects_count_slider.valueChanged.connect(self.redraw)
        self.control_panel.points_size_slider.valueChanged.connect(self.redraw)
        self.control_panel.line_width_slider.valueChanged.connect(self.redraw)

    @staticmethod
    def set_drawing_options(line_width: float, point_size: float):
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glLineWidth(line_width)
        gl.glPointSize(point_size)

    @QtCore.pyqtSlot()
    def regenerate_objects(self):
        self.generated_objects = generate_figures(
            self.primitive_count[self.selected_primitive], self.control_panel.objects_count_slider.maximum()
        )
        self.redraw()

    @QtCore.pyqtSlot(gl.Constant)
    def primitive_selected(self, primitive):
        self.selected_primitive = primitive
        self.generated_objects = generate_figures(
            self.primitive_count[primitive], self.control_panel.objects_count_slider.maximum()
        )

        self.gl_widget.draw_function = lambda: [
            self.set_drawing_options(self.control_panel.line_width_slider.value(),
                                     self.control_panel.points_size_slider.value()),
            draw_figures(self.generated_objects[:self.control_panel.objects_count_slider.value()],
                         self.selected_primitive)
        ]
        self.redraw()

    @QtCore.pyqtSlot()
    def redraw(self):
        self.gl_widget.update()


class PrimitiveSelector(QComboBox):
    primitive_selected = QtCore.pyqtSignal(gl.Constant)

    def __init__(self, primitives: List[gl.Constant], parent=None):
        super().__init__(parent)
        self.primitives = primitives
        self.addItems(list(map(lambda p: p.name, primitives)))
        self.currentIndexChanged.connect(self.selected)

    @QtCore.pyqtSlot(int)
    def selected(self, index):
        self.primitive_selected.emit(self.primitives[index])


def random_point(min_val=-1, max_val=1):
    return [random.uniform(min_val, max_val) for _ in range(2)]


def random_color():
    return [random.uniform(-1, 1) for _ in range(3)]


def generate_figures(num_points, num_objects):
    return list(list(random_point() for _ in range(num_points)) for _ in range(num_objects))


def draw_figures(figures, draw_type):
    gl.glBegin(draw_type)
    for points in figures:
        gl.glColor3dv(random_color())
        for point in points:
            gl.glVertex2dv(point)
    gl.glEnd()


class Lab1ControlPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.primitive_selector = PrimitiveSelector([
            gl.GL_POINTS, gl.GL_LINES, gl.GL_LINE_STRIP, gl.GL_LINE_LOOP, gl.GL_TRIANGLES,
            gl.GL_TRIANGLE_STRIP, gl.GL_TRIANGLE_FAN, gl.GL_QUADS, gl.GL_QUAD_STRIP, gl.GL_POLYGON
        ], self)

        self.recreate_button = QPushButton("Recreate Object", self)

        points_label = QLabel('Point Size', self)
        self.points_size_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.points_size_slider.setMinimum(1)
        self.points_size_slider.setMaximum(100)
        self.points_size_slider.setValue(10)

        lines_label = QLabel('Line Width', self)
        self.line_width_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.line_width_slider.setMinimum(1)
        self.line_width_slider.setMaximum(10)
        self.line_width_slider.setValue(5)

        count_label = QLabel('Number of Objects', self)
        self.objects_count_slider = QSlider(QtCore.Qt.Orientation.Horizontal, self)
        self.objects_count_slider.setMinimum(1)
        self.objects_count_slider.setMaximum(20)
        self.objects_count_slider.setValue(5)

        for widget in [
            self.primitive_selector, self.recreate_button, points_label, self.points_size_slider,
            lines_label, self.line_width_slider, count_label, self.objects_count_slider
        ]:
            layout.addWidget(widget)

        layout.addStretch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Lab1MainWindow()
    main_window.show()
    sys.exit(app.exec())
