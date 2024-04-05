from vectors import *
import pygame as p
import sys
from classy import *

window_bounds = WIDTH, HEIGHT, scale = 600, 600, 50
screen = p.display.set_mode((WIDTH, HEIGHT))
playfield = Playfield(3, 6, Vec(1.5, 5.5), Vec(1.5, 0.2), obstacles=[Moat(Vec(0, 4.2), .8, .2), Moat(Vec(1, 4.2), 2, .2)])
origin = x0, y0 = (WIDTH / 2) - playfield.width / 2 * scale, (
            HEIGHT - HEIGHT / 2) + playfield.height / 2 * scale  # This is the new origin
playfield_rect = p.Rect(x0, y0 - playfield.height * scale, playfield.width * scale, playfield.height * scale)
p.font.init()
font = p.font.SysFont('Monocraft', 20)


def ball_xy(pos):
    return origin[0] + pos.x * scale, origin[1] - pos.y * scale


def pygame_init():
    # Screen or whatever you want to call it is your best friend - it's a canvas
    # or surface where you can draw - generally you'll have one large canvas and
    # additional surfaces on top - effectively breaking things up and giving
    # you the ability to have multiples scenes in one window
    p.init()
    screen.fill((180, 210, 255))
    p.display.set_caption('Fireworks')


def drawer(object_list, place_to_draw_stuff=screen):
    for i in object_list:
        p.draw.circle(place_to_draw_stuff, i.color.color(), ball_xy(i.pos), 1)


def make_display(text, top_left, text_color=(255, 255, 255), bg_color=None):
    display = font.render(text, True, text_color, bg_color)
    display_rect = display.get_rect()
    display_rect.topleft = top_left
    return display, display_rect


def draw_text(text, top_left=(0, 0), text_color=(255, 255, 255), bg_color=None):
    display, display_rect = make_display(text, (0, 0), text_color=text_color, bg_color=bg_color)
    display_rect.topleft = top_left
    screen.blit(display, display_rect)


def draw_more_text(texts: list, top_left=Vec(), text_color=(255,255,255), bg_color=None):
    for x in texts:
        draw_text(x, (top_left + Vec(0, 20) * texts.index(x)).tuple(2), text_color, bg_color)


main = [Population(64, .5, Ball(playfield, 45, Vec(0, .2), speed=1))]

running = False
while True:
    # keystroke example
    for event in p.event.get():

        if event.type == p.QUIT:  # this refers to clicking on the "x"-close
            p.quit()
            sys.exit()

        elif event.type == p.KEYDOWN:  # there's a separate system built in
            # for multiple key presses or presses
            # that result in changes of state - tba
            if event.key == p.K_g:
                print("n")

            if event.key == p.K_a:
                print("goodbye")

            if event.key == p.K_SPACE:
                if running is False:
                    running = True
                    print("START")
                elif running is True:
                    running = False
                    print("PAUSE")

            if event.key == p.K_RETURN :
                print(main[0].best_score)

    if running:
        # background

        for x in range(20):
            for x in main:
                if x.step():
                    screen.fill((150, 210, 255))
                    p.draw.rect(screen, (166, 203, 164), playfield_rect)
                    for z in playfield.obstacles:
                        if isinstance(z, Moat):
                            p.draw.rect(screen, (0, 0, 200),  p.Rect(x0 + z.topleft.x * scale, y0 - z.topleft.y * scale, z.width * scale, z.height * scale))
                drawer(x.population)
        p.draw.circle(screen, (255, 255, 255), ball_xy(playfield.holexy), playfield.hole_r * scale)
        draw_more_text([f"Randomness: {main[0].randomness}",
                        f"Average Score: {main[0].average_score}",
                        f"Best Score: {main[0].best_score.success}",
                        f"Best Angle: {main[0].best_score.angle}",
                        f"SPEED: {round(mag(main[0].population[0].v), 2)}"], bg_color=(150, 210, 255))
        p.display.flip()

    # This sets an upper limit on the frame rate (here 100 frames per second)
    # often you won't be able
    p.time.Clock().tick()
