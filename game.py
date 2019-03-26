import math
import turtle

window = turtle.Screen()
window.setup(1200 + 3, 800 + 3, starty=0)
window.bgpic("images/background.png")
window.screensize(1200, 800)
# window.tracer(n=2)

BASE_X, BASE_Y = 0, -300


def calc_heading(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    length = (dx ** 2 + dy ** 2) ** 0.5
    cos_alpha = dx / length
    alpha = math.degrees(math.acos(cos_alpha))
    if dy < 0:
        alpha = -alpha
    return alpha


def fire_missile(x, y):
    heading = calc_heading(x1=BASE_X, y1=BASE_Y, x2=x, y2=y)

    if 0 < heading < 180:
        new_missile = turtle.Turtle(visible=False)
        new_missile.speed(0)
        new_missile.color('white')
        new_missile.penup()
        new_missile.setpos(x=BASE_X, y=BASE_Y)
        new_missile.pendown()
        new_missile.setheading(heading)
        new_missile.showturtle()

        missiles_info = {'missile': new_missile, 'target': [x, y],
                         'state': 'launched', 'radius': 0}
        our_missiles.append(missiles_info)


window.onclick(fire_missile)

our_missiles = []

while True:
    window.update()

    for missile_info in our_missiles:
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
            else:
                missile.shapesize(missile_info['radius'])

    dead_missiles = [info for info in our_missiles if info['state'] == 'dead']
    for dead in dead_missiles:
        our_missiles.remove(dead)

# TODO Вражеские ракеты появляются в рандоме (рандомный x и задержка)
#  и летят к базе
