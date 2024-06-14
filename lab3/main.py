import numpy as np
import tkinter as tk
from tkinter import ttk

RESOLUTION = 4
RES_CHANGERATE = 2
MOVSPEED = 300

class BezierCurveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ivanov A. S. 1303 LR3")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        self.show_points = True
        self.points = np.array([[50, 50], [50, 150], [610, 300], [600, 600]])
        self.selected_point = None

        # Создаем метку для пояснения разрешения
        self.resolution_label = tk.Label(root, text="Resolution: " + str(RESOLUTION))
        self.resolution_label.pack()

        # Создаем метку для вывода координат точек кривой
        self.curve_points_label = tk.Label(root, text="")
        self.curve_points_label.pack()

        self.resolution_slider = ttk.Scale(root, from_=1, to=10, orient='horizontal', length=200)
        self.resolution_slider.set(RESOLUTION)
        self.resolution_slider.pack()
        self.resolution_slider.bind("<ButtonRelease-1>", self.on_resolution_change)

        self.draw()

        self.canvas.bind("<Motion>", self.on_mouse_motion)
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def draw(self):
        self.canvas.delete("all")

        bezier_curve = self.calc_bezier(self.points, RESOLUTION)
        for i in range(len(bezier_curve) - 1):
            self.canvas.create_line(bezier_curve[i][0], bezier_curve[i][1],
                                    bezier_curve[i + 1][0], bezier_curve[i + 1][1],
                                    fill='white')

        if self.show_points:
            for point in bezier_curve:
                self.canvas.create_oval(point[0] - 3, point[1] - 3, point[0] + 3, point[1] + 3, fill='yellow')

        for i, point in enumerate(self.points):
            color = 'red' if i in [0, 3] else 'green'
            self.canvas.create_oval(point[0] - 4, point[1] - 4, point[0] + 4, point[1] + 4, fill=color)

        # Отрисовка соединительных линий между крайними красными и крайними зелеными точками
        self.canvas.create_line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1], fill='red')
        self.canvas.create_line(self.points[2][0], self.points[2][1], self.points[3][0], self.points[3][1], fill='red')

        # Обновляем текст метки с координатами точек кривой, округляя их до десятых
        curve_points_text = ", ".join([f"({round(point[0], 1)}, {round(point[1], 1)})" for point in bezier_curve])
        self.curve_points_label.config(text="Curve Points: " + curve_points_text)

    def on_mouse_motion(self, event):
        if self.selected_point is not None:
            self.points[self.selected_point] = [event.x, event.y]
            self.draw()

    def on_mouse_press(self, event):
        for i, point in enumerate(self.points):
            if abs(event.x - point[0]) < 5 and abs(event.y - point[1]) < 5:
                self.selected_point = i
                break

    def on_mouse_release(self, event):
        self.selected_point = None

    def calc_bezier(self, points, resolution):
        t_values = np.linspace(0, 1, resolution + 1)
        bezier_curve = [self.cube_bezier(t, *points) for t in t_values]
        return bezier_curve

    def cube_bezier(self, t, p0, p1, p2, p3):
        q0 = self.quad_bezier(t, p0, p1, p2)
        q1 = self.quad_bezier(t, p1, p2, p3)
        c0 = self.lerp(t, q0, q1)
        return c0

    def quad_bezier(self, t, p0, p1, p2):
        l0 = self.lerp(t, p0, p1)
        l1 = self.lerp(t, p1, p2)
        q0 = self.lerp(t, l0, l1)
        return q0

    def lerp(self, t, p0, p1):
        a = 1 - t
        return (a * p0[0] + t * p1[0], a * p0[1] + t * p1[1])

    def on_resolution_change(self, event):
        global RESOLUTION
        RESOLUTION = int(self.resolution_slider.get())
        self.resolution_label.config(text="Resolution: " + str(RESOLUTION))  # Обновляем значение разрешения
        self.draw()

def main():
    root = tk.Tk()
    app = BezierCurveApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
