import pygame
import os
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank game")

SPRITE_WIDTH, SPRITE_HEIGHT = 50, 50
BULLET_WIDTH, BULLET_HEIGHT = 1, 1

# Load images
TANK_NORTH = pygame.image.load(os.path.join('assets', 'tank-north.png'))
TANK_NORTH = pygame.transform.scale(TANK_NORTH, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_SOUTH = pygame.image.load(os.path.join('assets', 'tank-south.png'))
TANK_SOUTH = pygame.transform.scale(TANK_SOUTH, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_EAST = pygame.image.load(os.path.join('assets', 'tank-east.png'))
TANK_EAST = pygame.transform.scale(TANK_EAST, (SPRITE_WIDTH, SPRITE_HEIGHT))

TANK_WEST = pygame.image.load(os.path.join('assets', 'tank-west.png'))
TANK_WEST = pygame.transform.scale(TANK_WEST, (SPRITE_WIDTH, SPRITE_HEIGHT))

BULLET = pygame.image.load(os.path.join('assets', 'bullet.png'))
BULLET = pygame.transform.scale(BULLET, (BULLET_WIDTH, BULLET_HEIGHT))

ENEMY = pygame.image.load(os.path.join('assets', 'enemy.png'))
ENEMY = pygame.transform.scale(ENEMY, (SPRITE_WIDTH, SPRITE_HEIGHT))

EXPLOSION = pygame.image.load(os.path.join('assets', 'explosion.png'))
EXPLOSION = pygame.transform.scale(EXPLOSION, (SPRITE_WIDTH - 10, SPRITE_HEIGHT - 10))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Projectile:
    def __init__(self, x, y,  direction):
        self.x = x
        self.y = y
        # self.radius = radius
        # self.color = color
        self.vel = 8
        self.direction = direction
        self.image = BULLET

    def move(self):
        self.x += self.direction[0] * self.vel
        self.y += self.direction[1] * self.vel

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        # pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)


class Tank:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.north = False
        self.east = False
        self.south = False
        self.west = False
        self.image = TANK_NORTH
        self.max_health = health
        self.vel = 5
        self.bullets = []

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

    # region experiment TODO: add objs param for collision
    def move_bullets(self, direction):
        for bullet in self.bullets:
            bullet.move()
            win_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
            if not win_rect.collidepoint((bullet.x, bullet.y)):
                self.bullets.pop(self.bullets.index(bullet))

    def shoot(self):
        bullet = Projectile(self.x, self.y, (0, -1))
        self.bullets.append(bullet)

    # endregion
    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 25)

    player_vel = 5
    tank = Tank(300, 200)
    bullets = []

    direction = (0, -1)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.fill(WHITE)
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", True, (0, 0, 0))
        level_label = main_font.render(f"Level: {level}", True, (0, 0, 0))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # for bullet in bullets:
        #     bullet.draw(WIN)

        tank.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # for bullet in bullets:
        #     bullet.move()
        #     win_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        #     if not win_rect.collidepoint((bullet.x, bullet.y)):
        #         bullets.pop(bullets.index(bullet))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and tank.y - tank.vel > 0:
            tank.y -= tank.vel
            tank.north = True
            tank.east, tank.south, tank.west = False, False, False
            direction = (0, -1)
            # tank.move_bullets(direction)
        elif keys[pygame.K_RIGHT] and tank.x + tank.vel + tank.get_width() < WIDTH:
            tank.x += tank.vel
            tank.east = True
            tank.north, tank.south, tank.west = False, False, False
            direction = (1, 0)
        elif keys[pygame.K_DOWN] and tank.y + player_vel + tank.get_height() < HEIGHT:
            tank.y += tank.vel
            tank.south = True
            tank.north, tank.east, tank.west = False, False, False
            direction = (0, 1)
        elif keys[pygame.K_LEFT] and tank.x - tank.vel > 0:
            tank.x -= tank.vel
            tank.west = True
            tank.north, tank.east, tank.south = False, False, False
            direction = (-1, 0)
        if keys[pygame.K_SPACE]:
            tank.shoot()
            # if len(bullets) < 5:
            #     tank_x, tank_y = round(tank.x + tank.get_width() // 2), round(tank.y + tank.get_height() // 2)
            #     bullet = Projectile(tank_x, tank_y, 6, (0, 0, 0), direction)
            #     bullets.append(bullet)
            tank.move_bullets(direction)
        redraw_window()


main()
