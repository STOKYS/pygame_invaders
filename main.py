import math
import random

import pygame
import datetime

from enemy import Bomb

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Invaders")
pygame.display.set_icon(pygame.image.load('data/media/images/icon.jpg'))

from menu import Menu
from utils import screen, FPS, fnc_write_user_data, f_fifty, SCREEN_WIDTH, SCREEN_HEIGHT, f_forty, img_player_turret_bg, \
    img_player_char_charles, img_player_char_george, img_player_turret_fg, img_player_char_harry, img_explosion, \
    img_enemy_nbomb, img_enemy_bigbomb, img_enemy_bomb, fnc_collision, f_twenty, f_thirty, img_player_cross, \
    fnc_read_user_data, img_player_cannon


class App:
    def __init__(self):
        self.running = True
        self.menu = None
        self.game = None
        self.menu_running = False
        self.game_running = False
        self.fnc_app_menu()

    def fnc_app_menu(self):
        pygame.mouse.set_visible(True)
        self.menu = Menu(self)
        self.game_running = False

    def fnc_app_game(self, level):
        pygame.mouse.set_visible(False)
        self.game = Game(self, level)
        self.menu_running = False

    def fnc_app_update(self):
        if self.menu_running:
            self.menu.fnc_menu_update()
        if self.game_running:
            self.game.fnc_game_update()


class Game:
    def __init__(self, parent, level):
        parent.game_running = True
        self.started = False
        self.player = Player()
        self.enemies = [Bomb(0, 1, 1)]
        self.timer = datetime.datetime.now().timestamp()
        self.delay = [4000, 3500, 3000, 2500, 2500, 2000]
        self.delay_s = [2500, 2000, 2000, 2000, 1500, 1000]
        self.delay_ch = [20, 20, 20, 20, 15, 15]
        self.rand = [100, 80, 50, 30, 15, 5]
        self.level = level
        pygame.display.set_caption(f"Invaders - level: {level}")

    def fnc_game_update(self):
        self.player.fnc_player_update()
        self.fnc_game_draw()
        self.fnc_game_gui()
        if datetime.datetime.now().timestamp() >= self.timer + self.delay[self.level-1] / 1000:
            self.timer = datetime.datetime.now().timestamp()
            if self.delay[self.level-1] > self.delay_s[self.level-1]:
                self.delay[self.level-1] -= self.delay_ch[self.level-1]
            self.fnc_game_create_enemy()

    def fnc_game_create_enemy(self):
        __random_e = random.randint(1, self.rand[self.level-1])
        if __random_e == 1:
            self.enemies.append(Bomb(1, 1, 5))
        elif __random_e == 2:
            self.enemies.append(Bomb(2, 1, 3))
        else:
            self.enemies.append(Bomb(0, 1, 1))

    def fnc_game_lost(self):
        __btn_lost_t = f_fifty.render("YOU LOST!", True, (200, 0, 0))
        __btn_lost_b = __btn_lost_t.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 25))
        __btn_score_t = f_forty.render(f"Score: {self.player.score}", True, (150, 0, 0))
        __btn_score_b = __btn_score_t.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 25))
        screen.blit(__btn_lost_t, __btn_lost_b)
        screen.blit(__btn_score_t, __btn_score_b)
        pygame.display.update((__btn_lost_b, __btn_score_b))
        if self.player.score > self.player.userdata.get(f"level{self.level}"):
            fnc_write_user_data(self.level, self.player.score)
        pygame.time.wait(5000)
        app.fnc_app_menu()

    def fnc_game_draw(self):
        screen.blit(img_player_turret_bg, (0, 800))
        screen.blit(img_player_char_charles, (0, 800))
        screen.blit(img_player_cannon_deg, pivot)
        screen.blit(img_player_char_george, (0, 800))
        screen.blit(img_player_turret_fg, (0, 800))
        screen.blit(img_player_char_harry, (0, 800))
        if self.player.shells:
            for i in self.player.shells:
                i.fnc_shell_update()
                pygame.draw.circle(screen, (255, 255, 255), i.position, 5)
        if self.enemies:
            buffer = []
            for j in range(len(self.enemies)):
                if self.enemies[j].position[1] >= 960:
                    buffer.append(j)
                    self.player.health -= self.enemies[j].damage
                    screen.blit(img_explosion, self.enemies[j].position)
                    if self.player.reload_streak > 0:
                        self.player.reload_streak -= 1
                self.enemies[j].fnc_bomb_update()
                if self.enemies[j].type == 1:
                    screen.blit(img_enemy_nbomb, self.enemies[j].position)
                elif self.enemies[j].type == 2:
                    screen.blit(img_enemy_bigbomb, self.enemies[j].position)
                else:
                    screen.blit(img_enemy_bomb, self.enemies[j].position)
            for i in range(len(buffer)):
                del self.enemies[buffer[i]]
        if self.enemies and self.player.shells:
            shell_buffer = []
            bomb_buffer = []
            for i in range(len(self.player.shells)):
                for j in range(len(self.enemies)):
                    if fnc_collision(self.player.shells[i].position, self.enemies[j].position):
                        self.player.reload_streak += 1
                        screen.blit(img_explosion, self.enemies[j].position)
                        shell_buffer.append(i)
                        if self.enemies[j].health == 1:
                            bomb_buffer.append(j)
                        else:
                            self.enemies[j].health -= 1
                        self.player.score += 10 * self.enemies[j].damage
            for i in range(len(shell_buffer)):
                del self.player.shells[shell_buffer[i]]
            for i in range(len(bomb_buffer)):
                del self.enemies[bomb_buffer[i]]

    def fnc_game_gui(self):
        __time_elapsed = (datetime.datetime.now().timestamp() - self.player.reload)
        __time_reload_t = ((self.player.reload_time - (self.player.reload_streak * self.player.reload_streak_multip)) / 1000)
        __time_reload = (100 / __time_reload_t)
        pygame.draw.rect(screen, (255, 0, 0), (200, 980, 600, 10))
        pygame.draw.rect(screen, (0, 255, 0), (200, 980, self.player.health * 6, 10))
        if __time_reload_t - __time_elapsed > 0:
            pygame.draw.rect(screen, (255, 0, 0), (mouse_pos[0] + 10, mouse_pos[1] + 25, 20, 5))
            pygame.draw.rect(screen, (0, 255, 0), (mouse_pos[0] + 10, mouse_pos[1] + 25, 20, 5) if __time_reload * __time_elapsed > 100 else (mouse_pos[0] + 10, mouse_pos[1] + 25, __time_elapsed * __time_reload / 5, 5))
            screen.blit(f_twenty.render(f'{round(__time_reload_t - __time_elapsed, 1)}s', True, (150, 150, 150)), (mouse_pos[0] + 10, mouse_pos[1] + 10))
        screen.blit(f_thirty.render(f'Score: {self.player.score}', True, (200, 200, 200)), (0, 0))
        screen.blit(
            f_twenty.render(f'H-Score: {self.player.userdata.get(f"level{self.level}")}', True, (200, 200, 200)), (0, 20))
        screen.blit(f_twenty.render(f'Health: {self.player.health}%', True, (20, 20, 20)), (450, 978))
        screen.blit(f_thirty.render(f'Streak: {self.player.reload_streak}', True, (200, 200, 200)), (850, 0))
        screen.blit(f_twenty.render(f'Reload time: {__time_reload_t}s', True, (200, 200, 200)), (850, 20))
        screen.blit(img_player_cross, (mouse_pos[0] - 16, mouse_pos[1] - 16))


