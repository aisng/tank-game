import math

import pygame
import os
import time
from random import randint

pygame.font.init()

WIN_WIDTH, WIN_HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Tank game")

SPRITE_WIDTH, SPRITE_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 30, 30

# Load images
TANK_NORTH = pygame.image.load(os.path.join('assets', 'tank-north.png'))
TANK_NORTH = pygame.transform.scale(TANK_NORTH, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_SOUTH = pygame.image.load(os.path.join('assets', 'tank-south.png'))
TANK_SOUTH = pygame.transform.scale(TANK_SOUTH, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_EAST = pygame.image.load(os.path.join('assets', 'tank-east.png'))
TANK_EAST = pygame.transform.scale(TANK_EAST, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_WEST = pygame.image.load(os.path.join('assets', 'tank-west.png'))
TANK_WEST = pygame.transform.scale(TANK_WEST, (SPRITE_WIDTH, SPRITE_HEIGHT))

BULLET_NORTH = pygame.image.load(os.path.join('assets', 'bullet-north.png'))
BULLET_NORTH = pygame.transform.scale(BULLET_NORTH, (BULLET_WIDTH, BULLET_HEIGHT))

BULLET_EAST = pygame.image.load(os.path.join('assets', 'bullet-east.png'))
BULLET_EAST = pygame.transform.scale(BULLET_EAST, (BULLET_WIDTH, BULLET_HEIGHT))

BULLET_SOUTH = pygame.image.load(os.path.join('assets', 'bullet-south.png'))
BULLET_SOUTH = pygame.transform.scale(BULLET_SOUTH, (BULLET_WIDTH, BULLET_HEIGHT))

BULLET_WEST = pygame.image.load(os.path.join('assets', 'bullet-west.png'))
BULLET_WEST = pygame.transform.scale(BULLET_WEST, (BULLET_WIDTH, BULLET_HEIGHT))

ENEMY = pygame.image.load(os.path.join('assets', 'enemy.png'))
ENEMY = pygame.transform.scale(ENEMY, (SPRITE_WIDTH, SPRITE_HEIGHT))

EXPLOSION = pygame.image.load(os.path.join('assets', 'explosion.png'))
EXPLOSION = pygame.transform.scale(EXPLOSION, (SPRITE_WIDTH, SPRITE_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Projectile:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.vel = 8
        self.direction = direction
        self.image = BULLET_NORTH
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.x += self.direction[0] * self.vel
        self.y += self.direction[1] * self.vel

    def draw(self, window):
        if self.direction == (1, 0):  # east
            window.blit(BULLET_EAST, (self.x, self.y))
        elif self.direction == (0, 1):  # south
            window.blit(BULLET_SOUTH, (self.x, self.y))
        elif self.direction == (-1, 0):  # west
            window.blit(BULLET_WEST, (self.x, self.y))
        else:  # north
            window.blit(self.image, (self.x, self.y))

    def collision(self, obj):
        return collide(self, obj)


class Tank:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = False
        self.east = False
        self.south = False
        self.west = False
        self.image = TANK_NORTH
        self.vel = 5
        self.bullets = []
        self.bullet_direction = (0, -1)
        self.bullet_cooldown = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0
        self.destroyed = False

    def draw(self, window):
        if self.east:
            window.blit(TANK_EAST, (self.x, self.y))
        elif self.south:
            window.blit(TANK_SOUTH, (self.x, self.y))
        elif self.west:
            window.blit(TANK_WEST, (self.x, self.y))
        else:
            window.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)
        if self.destroyed:
            window.blit(EXPLOSION, (self.x, self.y))

    def shoot(self):
        self.cooldown()
        if self.bullet_cooldown == 0:

        # if len(self.bullets) < 4:
            # center the bullet img on the tank
            tank_center_x, tank_center_y = round(self.x + self.get_width() / 2), round(self.y + self.get_height() / 2)
            bullet_center_x, bullet_center_y = round(tank_center_x - BULLET_WIDTH / 2), round(
                tank_center_y - BULLET_HEIGHT / 2)
            # make bullets appear as being shot from tank's cannon
            if self.east:
                bullet_center_x += 40
            elif self.south:
                bullet_center_y += 40
            elif self.west:
                bullet_center_x -= 40
            else:
                bullet_center_y -= 40
            bullet = Projectile(bullet_center_x, bullet_center_y, self.bullet_direction)
            self.bullet_cooldown = 1
            self.bullets.append(bullet)

    def cooldown(self):
        if self.bullet_cooldown >= self.COOLDOWN:
            self.bullet_cooldown = 0
        elif self.bullet_cooldown > 0:
            self.bullet_cooldown += 1

    def move_bullets(self, objs):
        self.cooldown()
        win_rect = pygame.Rect(0, 0, WIN_WIDTH, WIN_HEIGHT)
        for bullet in self.bullets:
            bullet.move()
            if not win_rect.collidepoint((bullet.x, bullet.y)):  # making bullet disappear if off-screen
                self.bullets.remove(bullet)
            else:  # remove bullet obj and enemy obj if they collide
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        self.score += 10
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def move_north(self):
        self.y -= self.vel
        self.north = True
        self.east, self.south, self.west = False, False, False
        self.bullet_direction = (0, -1)

    def move_east(self):
        self.x += self.vel
        self.east = True
        self.north, self.south, self.west = False, False, False
        self.bullet_direction = (1, 0)

    def move_south(self):
        self.y += self.vel
        self.south = True
        self.east, self.west, self.north = False, False, False
        self.bullet_direction = (0, 1)

    def move_west(self):
        self.x -= self.vel
        self.west = True
        self.north, self.east, self.south = False, False, False
        self.bullet_direction = (-1, 0)

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = ENEMY
        self.vel = 1
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def chase_tank(self, tank):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = tank.x - self.x, tank.y - self.y
        distance = math.hypot(dx, dy)
        dx, dy = dx / distance, dy / distance  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.x += dx * self.vel
        self.y += dy * self.vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 40)

    starting_pos_x = round(WIN_WIDTH - WIN_WIDTH / 2) - round(SPRITE_WIDTH - SPRITE_WIDTH / 2)
    starting_pos_y = round(WIN_HEIGHT - WIN_HEIGHT / 2) - round(SPRITE_HEIGHT - SPRITE_HEIGHT / 2)
    tank = Tank(starting_pos_x, starting_pos_y)

    enemies = []
    wave_length = 0

    clock = pygame.time.Clock()
    lost = False
    lost_count = 0

    def redraw_window():
        WIN.fill(WHITE)
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", True, BLACK)
        level_label = main_font.render(f"Level: {level}", True, BLACK)
        score_label = main_font.render(f"Score: {tank.score}", True, BLACK)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIN_WIDTH - level_label.get_width() - 10, 10))
        WIN.blit(score_label,
                 ((WIN_WIDTH - WIN_WIDTH / 2) - (score_label.get_width() - score_label.get_width() / 2), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        tank.draw(WIN)

        if lost:
            tank.destroyed = True
            lost_label = lost_font.render(f"You lost! Score: {tank.score}", True, BLACK)
            WIN.blit(lost_label,
                     (WIN_WIDTH / 2 - lost_label.get_width() / 2, WIN_HEIGHT / 2 - lost_label.get_height() / 2))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if lives <= 0:
            lost = True
            lost_count += 1

        # show lost label for 3 seconds
        if lost:

            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 1
            for i in range(wave_length):
                enemy = Enemy(randint(10, WIN_WIDTH - 10), randint(10, WIN_HEIGHT - 10))
                enemies.append(enemy)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and tank.y - tank.vel > 0:
            tank.move_north()
        elif keys[pygame.K_RIGHT] and tank.x + tank.vel + tank.get_width() < WIN_WIDTH:
            tank.move_east()
        elif keys[pygame.K_DOWN] and tank.y + tank.vel + tank.get_height() < WIN_HEIGHT:
            tank.move_south()
        elif keys[pygame.K_LEFT] and tank.x - tank.vel > 0:
            tank.move_west()
        if keys[pygame.K_SPACE]:
            tank.shoot()

        for enemy in enemies:
            enemy.chase_tank(tank)
            if collide(enemy, tank):
                lives -= 1
                enemies.pop(enemies.index(enemy))
        tank.move_bullets(enemies)



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.fill(WHITE)
        title_label = title_font.render("Press Enter to begin...", 1, BLACK)
        WIN.blit(title_label,
                 (WIN_WIDTH / 2 - title_label.get_width() / 2, WIN_HEIGHT / 2 - title_label.get_height() / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main()


main_menu()
