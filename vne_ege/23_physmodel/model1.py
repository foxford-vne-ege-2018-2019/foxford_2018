import tkinter as tk

SCALE_PX_FOR_METER = 10.  # pixels for a meter
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
R = 5

PAUSE_DELTA_T = 100  # ms
dt = 0.01  # second is a tick of time

m = 1
t = 0
x = 0
y = 0
Vx = 3
Vy = 10


def screen_xy(x, y):
    screen_x = SCALE_PX_FOR_METER * x + SCREEN_WIDTH // 2
    screen_y = -SCALE_PX_FOR_METER * y + SCREEN_HEIGHT // 2
    return screen_x, screen_y


def main():
    global canvas, oval_id, root
    root = tk.Tk()
    root.geometry(str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    screen_x, screen_y = screen_xy(x, y)
    oval_id = canvas.create_oval(screen_x - R, screen_y - R,
                                 screen_x + R, screen_y + R, fill="red")
    tick()
    root.mainloop()


def Fx(m, x, y, Vx, Vy, t):
    return 0


def Fy(m, x, y, Vx, Vy, t):
    return -m*9.8


def tick():
    global t, m, x, y, Vx, Vy, canvas
    t += dt
    ax = Fx(m, x, y, Vx, Vy, t) / m
    ay = Fy(m, x, y, Vx, Vy, t) / m
    x += Vx*dt + ax*dt**2 / 2
    y += Vy*dt + ay*dt**2 / 2
    Vx += ax*dt
    Vy += ay*dt

    screen_x, screen_y = screen_xy(x, y)
    canvas.coords(oval_id, screen_x - R, screen_y - R,
                  screen_x + R, screen_y + R)

    root.after(PAUSE_DELTA_T, tick)


main()
