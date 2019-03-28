import os
import random
import turtle


BASE_PATH = os.path.dirname(__file__)

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3, starty=0)
window.bgpic(os.path.join(BASE_PATH, "images", "background.png"))
window.screensize(1200, 800)
window.tracer(n=2)

BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5


def fire_missile(x, y):
    new_missile = turtle.Turtle(visible=False)
    new_missile.speed(0)
    new_missile.color('white')
    new_missile.penup()
    new_missile.setpos(x=BASE_X, y=BASE_Y)
    new_missile.pendown()
    heading = new_missile.towards(x=x, y=y)
    if 0 < heading < 180:
        new_missile.setheading(heading)
        new_missile.showturtle()

        missile_info = {'missile': new_missile, 'target': [x, y],
                        'state': 'launched', 'radius': 0}
        our_missiles.append(missile_info)


def fire_enemy_missile():
    x = random.randint(-600, 600)
    y = 400

    new_missile = turtle.Turtle(visible=False)
    new_missile.speed(0)
    new_missile.color('red')
    new_missile.penup()
    new_missile.setpos(x=x, y=y)
    new_missile.pendown()
    heading = new_missile.towards(x=BASE_X, y=BASE_Y)
    new_missile.setheading(heading)
    new_missile.showturtle()

    missile_info = {'missile': new_missile, 'target': [BASE_X, BASE_Y],
                    'state': 'launched', 'radius': 0}
    enemy_missiles.append(missile_info)


def move_missile(missiles_list):
    for missile_info in missiles_list:
        state = missile_info['state']
        missile = missile_info['missile']
        if state == 'launched':
            missile.forward(4)
            target = missile_info['target']
            if missile.distance(x=target[0], y=target[1]) < 5:
                missile.shape('circle')
                missile_info['state'] = 'explode'
        elif state == 'explode':
            missile_info['radius'] += 1
            if missile_info['radius'] > 5:
                missile.clear()
                missile.hideturtle()
                missile_info['state'] = 'dead'
                dead_missiles.append(missile_info)
            else:
                missile.shapesize(missile_info['radius'])


window.onclick(fire_missile)

our_missiles = []
enemy_missiles = []

while True:
    window.update()
    dead_missiles = []

    if len(enemy_missiles) < ENEMY_COUNT:
        fire_enemy_missile()

    move_missile(our_missiles)
    move_missile(enemy_missiles)

    for dead in dead_missiles:
        our_missiles.remove(dead) if dead in our_missiles else enemy_missiles.remove(dead)
