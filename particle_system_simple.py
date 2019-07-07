import tcod as libtcod
import random
import time

screen_width = 80
screen_height = 50
window_title = "A Particle System"
max_particle_moves = 100
particles_per_update = 2

red_lt = libtcod.Color(251,73,52) #gruvbox lt red

class Particle:
    def __init__(self, x, y, vx, vy, colour):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colour = colour
        self.moves = 0

    def is_dead(self):
        if self.moves > max_particle_moves:
            return True
        else:
            return False

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.moves += 1

    def draw(self):
        libtcod.console_set_char_background(
            0,
            self.x,
            self.y,
            self.colour,
            libtcod.BKGND_SET
        )


class ParticleSystem:
    def __init__(self, x, y):
        self.origin = x, y
        self.particles = []

    def update(self):
        x, y = self.origin

        for p in self.particles:
            p.move()
            if p.is_dead():
                self.particles.remove(p)

    def add_particles(self, number):
        for i in range(0, number):
            vx = random.randint(-2, 2)
            vy = random.randint(-2, 2)
            p = Particle(self.origin[0], self.origin[1], vx, vy, red_lt)
            self.particles.append(p)


    def draw(self):
        for p in self.particles:
            p.draw()


def main():

    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    libtcod.console_init_root(
        screen_width,
        screen_height,
        window_title,
        False,
    )

    ps = ParticleSystem(20, 20)

    while not libtcod.console_is_window_closed():
        libtcod.console_clear(0)
        ps.draw()
        ps.update()
        ps.add_particles(particles_per_update)
        time.sleep(.1)
        libtcod.console_flush()
        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_ESCAPE: break


if __name__ == "__main__":
    main()
