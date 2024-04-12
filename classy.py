import math

from constantinopal import *
from vectors import *


class HillValley:
    def __init__(self, x_y, hill:bool = True):
        self.pos = x_y
        self.mult = 1 if hill else -1

    def check(self, input_position):
        distance = mag(self.pos-input_position)
        if distance < 1:
            if distance < 0.5:
                force_multiplier = 0.2 * distance
            else:
                force_multiplier = 0.05/distance
            return norm(input_position - self.pos) * force_multiplier * self.mult
        return Vec()

class Moat:
    def __init__(self, topleft, width, height):
        self.topleft = topleft
        self.width = width
        self.height = height

    def check(self, initposition):
        if self.topleft.x < initposition.x < self.topleft.x + self.width and self.topleft.y - self.height < initposition.y < self.topleft.y:
            return "Fail"
        else:
            return Vec()


class Wall:
    def __init__(self, p1, p2, vertical):
        self.vertical = vertical
        self.p1 = p1
        self.p2 = p2
        self.x = p1.x
        self.y = p1.y


class Playfield:
    def __init__(self, width, height, holexy: Vec, startpos: Vec, hole_r: int = 0.05, obstacles = [], walls = []):
        self.height = height
        self.width = width
        self.holexy = holexy
        self.startpos = startpos
        self.hole_r = hole_r
        self.obstacles = obstacles
        self.walls = walls

class Ball:
    def __init__(self, playfield: Playfield, angle: float, startpos:Vec = Vec(), speed: int = 10, color: Vec = None, wind: Vec = Vec()):
        self.playfield = playfield
        self.pos = playfield.startpos
        self.pos_init = playfield.startpos
        self.speed = speed
        self.v = vectorize(speed, angle)
        self.a = Vec()
        self.forces = [norm(self.v) * friction]
        self.angle = angle
        self.m = 0.045
        self.success = None
        if color is None:
            self.color = (randvec()*255).__abs__()
        else:
            self.color = color
        self.r = 0.021335
        self.wind = wind

    def bounce_off_wall(self, wall_norm):
        self.v -= rotate(2 * dot(self.v, wall_norm) * wall_norm, random.gauss(0, wall_randomness))

    def in_hole(self):
        return -0.03125 * mag(self.v) + self.playfield.hole_r >= mag(self.pos - self.playfield.holexy)

    def step(self):
        if self.success is not True:
            for w in self.playfield.walls:
                if w.vertical:
                    if self.pos.x < w.x < self.pos.x + self.v.x * dt and w.p1.y < self.pos.y < w.p2.y:
                        self.bounce_off_wall(Vec(-1, 0))
                    elif self.pos.x > w.x > self.pos.x + self.v.x * dt and w.p1.y < self.pos.y < w.p2.y:
                        self.bounce_off_wall(Vec(1, 0))
                else:
                    if self.pos.y < w.y < self.pos.y + self.v.y * dt and w.p1.x < self.pos.x < w.p2.x:
                        self.bounce_off_wall(Vec(0, -1))
                    elif self.pos.y > w.y > self.pos.y + self.v.y * dt and w.p1.x < self.pos.x < w.p2.x:
                        self.bounce_off_wall(Vec(0, 1))
            self.pos += self.v * dt
            if self.pos.x > self.playfield.width:
                self.pos -= self.v * dt
                self.bounce_off_wall(Vec(-1, 0))
            elif self.pos.x < 0:
                self.pos -= self.v * dt
                self.bounce_off_wall(Vec(1, 0))
            if self.pos.y > self.playfield.height:
                self.pos -= self.v * dt
                self.bounce_off_wall(Vec(0, -1))
            elif self.pos.y < 0:
                self.pos -= self.v * dt
                self.bounce_off_wall(Vec(0, 1))
            self.v += self.a * dt
            self.a = sum(self.forces, Vec())/self.m
            self.forces = [norm(self.v) * friction]
            for x in self.playfield.obstacles:
                if x.check(self.pos) == "Fail":
                    self.v = Vec()
                else:
                    self.forces.append(x.check(self.pos))
            if self.in_hole():
                print("SUCCESS")
                self.success = 0
            if mag(self.v) <= 0.01:
                self.success = mag(self.pos - self.playfield.holexy)

    def varied_copy(self, randomness):
        new_angle = random.gauss(self.angle, randomness)
        new_speed = random.gauss(self.speed, randomness)
        new_color = ((self.angle - new_angle)/360 + (self.speed - new_speed)/self.speed)/2 * self.color + self.color
        return Ball(self.playfield, new_angle, self.pos_init, new_speed,
                    color=new_color)

    def __repr__(self):
        return f"Ball with angle: {self.angle}, Speed: {self.speed}, Velocity {vectorize(self.speed, self.angle)}"


class Population:
    def __init__(self, popsize, randomness, defaultball: Ball, survival_rate = 10):
        self.population = [Ball(defaultball.playfield, random.uniform(0, 360), defaultball.pos,
                                mag(defaultball.v) + random.uniform(-mag(defaultball.v), mag(defaultball.v))) for i in range(popsize)]
        self.randomness = randomness
        self.average_score = 0
        self.best_score = defaultball

    def all_landed(self):
        for ball in self.population:
            if ball.success is None:
                return False
        return True

    def reproduction(self):
        new_pop = []
        self.average_score = sum([x.success for x in self.population])/len(self.population)
        self.population = sorted(self.population, key = lambda x: x.success)
        self.best_score = self.population[0]
        for x in self.population[0:int(math.sqrt(len(self.population)))]:
            for xx in range(int(math.sqrt(len(self.population)))):
                new_pop.append(x.varied_copy(self.randomness))
        self.population = new_pop
        del new_pop

    def step(self):
        for ball in self.population:
            ball.step()
        if self.all_landed():
            self.reproduction()
            self.randomness *= .7
            return True
        else:
            return False

class Ecosystem:
    def __init__(self, number_of_families, default_family):
        self.x = number_of_families




