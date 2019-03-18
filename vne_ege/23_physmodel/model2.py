import tkinter as tk

SCALE_PX_FOR_METER = 300 / 150E9  # pixels for a meter
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 700
R = 5
TIME_SCALE_FACTOR = 10 * (365*24*60)

PAUSE_DELTA_T = 10  # ms
# second is a tick of time
dt = TIME_SCALE_FACTOR * PAUSE_DELTA_T / 1000

GRAVITY_CONST = 6.67408E-11
SOLAR_MASS = 1.98847e30
EARTH_MASS = 5.9722e24

t = 0
x = -149_598_023_000  # meters
y = 0
Vx = 0
Vy = 29_783  # meters per second


def Fx(m, x, y, Vx, Vy, t):
    r = (x**2 + y**2)**0.5
    F = GRAVITY_CONST*SOLAR_MASS*m/r**2
    return F*(-x/r)


def Fy(m, x, y, Vx, Vy, t):
    r = (x**2 + y**2)**0.5
    F = GRAVITY_CONST*SOLAR_MASS*m/r**2
    return F*(-y/r)


def tick():
    global t, x, y, Vx, Vy, canvas
    t += dt
    ax = Fx(EARTH_MASS, x, y, Vx, Vy, t) / EARTH_MASS
    ay = Fy(EARTH_MASS, x, y, Vx, Vy, t) / EARTH_MASS
    x += Vx*dt + ax*dt**2 / 2
    y += Vy*dt + ay*dt**2 / 2
    Vx += ax*dt
    Vy += ay*dt

    screen_x, screen_y = screen_xy(x, y)
    canvas.coords(earth_id, screen_x - R, screen_y - R,
                  screen_x + R, screen_y + R)

    root.after(PAUSE_DELTA_T, tick)


def screen_xy(x, y):
    screen_x = SCALE_PX_FOR_METER * x + SCREEN_WIDTH // 2
    screen_y = -SCALE_PX_FOR_METER * y + SCREEN_HEIGHT // 2
    return screen_x, screen_y


def main():
    global canvas, earth_id, root
    root = tk.Tk()
    root.geometry(str(SCREEN_WIDTH) + 'x' + str(SCREEN_HEIGHT))
    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=1)

    # THE SUN
    screen_x, screen_y = screen_xy(0, 0)
    canvas.create_oval(screen_x - R, screen_y - R,
                       screen_x + R, screen_y + R, fill="red")

    # THE EARTH
    screen_x, screen_y = screen_xy(x, y)
    earth_id = canvas.create_oval(screen_x - R, screen_y - R,
                                  screen_x + R, screen_y + R, fill="blue")

    tick()
    root.mainloop()


main()