class Player:
    def __init__(self):
        self.position = [500, 855]
        self.rotation = 0
        self.shells = []
        self.reload = datetime.datetime.now().timestamp()
        self.reload_time = 2500
        self.reload_streak_multip = 50
        self.reload_streak = 0
        self.score = 0
        self.health = 100
        self.userdata = fnc_read_user_data()

    def fnc_player_update(self):
        if self.health <= 0:
            app.game.fnc_game_lost()
        global img_player_cannon_deg, pivot
        img_player_cannon_deg, pivot = self.fnc_rotation(img_player_cannon, pygame.math.Vector2(0, 0))

    def fnc_rotation(self, surface, offset):
        global img_player_cannon_deg, pivot, mouse_pos
        self.fnc_player_deg(mouse_pos)
        if self.rotation < -90:
            self.rotation = -90
        if mouse_pos[0] > 500:
            rotated_image = pygame.transform.rotozoom(surface, self.rotation, 1)
        else:
            rotated_image = pygame.transform.rotozoom(surface, -self.rotation, 1)
        rotated_offset = offset.rotate(self.rotation)
        rect = rotated_image.get_rect(center=self.position + rotated_offset)
        return rotated_image, rect

    def fnc_player_deg(self, mouse):
        side_c = math.sqrt(math.pow((self.position[0] - mouse[0]), 2) + (math.pow((self.position[1] - mouse[1]), 2)))
        if side_c:
            deg = math.degrees(math.asin((self.position[1] - mouse[1]) / side_c))
            self.rotation = (deg - 90)

    def fnc_player_shoot(self):
        if datetime.datetime.now().timestamp() >= self.reload + ((self.reload_time - (self.reload_streak * self.reload_streak_multip)) / 1000):
            print((self.reload_time - (self.reload_streak * self.reload_streak_multip)) / 1000)
            self.reload = datetime.datetime.now().timestamp()
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

    def fnc_shell_update(self):
        if (self.timer + 1500) > (pygame.time.get_ticks()):
            self.fnc_shell_move()
        else:
            app.game.player.reload_streak = 0
            del app.game.player.shells[0]

    def fnc_shell_move(self):
        self.position = [self.position[0] - self.force * math.cos(math.radians(self.rotation)), self.position[1] - self.force * math.sin(math.radians(self.rotation))]


start_time = datetime.datetime.now().timestamp()

app = App()

while app.running:

    mouse_pos = list(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if app.menu_running:
                    if app.menu.btn_start_level_one_b.collidepoint(event.pos):
                        app.fnc_app_game(1)
                    elif app.menu.btn_start_level_two_b.collidepoint(event.pos):
                        app.fnc_app_game(2)
                    elif app.menu.btn_start_level_thr_b.collidepoint(event.pos):
                        app.fnc_app_game(3)
                    elif app.menu.btn_start_level_fou_b.collidepoint(event.pos):
                        app.fnc_app_game(4)
                    elif app.menu.btn_start_level_fiv_b.collidepoint(event.pos):
                        app.fnc_app_game(5)
                    elif app.menu.btn_start_level_six_b.collidepoint(event.pos):
                        app.fnc_app_game(6)
                if app.game_running:
                    app.game.player.fnc_player_shoot()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if app.game_running:
                    if app.game.player.score > app.game.player.userdata.get(f"level{app.game.level}"):
                        fnc_write_user_data(app.game.level, app.game.player.score)
                    app.fnc_app_menu()
                elif app.menu_running:
                    app.running = False

    screen.fill((20, 20, 20))

    app.fnc_app_update()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
