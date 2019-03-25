import tkinter as tk
from random import randint

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700
SCALE_PX_FOR_METER = 50  # pixels for a meter
BOX_X1 = -50
BOX_X2 = +50
BOX_Y1 = -20
BOX_Y2 = +20

TIME_SCALE_FACTOR = 1
PAUSE_DELTA_T = 10  # ms
# second is a tick of time
dt = TIME_SCALE_FACTOR * PAUSE_DELTA_T / 1000
t = 0


def screen_xy(x, y):
    screen_x = SCALE_PX_FOR_METER * x + SCREEN_WIDTH // 2
    screen_y = -SCALE_PX_FOR_METER * y + SCREEN_HEIGHT // 2
    return screen_x, screen_y


class Ball:
    def __init__(self, x=None, y=None, Vx=None, Vy=None, r=None, m=1):
        """ x, y in meters
            Vx, Vy in meters per second
            m in kilo
        """
        self.r = r or 2
        self.x = x or randint(BOX_X1 + self.r, BOX_X2 - self.r)
        self.y = y or randint(BOX_Y1 + self.r, BOX_Y2 - self.r)
        self.Vx = Vx if Vx is not None else randint(10, 30)
        self.Vy = Vy if Vy is not None else randint(10, 30)
        self.m = m

        self.oval_id = canvas.create_oval(*self.get_oval_screen_coords(),
                                          fill='green')

    def tick(self):
        """ Сдвигает шарик ball в соответствии с его скоростью.
        """
        Fx, Fy = self.force()
        ax = Fx / self.m
        ay = Fy / self.m

        self.x += self.Vx * dt + ax * dt ** 2 / 2
        self.y += self.Vy * dt + ay * dt ** 2 / 2
        self.Vx += ax * dt
        self.Vy += ay * dt

        if self.x + self.r >= BOX_X2 or self.x - self.r <= BOX_X1:
            self.Vx = -self.Vx
        if self.y + self.r >= BOX_Y2 or self.y - self.r <= BOX_Y1:
            self.Vy = -self.Vy

        canvas.coords(self.oval_id, self.get_oval_screen_coords())

    def get_oval_screen_coords(self):
        x1, y1 = screen_xy(self.x - self.r, self.y - self.r)
        x2, y2 = screen_xy(self.x + self.r, self.y + self.r)
        return x1, y1, x2, y2

    def force(self):
        Fx = 0
        Fy = -self.m * 9.8  # default gravity
        return Fx, Fy

    def collide(self, other):
        rx, ry = other.x - self.x, other.y - self.y
        nx, ny = [projection / (rx**2 + ry**2)**0.5 for projection in (rx, ry)]
        # проекция векторов скорости на ось взаимодействия (вектор нормали к плоскости столкновения)
        self_Vn = self.Vx*nx + self.Vy*ny
        other_Vn = other.Vx*nx + other.Vy*ny
        # При равных массах - тупо обмен нормальными скоростями
        self.Vx, self.Vy = self.Vx - self_Vn*nx + other_Vn*nx, self.Vy - self_Vn*ny + other_Vn*ny
        other.Vx, other.Vy = other.Vx - other_Vn*nx + self_Vn*nx, other.Vy - other_Vn*ny + self_Vn*ny

    def intersect(self, other):
        dr2 = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        return dr2 < (self.r + other.r)**2


def tick():
    global t, canvas, balls, SCALE_PX_FOR_METER
    t += dt
    for ball in balls:
        ball.tick()
    for i in range(len(balls)-1):
        for k in range(i+1, len(balls)):
            if balls[i].intersect(balls[k]):
                balls[i].collide(balls[k])

    canvas.coords(box, *screen_xy(BOX_X1, BOX_Y1), *screen_xy(BOX_X2, BOX_Y2))
    SCALE_PX_FOR_METER *= 0.999
    root.after(PAUSE_DELTA_T, tick)


def main():
    global canvas, root, balls, box
    root = tk.Tk()
    root.geometry(str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)
    box = canvas.create_rectangle(*screen_xy(BOX_X1, BOX_Y1),
                            *screen_xy(BOX_X2, BOX_Y2), fill="brown")

    balls = []
    for i in range(10):
        balls.append(Ball())

    tick()
    root.mainloop()


main()
