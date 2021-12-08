import pygame
import math
import random
import datetime


class Game:
    def __init__(self):
        self.started = False
        self.player = Player()
        self.enemies = [Bomb()]
        self.timer = datetime.datetime.now().timestamp()
        self.delay = 3000

    def fnc_update(self):
        self.player.fnc_update()
        self.fnc_draw()
        if datetime.datetime.now().timestamp() >= self.timer + self.delay / 1000:
            self.timer = datetime.datetime.now().timestamp()
            if self.delay > self.player.reload:
                self.delay -= 10
            self.fnc_create_enemy()
            print(self.delay)

    def fnc_create_enemy(self):
        self.enemies.append(Bomb())

    def fnc_draw(self):
        screen.blit(img_player_turret_bg, (0, 800))
        screen.blit(img_player_char_charles, (0, 800))
        screen.blit(img_player_cannon_deg, pivot)
        screen.blit(img_player_char_george, (0, 800))
        screen.blit(img_player_turret_fg, (0, 800))
        screen.blit(img_player_char_harry, (0, 800))
        screen.blit(img_player_cross, (mouse_pos[0] - 16, mouse_pos[1] - 16))
        if self.player.shells:
            for i in self.player.shells:
                i.fnc_update()
                pygame.draw.circle(screen, (255, 255, 255), i.position, 5)
        if self.enemies:
            buffer = []
            for j in range(len(self.enemies)):
                if self.enemies[j].position[1] >= 960:
                    buffer.append(j)
                self.enemies[j].fnc_update()
                screen.blit(img_enemy_bomb, self.enemies[j].position)
            for i in range(len(buffer)):
                self.player.health -= 1
                del self.enemies[buffer[i]]
        if self.enemies and self.player.shells:
            shell_buffer = []
            bomb_buffer = []
            for i in range(len(self.player.shells)):
                for j in range(len(self.enemies)):
                    if fnc_collision(self.player.shells[i].position, self.enemies[j].position):
                        shell_buffer.append(i)
                        bomb_buffer.append(j)
                        self.player.score += 10
            for i in range(len(shell_buffer)):
                del self.player.shells[shell_buffer[i]]
                del self.enemies[bomb_buffer[i]]
        pygame.draw.rect(screen, (255, 0, 0), (450, 920, 100, 5))
        pygame.draw.rect(screen, (0, 255, 0), (450, 920, ((pygame.time.get_ticks() - self.player.reload) / 20) if self.player.reload + 2000 > pygame.time.get_ticks() else 100, 5))
        pygame.draw.rect(screen, (255, 0, 0), (200, 980, 600, 10))
        pygame.draw.rect(screen, (0, 255, 0), (200, 980, self.player.health * 6, 10))
        screen.blit(f_score.render(f'Score: {self.player.score}', True, (200, 200, 200)), (0, 0))
        screen.blit(f_health.render(f'Health: {self.player.health}%', True, (20, 20, 20)), (450, 978))


class Player:
    def __init__(self):
        self.position = [500, 855]
        self.rotation = 0
        self.shells = []
        self.reload = pygame.time.get_ticks()
        self.score = 0
        self.health = 100

    def fnc_update(self):
        global img_player_cannon_deg, pivot
        img_player_cannon_deg, pivot = self.fnc_rotation(img_player_cannon, pygame.math.Vector2(0, 0))

    def fnc_rotation(self, surface, offset):
        global img_player_cannon_deg, pivot, mouse_pos
        self.fnc_calculate_deg(mouse_pos)
        if self.rotation < -90:
            self.rotation = -90
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
        if side_c:
            deg = math.degrees(math.asin((self.position[1] - mouse[1]) / side_c))
            self.rotation = (deg - 90)

    def fnc_shoot(self):
        if self.reload + 2000 < pygame.time.get_ticks():
            self.reload = pygame.time.get_ticks()
            self.shells.append(Shell(self.position, self.rotation, 20))


class Shell:
    def __init__(self, position, rotation, force):
        global mouse_pos
        if mouse_pos[0] > 500:
            self.rotation = 90 + (-rotation)
        else:
            self.rotation = 90 - (-rotation)
        self.position = [position[0] - (120 * math.cos(math.radians(self.rotation))), position[1] - (120 * math.sin(math.radians(self.rotation)))]
        self.force = force
        self.timer = pygame.time.get_ticks()

    def fnc_update(self):
        if (self.timer + 1500) > (pygame.time.get_ticks()):
            self.fnc_move()
        else:
            del game.player.shells[0]

    def fnc_move(self):
        self.position = [self.position[0] - self.force * math.cos(math.radians(self.rotation)), self.position[1] - self.force * math.sin(math.radians(self.rotation))]


class Bomb:
    def __init__(self):
        self.position = [random.randrange(900) + 50, -50]

    def fnc_update(self):
        self.fnc_move()

    def fnc_move(self):
        self.position = [self.position[0], self.position[1] + 3]


def fnc_collision(shell, bomb):
    __bomb_xy = [bomb[0], bomb[0] + 18, bomb[1], bomb[1] + 40]
    __shell_xy = [shell[0] - 5, shell[0] + 5, shell[1] - 5, shell[1] + 5]
    if (__bomb_xy[3] < __shell_xy[2]) or (__bomb_xy[2] > __shell_xy[3]) or (__bomb_xy[1] < __shell_xy[0]) or (__bomb_xy[0] > __shell_xy[1]):
        return False
    else:
        return True


pygame.init()
pygame.font.init()
game = Game()
pygame.display.set_caption("Invaders")
screen = pygame.display.set_mode([1000, 1000])

clock = pygame.time.Clock()
f_score = pygame.font.Font(None, 30)
f_health = pygame.font.Font(None, 20)
f_reload = pygame.font.Font(None, 10)
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

img_player_cannon = pygame.image.load('media/images/player/cannon2.png')
img_player_turret_bg = pygame.image.load('media/images/player/turret_bg.png')
img_player_turret_fg = pygame.image.load('media/images/player/turret_fg.png')
img_player_char_harry = pygame.image.load('media/images/player/col_harry.png')
img_player_char_george = pygame.image.load('media/images/player/cpt_george.png')
img_player_char_charles = pygame.image.load('media/images/player/lt_charles.png')
img_player_cross = pygame.image.load('media/images/player/cross.png')
img_enemy_bomb = pygame.image.load('media/images/enemy/bomb.png')

running = True

start_time = datetime.datetime.now().timestamp()

while running:

    mouse_pos = list(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.player.fnc_shoot()

    screen.fill((20, 20, 20))

    game.fnc_update()

    pygame.display.flip()
    clock.tick(144)

pygame.quit()
