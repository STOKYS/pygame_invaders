import pygame
import math


class Game:
    def __init__(self):
        self.started = False
        self.player = Player()


class Player:
    def __init__(self):
        self.position = [500, 800]
        self.rotation = 0
        self.shells = False

    def fnc_rotation(self, surface, offset):
        global img_player_cannon_deg, pivot, mouse_pos
        self.fnc_calculate_deg(mouse_pos)
        if mouse_pos[0] > 500:
            rotated_image = pygame.transform.rotozoom(surface, self.rotation, 1)
        else:
            rotated_image = pygame.transform.rotozoom(surface, -self.rotation, 1)
        rotated_offset = offset.rotate(self.rotation)
        rect = rotated_image.get_rect(center=self.position + rotated_offset)
        return rotated_image, rect

    def fnc_calculate_deg(self, mouse):
        mouse = list(mouse)
        side_c = math.sqrt(math.pow((self.position[0] - mouse[0]), 2) + (math.pow((self.position[1] - mouse[1]), 2)))
        deg = math.degrees(math.asin((self.position[1] - mouse[1]) / side_c))
        self.rotation = (deg - 90)

    def shoot(self):
        self.shells = Shell(self.position, self.rotation)
        print("Shots fired")


class Shell:
    def __init__(self, position, rotation):
        global mouse_pos
        if mouse_pos[0] > 500:
            self.rotation = 90 + (-rotation)
        else:
            self.rotation = 90 - (-rotation)
        __side_y = 78 * math.sin(math.radians(self.rotation))
        __side_x = 78 * math.cos(math.radians(self.rotation))
        self.position = [position[0] - __side_x, position[1] - __side_y]


pygame.init()
game = Game()
pygame.display.set_caption("Invaders")
screen = pygame.display.set_mode([1000, 1000])

clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

img_player_cannon = pygame.image.load('media/images/player/cannon.png')
img_player_turret_bg = pygame.image.load('media/images/player/turret_bg.png')
img_player_turret_fg = pygame.image.load('media/images/player/turret_fg.png')
img_player_cross = pygame.image.load('media/images/player/cross.png')

running = True

while running:

    mouse_pos = list(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.player.shoot()

    screen.fill((20, 20, 20))

    img_player_cannon_deg, pivot = game.player.fnc_rotation(img_player_cannon, pygame.math.Vector2(0, 0))

    screen.blit(img_player_turret_bg, (410, 780))
    screen.blit(img_player_cannon_deg, pivot)
    screen.blit(img_player_turret_fg, (410, 780))
    screen.blit(img_player_cross, (mouse_pos[0] - 16, mouse_pos[1] - 16))

    pygame.draw.line(screen, (255, 255, 255), game.player.position, mouse_pos)
    if game.player.shells:
        pygame.draw.circle(screen, (255, 255, 255), game.player.shells.position, 5)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
