import os
import random
import time
import turtle

from PIL import ImageTk, Image


BASE_PATH = os.path.dirname(__file__)
BASE_X, BASE_Y = 0, -300
START_ENEMY_COUNT = 3
START_SPEED = 1
BUILDING_INFOS = {'house': [BASE_X - 400, BASE_Y],
                  'kremlin': [BASE_X - 200, BASE_Y],
                  'nuclear': [BASE_X + 200, BASE_Y],
                  'skyscraper': [BASE_X + 400, BASE_Y]}


class Missile:

    def __init__(self, x, y, color, x2, y2, speed):
        self.color = color

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.color(color)
        pen.penup()
        pen.setpos(x=x, y=y)
        pen.pendown()
        heading = pen.towards(x2, y2)
        pen.setheading(heading)
        pic_path = os.path.join(BASE_PATH, "images", "missile.gif")
        raw_pic = Image.open(pic_path).convert('RGBA')
        rotated_pic = raw_pic.rotate(angle=heading - 90, expand=1)
        pic = ImageTk.PhotoImage(rotated_pic)
        pic_name = f"pic_{heading - 90}"
        window.register_shape(pic_name, turtle.Shape("image", pic))
        pen.shape(pic_name)
        pen.showturtle()
        self.pen = pen

        self.state = 'launched'
        self.target = x2, y2
        self.radius = 0
        self.speed = speed

    def step(self):
        if self.state == 'launched':
            self.pen.forward(self.speed)
            if self.pen.distance(x=self.target[0], y=self.target[1]) < 30:
                self.state = 'explode'
                self.pen.shape('circle')
        elif self.state == 'explode':
            self.radius += 1
            if self.radius > 5:
                self.pen.clear()
                self.pen.hideturtle()
                self.state = 'dead'
            else:
                self.pen.shapesize(self.radius)
        elif self.state == 'dead':
            self.pen.clear()
            self.pen.hideturtle()

    def distance(self, x, y):
        return self.pen.distance(x=x, y=y)

    @property
    def x(self):
        return self.pen.xcor()

    @property
    def y(self):
        return self.pen.ycor()


class Building:
    INITIAL_HEALTH = 1000

    def __init__(self, x, y, bld_name, our_missiles=None):
        self.name = bld_name
        self.x = x
        self.y = y
        self.health = self.INITIAL_HEALTH
        self.our_missiles = our_missiles

        pen = turtle.Turtle()
        pen.hideturtle()
        pen.speed(0)
        pen.penup()
        pen.setpos(x=self.x, y=self.y)
        pic_path = os.path.join(BASE_PATH, "images", self.get_pic_name())
        window.register_shape(pic_path)
        pen.shape(pic_path)
        pen.showturtle()
        self.pen = pen

        title = turtle.Turtle(visible=False)
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.setpos(x=self.x, y=self.y - 80)
        title.color("purple")
        title.write(str(self.health), align="center", font=["Arial", 20, "bold"])
        self.title = title
        self.title_health = self.health

    def get_pic_name(self):
        if self.health < self.INITIAL_HEALTH * 0.2:
            return f"{self.name}_3.gif"
        if self.health < self.INITIAL_HEALTH * 0.8:
            return f"{self.name}_2.gif"
        return f"{self.name}_1.gif"

    def draw(self):
        pic_name = self.get_pic_name()
        pic_path = os.path.join(BASE_PATH, "images", pic_name)
        if self.pen.shape() != pic_path:
            window.register_shape(pic_path)
            self.pen.shape(pic_path)
        if self.health != self.title_health:
            self.title_health = self.health
            self.title.clear()
            if self.title_health > 0:
                self.title.write(str(self.title_health), align="center", font=["Arial", 20, "bold"])

    def is_alive(self):
        return self.health > 0


class MissileBase(Building):
    INITIAL_HEALTH = 2000

    def get_pic_name(self):
        for missile in self.our_missiles:
            if missile.distance(self.x, self.y) < 60:
                return f"{self.name}_opened.gif"
        return f"{self.name}.gif"


