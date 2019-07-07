import tcod as libtcod
import random
import time

bg = libtcod.Color(40, 40, 40)  # gruvbox bg
red_dk = libtcod.Color(204, 36, 29)  # gruvbox dk red
red_lt = libtcod.Color(251, 73, 52)  # gruvbox lt red

colours_to_map = (
    libtcod.Color(204, 36, 29),
    libtcod.Color(254, 128, 25),
    libtcod.Color(214, 93, 14),
)
idx = [0, 4, 8]
map = libtcod.color_gen_map(colours_to_map, idx)

screen_width = 80
screen_height = 50
window_title = "A Particle System"
particles_per_update = 80
max_particle_moves = 3


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
        if random.randint(0, 100) < 10:
            self.x += random.randint(-1, 1)

        if random.randint(0, 100) < 10:
            self.y += random.randint(-1, 1)

        self.x += self.vx
        self.y += self.vy
        # print(f"x: {self.x}, y: {self.y}")
        self.moves += 1

    def increase_velocity(self, xa, ya):
        self.vx += xa
        self.vy += ya

    def draw(self):
        libtcod.console_set_char_background(
            0, self.x, self.y, self.colour, libtcod.BKGND_SET
        )
        print(self.colour)


class ParticleSystem:
    def __init__(self, x, y):
        self.position = x, y
        self.particles = []
        self.age = 0

    def update(self):
        x, y = self.position
        for p in self.particles:
            p.move()
            if p.is_dead():
                self.particles.remove(p)
        if self.age < 4:
            for i in range(0, particles_per_update):
                vx = random.randint(-2, 2)
                vy = random.randint(-2, 2)
                p = Particle(x, y, vx, vy, map[random.randint(0, 3)])
                print(f"x: {x}, y: {y}, vx: {vx}, vy: {vy}")
                self.particles.append(p)
        print(len(self.particles))
        self.age += 1

    def draw(self):
        print(map)
        for p in self.particles:
            if p.moves > max_particle_moves / 3:
                p.colour = map[random.randint(4, 5)]
            if p.moves > max_particle_moves / 3 * 2:
                p.colour = map[random.randint(5, 8)]

            p.draw()


def main():

    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    libtcod.console_init_root(screen_width, screen_height, window_title, False)

    ps = ParticleSystem(20, 20)

    while not libtcod.console_is_window_closed():
        libtcod.console_clear(0)
        ps.draw()
        ps.update()
        time.sleep(0.1)
        libtcod.console_flush()
        # p = Particle(20, 20, 2, 2, red_dk)
        # p.draw()
        key = libtcod.console_check_for_keypress()
        if key.vk == libtcod.KEY_ESCAPE:
            break


if __name__ == "__main__":
    main()
