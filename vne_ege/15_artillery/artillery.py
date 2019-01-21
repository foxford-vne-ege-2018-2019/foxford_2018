import tkinter
import time
import math
from random import randint
from PIL import Image, ImageTk


canvas_width = 640
canvas_height = 480
default_initial_balls_number = 10
max_fire_energy = 200  # максимальное количество условных единиц энергии при стрельбе
max_click_time = 2  # максимальное количество секунд для набора энергии выстрела
default_ball_color = "yellow"
missile_color = "red"
global_tanks_number = 2


# --------- GAME MODEL: ----------
class Game:
    def __init__(self, initial_balls_number):
        self.initial_balls_number = initial_balls_number
        self.balls = []  # список объектов типа Ball
        self.terrain = Terrain()
        self.tanks = []
        for i in range(global_tanks_number):
            tank_x = randint(Tank.turret_radius, canvas_width - Tank.turret_radius)
            tank_y = canvas_height - self.terrain.heights[tank_x]
            tank = Tank(tank_x, tank_y, "darkgreen")
            self.tanks.append(tank)
        self.current_tank_index = 0
        self.missiles = []
        self.mode = 0  # установка режима прицеливания в начале игры

        self.t = 0
        self.dt = 0.05  # Квант модельного (рассчётного) времени.
        self.paused = True
        self._click_time = None
        for i in range(initial_balls_number):
            ball = Ball(default_ball_color)
            self.balls.append(ball)

    def start(self):
        self.paused = False

    def stop(self):
        self.paused = True

    def step(self):
        # доступ к флажку контроллера нужен для передачи ему информации, что игра кончилась:
        global allow_input
        if self.mode == 1:  # 1 -- режим полёта ракеты/снаряда
            if self.missiles:
                # рассчёт полёта каждого снаряда:
                for missile in self.missiles:
                    missile.step(self.dt)

                # TODO: уничтожать из списка ракеты, которые разбились о танк
                # Удаляем снаряды, которые коснулись земли или танка
                for k in range(len(self.missiles) - 1, -1, -1):
                    x = self.missiles[k].x
                    y = self.missiles[k].y
                    if y >= canvas_height - self.terrain.heights[x]:
                        print("Снаряд коснулся земли!")
                        self.missiles[k].delete()
                        self.missiles.pop(k)
                        break
            else:
                print("переход в режим прицеливания")
                self.mode = 0  # переход в режим прицеливания
                allow_input = True  # отмена блокировки прицеливания

        # Определяем факт конца игры (раунда):
        # if ???:
        #    self.game_over()
        #    allow_input = False
        self.t += self.dt

    def click(self, x, y):
        """ Подготовка к выстрелу танка.
        """
        self._click_time = time.time()

    def release(self, x, y):
        """ Подготовка к выстрелу танка.
        """
        global allow_input
        delta_t = time.time() - self._click_time
        energy = max_fire_energy * (1 if delta_t > max_click_time else delta_t / max_click_time)

        self.tanks[self.current_tank_index].aim(x, y)
        missile = self.tanks[self.current_tank_index].fire(energy)
        self.current_tank_index = (self.current_tank_index + 1) % global_tanks_number
        allow_input = False  # блокируем ввод на время полёта ракеты
        self.missiles.append(missile)

    def mouse_motion(self, x, y):
        """ При движении мышкой вызываем для танка (пока что единственного) его алгоритм прицеливания """
        self.tanks[self.current_tank_index].aim(x, y)

    def game_over(self):
        for ball in self.balls:
            ball.delete()
        for missile in self.missiles:
            missile.delete()
        for tank in self.tanks:
            tank.delete()
        print("Конец игры!")


class Terrain:
    color = "brown"
    period = 200
    max_height = 250
    amplitude = 30

    def __init__(self):
        self.heights = [0]*canvas_width
        self.lines = [0]*canvas_width
        for x in range(canvas_width):
            height = Terrain.max_height - Terrain.amplitude + \
                    Terrain.amplitude*math.sin(x*math.pi/Terrain.period)
            line = canvas.create_line(x, canvas_height - height,
                                      x, canvas_height,
                                      width=1, fill=Terrain.color)
            self.heights[x] = height
            self.lines[x] = line

    def update(self):
        for x in range(canvas_width):
            avatar = self.lines[x]
            canvas.coords(avatar, x, canvas_height - self.heights[x],
                          x, canvas_height)


