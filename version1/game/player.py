import pyglet
import math
from pyglet.window import key
from . import physicalobject, resources, load, util
from numpy import e


class Player(physicalobject.PhysicalObject):

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        self.thrust = 200.0
        self.max_vel = 500
        self.rotate_speed = 100.0
        self.key_handler = key.KeyStateHandler()
        self.num_lives = 3
        self.score = 0
        self.friction = 100
        self.restart = False
        self.actions = [False, False, False, False]
        self.distances = []
        self.collision = 0
        self.rotation = 270

    def sight(self):
        verts = []
        for i in range(8):
            angle = math.radians((float(i)/8 * 360.0) - self.rotation)
            x = 400*math.cos(angle) + self.x
            y = 400*math.sin(angle) + self.y
            verts += [self.x, self.y, x, y]
        return pyglet.graphics.vertex_list(16, ('v2f', verts)), verts

    def update(self, dt):
        super(Player, self).update(dt)
        angle_radians = -math.radians(self.rotation)
        # if self.key_handler[key.LEFT]:
        #     self.rotation -= self.rotate_speed * dt
        # if self.key_handler[key.RIGHT]:
        #     self.rotation += self.rotate_speed * dt
        # if self.key_handler[key.UP]:
        #     force_x = math.cos(angle_radians) * self.thrust * dt
        #     force_y = math.sin(angle_radians) * self.thrust * dt

        if self.actions[0]:
            self.rotation -= self.rotate_speed * dt
        if self.actions[1]:
            self.rotation += self.rotate_speed * dt
        if self.actions[2]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt

        else:
            force_x, force_y = 0, 0

        self.velocity_x += force_x
        self.velocity_y += force_y

        if self.velocity_y >= self.max_vel or self.velocity_y <= -self.max_vel:
            self.velocity_y = self.max_vel*self.velocity_y/abs(self.velocity_y)

        if self.velocity_x >= self.max_vel or self.velocity_x <= -self.max_vel:
            self.velocity_x = self.max_vel*self.velocity_x/abs(self.velocity_x)

        self.velocity_x -= (self.friction * self.velocity_x/(abs(self.velocity_x)+1))*dt

        self.velocity_y -= (self.friction * self.velocity_y/(abs(self.velocity_y)+1))*dt

    def on_key_press(self, symbol, modifiers):
        if symbol == key.R:
            self.restart = True

    def handle_collision_with(self, other_object):
        super(Player, self).handle_collision_with(other_object)
        if self.dead and len(self.lives) > 1:
            self.dead = False
            self.lives[-1].delete()
            self.lives = self.lives[0:-1]
            self.x, self.y = 400, 300
            self.velocity_x, self.velocity_y = 0.0, 0.0
            self.rotation = 270.0
        else:
            self.lives = None