class Game:

    def __init__(self, game_window):

        game_window.clear()
        game_window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
        game_window.tracer(n=5)
        game_window.onclick(self.fire_missile)

        self.our_missiles = []
        self.enemy_missiles = []
        self.buildings = []

        self.enemy_count = START_ENEMY_COUNT
        self.speed = START_SPEED
        self.score = 0
        self.title_score = self.score

        pen = turtle.Turtle(visible=False)
        pen.speed(0)
        pen.penup()
        pen.setpos(x=520, y=320)
        pen.color("white")
        pen.write(f"SCORE: {self.title_score}", align="right", font=["Arial", 40, "bold"])
        self.pen = pen

        base = MissileBase(x=BASE_X, y=BASE_Y, bld_name='base', our_missiles=self.our_missiles)
        self.buildings.append(base)

        for name, position in BUILDING_INFOS.items():
            bld = Building(x=position[0], y=position[1], bld_name=name)
            self.buildings.append(bld)

    def fire_missile(self, x, y):
        if self.buildings[0].name == 'base' and self.buildings[0].is_alive():
            info = Missile(color='white', x=BASE_X, y=BASE_Y + 30, x2=x, y2=y, speed=30)
            self.our_missiles.append(info)

    def fire_enemy_missile(self):
        x = random.randint(-600, 600)
        y = 400
        alive_buildings = [b for b in self.buildings if b.is_alive()]
        if alive_buildings:
            target = random.choice(alive_buildings)
            info = Missile(color='red', x=x, y=y, x2=target.x, y2=target.y, speed=self.speed)
            self.enemy_missiles.append(info)

    @staticmethod
    def move_missiles(missiles):
        for missile in missiles:
            missile.step()

        dead_missiles = [missile for missile in missiles if missile.state == 'dead']
        for dead in dead_missiles:
            missiles.remove(dead)

    def check_enemy_count(self):
        if len(self.enemy_missiles) < self.enemy_count:
            self.fire_enemy_missile()

    def check_interceptions(self):
        for our_missile in self.our_missiles:
            if our_missile.state != 'explode':
                continue
            for enemy_missile in self.enemy_missiles:
                if enemy_missile.distance(our_missile.x, our_missile.y) < our_missile.radius * 15:
                    enemy_missile.state = 'dead'
                    self.score += 1
                    self.check_game_level()

    def check_impact(self):
        for enemy_missile in self.enemy_missiles:
            if enemy_missile.state != 'explode':
                continue
            for building in self.buildings:
                if enemy_missile.distance(building.x, building.y) < enemy_missile.radius * 30:
                    building.health -= 20
                    print(f"{building.name} - {building.health}")

    def check_game_level(self):
        if self.score % 25 == 0:
            self.speed += 1
        if self.score % 50 == 0:
            self.enemy_count += 1

    def game_over(self):
        i = 0
        for building in self.buildings:
            if building.health <= 0:
                i += 1
        return len(self.buildings) == i

    def draw_buildings(self):
        for building in self.buildings:
            building.draw()

    def draw_game_over(self):
        self.pen.setpos(x=0, y=0)
        self.pen.color("red")
        self.pen.write("Game Over", align="center", font=["Arial", 80, "bold"])

    def draw_score(self):
        self.pen.setpos(x=520, y=320)
        self.pen.color("white")

        if self.score != self.title_score:
            self.title_score = self.score
            self.pen.clear()
            self.pen.write(f"SCORE: {self.title_score}", align="right", font=["Arial", 40, "bold"])

    def main_loop(self):
        while True:
            window.update()
            self.draw_score()
            if self.game_over():
                return
            self.draw_buildings()
            self.check_impact()
            self.check_enemy_count()
            self.check_interceptions()
            self.move_missiles(missiles=self.our_missiles)
            self.move_missiles(missiles=self.enemy_missiles)
            time.sleep(0.02)


window = turtle.Screen()
window.setup(1200 + 3, 800 + 3, starty=0)
window.screensize(1200, 800)
window.textinput(title='Game', prompt="Press OK to start")

while True:
    game = Game(window)
    game.main_loop()
    game.draw_game_over()
    answer = window.textinput(title='Game', prompt="Continue game? Y/N")
    if answer is None:
        break
    elif answer.lower() not in ('y', "yes", 'д', "да"):
        break

window.bye()