class Ball:
    density = 1.0  # стандартная плотность

    def __init__(self, color):
        self.r = randint(5, 20)
        self.m = self.density * math.pi * self.r ** 2  # Масса пропорциональна площади, т.е. квадрату радиуса.
        self.x = randint(0 + self.r, canvas_width - self.r)
        self.y = randint(0 + self.r, canvas_height - self.r)
        self.Vx = randint(-100, 100)
        self.Vy = randint(-100, 100)
        self.oval_id = canvas.create_oval(self.x - self.r, self.y - self.r,
                                          self.x + self.r, self.y + self.r,
                                          fill=color)

    def delete(self):
        canvas.delete(self.oval_id)
        self.oval_id = None

    def step(self, dt):
        """ Сдвигает шарик ball в соответствии с его скоростью.
        """
        if self.oval_id is not None:
            Fx, Fy = self.force()
            ax = Fx / self.m
            ay = Fy / self.m

            self.x += self.Vx * dt + ax * dt ** 2 / 2
            self.y += self.Vy * dt + ay * dt ** 2 / 2
            self.Vx += ax * dt
            self.Vy += ay * dt

            if self.x + self.r >= canvas_width or self.x - self.r <= 0:
                self.Vx = -self.Vx
            if self.y + self.r >= canvas_height or self.y - self.r <= 0:
                self.Vy = -self.Vy
            canvas.coords(self.oval_id, (self.x - self.r, self.y - self.r,
                                         self.x + self.r, self.y + self.r))

    def force(self):
        Fx = 0
        Fy = self.m * 9.8  # default gravity
        return Fx, Fy

    def overlap(self, x, y):
        return (self.x - x)**2 + (self.y - y)**2 <= self.r**2

    def intersect(self, other):
        return (self.x - other.x)**2 + (self.y - other.y)**2 <= (self.r + other.r)**2

    def collide(self, other):
        delta_r = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2)**0.5
        ix = (other.x - self.x) / delta_r
        iy = (other.y - self.y) / delta_r
        Vself_normal = self.Vx*ix + self.Vy*iy
        Vother_normal = other.Vx * ix + other.Vy * iy
        self.Vx = self.Vx + (Vother_normal - Vself_normal) * ix
        self.Vy = self.Vy + (Vother_normal - Vself_normal) * iy
        other.Vx = other.Vx + (-Vother_normal + Vself_normal) * ix
        other.Vy = other.Vy + (-Vother_normal + Vself_normal) * iy


class Tank:
    """
    Танк, который умеет прицеливаться в заданную точку и порождать снаряды.
    """
    gun_length = 70
    turret_radius = 60
    gun_width = 8

    def __init__(self, x, y, color):
        """
            x, y - точка центра турели
            dx, dy - вектор ствола танка
        """
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = -1
        x1, y1, x2, y2 = self._gun_xy()
        self.gun_avatar = canvas.create_line(x1, y1, x2, y2, width=self.gun_width, fill=color)
        self.tank_image = ImageTk.PhotoImage(Image.open("pic/tank0.png"))
        self.tank_avatar = canvas.create_image(self.x, self.y - self.tank_image.height()//2,
                                               image=self.tank_image)

    def _gun_xy(self):
        """
        :return: (x1, y1, x2, y2) экранные координаты начала и конца ствола пушки
        """
        x1 = self.x
        y1 = self.y - self.turret_radius
        x2 = x1 + self.dx * self.gun_length
        y2 = y1 + self.dy * self.gun_length
        return x1, y1, x2, y2

    def aim(self, x, y):
        """ Прицеливание ствола в сторону точки (x, y)"""
        r = ((x - self.x)**2 + (y - self.y)**2)**0.5
        self.dx = (x - self.x) / r
        self.dy = (y - self.y) / r
        x1, y1, x2, y2 = self._gun_xy()
        canvas.coords(self.gun_avatar, x1, y1, x2, y2)

    def fire(self, energy):
        """
        Стреляет снарядом, порождая новый объект типа "летящий снаряд".
        :param energy: Энергия выстрела - положительное дробное число.
        :return: Снаряд, который будет поражать цели.
        """
        missile = Ball(missile_color)
        x1, y1, x2, y2 = self._gun_xy()
        missile.x = x2
        missile.y = y2
        missile.r = self.gun_width // 2
        missile.Vx = self.dx * energy
        missile.Vy = self.dy * energy
        missile.step(0)
        return missile

    def delete(self):
        """ удаляет аватары танка с холста"""
        canvas.delete(self.gun_avatar)
        self.gun_avatar = None
        canvas.delete(self.tank_avatar)
        self.tank_avatar = None


# --------- GAME CONTROLLER: ----------
# Режим игры - игра идёт или нет
allow_input = False
sleep_time = 50  # ms
scores = 0


def tick():
    time_label.after(sleep_time, tick)
    time_label['text'] = time.strftime('%H:%M:%S')
    if allow_input:
        game.step()


def button_start_game_handler():
    global allow_input
    if not allow_input:
        game.start()
        allow_input = True


def button_stop_game_handler():
    global allow_input
    if allow_input:
        game.stop()
        allow_input = False


def mouse_click_handler(event):
    if allow_input:
        game.click(event.x, event.y)


def mouse_release_handler(event):
    if allow_input:
        game.release(event.x, event.y)


def mouse_motion_handler(event):
    if allow_input:
        game.mouse_motion(event.x, event.y)


# --------- GAME VIEW: ----------
root = tkinter.Tk("Лопни шарик!")

buttons_panel = tkinter.Frame(bg="gray", width=canvas_width)
buttons_panel.pack(side=tkinter.TOP, anchor="nw", fill=tkinter.X)
button_start = tkinter.Button(buttons_panel, text="Start",
                              command=button_start_game_handler)
button_start.pack(side=tkinter.LEFT)
button_stop = tkinter.Button(buttons_panel, text="Stop",
                             command=button_stop_game_handler)
button_stop.pack(side=tkinter.LEFT)
time_label = tkinter.Label(buttons_panel, font='sans 14')
time_label.pack(side=tkinter.LEFT)
scores_text = tkinter.Label(buttons_panel, text="Ваши очки: 0")
scores_text.pack(side=tkinter.RIGHT)
canvas = tkinter.Canvas(root, bg='lightgray', width=canvas_width, height=canvas_height)
canvas.pack(anchor="nw", fill=tkinter.BOTH, expand=1)
canvas.bind("<Button-1>", mouse_click_handler)
canvas.bind("<ButtonRelease-1>", mouse_release_handler)
canvas.bind("<Motion>", mouse_motion_handler)

game = Game(default_initial_balls_number)

time_label.after_idle(tick)
root.mainloop()
