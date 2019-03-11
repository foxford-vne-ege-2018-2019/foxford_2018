import tkinter as tk

SCALE_PX_FOR_METER = 4000.  # pixels for a meter
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PERSPECTIVE = SCREEN_WIDTH / SCALE_PX_FOR_METER


def tk_xy(screen_x, screen_y):
    tk_x = int(screen_x * SCALE_PX_FOR_METER + SCREEN_WIDTH / 2)
    tk_y = int(SCREEN_HEIGHT / 2 - screen_y * SCALE_PX_FOR_METER)
    return tk_x, tk_y


def projection(x, y, z):
    if z <= 0:  # точка находится сзади от глаза! => невидима
        return None
    k = PERSPECTIVE / z
    screen_x = k * x
    screen_y = k * y
    return screen_x, screen_y


def draw_3d_line(point1, point2, canvas):
    tk_x1, tk_y1 = tk_xy(*projection(*point1))
    tk_x2, tk_y2 = tk_xy(*projection(*point2))
    canvas.create_line(tk_x1, tk_y1, tk_x2, tk_y2)


def main():
    root = tk.Tk()
    root.geometry(str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    depth = 5
    points_a = [(1, 0, depth), (0, 1, depth), (0, -1, depth), (-1, 0, depth)]
    points_b = [(1, 0, depth + 1), (0, 1, depth + 1), (0, -1, depth + 1), (-1, 0, depth + 1)]

    for point1, point2 in zip(points_a, points_b):
        draw_3d_line(point1, point2, canvas)
    for point1, point2 in zip(points_a, points_a[1:] + points_a[:1]):
        draw_3d_line(point1, point2, canvas)

    root.mainloop()


main()
