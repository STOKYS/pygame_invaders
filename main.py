import json
import pygame
import math
import random
import datetime

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
FPS = 60

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Invaders")
screen = pygame.display.set_mode([1000, 1000])
pygame.display.set_icon(pygame.image.load('data/media/images/icon.jpg'))

f_fifty = pygame.font.Font(None, 50)
f_forty = pygame.font.Font(None, 40)
f_thirty = pygame.font.Font(None, 30)
f_twenty = pygame.font.Font(None, 20)
f_ten = pygame.font.Font(None, 10)


def fnc_read_user_data(encoding='utf-8'):
    try:
        with open('data/user_data/user_data.json', mode='r', encoding=encoding) as file:
            data = json.load(file)
    except Exception as error:
        return f"Something went wrong with opening user data file: {error}"
    finally:
        file.close()
    return data


def fnc_write_user_data(level, score, encoding='utf-8'):
    data = fnc_read_user_data()
    data[f"level{level}"] = score
    try:
        with open('data/user_data/user_data.json', mode='w', encoding=encoding) as file:
            json.dump(data, file, indent=4)
    except Exception as error:
        return f"Something went wrong with opening user data file: {error}"
    finally:
        file.close()
    return data


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


class Menu:
    def __init__(self, parent):
        parent.menu_running = True
        self.user_data = fnc_read_user_data()
        self.btn_start_level_one_b, self.btn_start_level_two_b, self.btn_start_level_thr_b, self.btn_start_level_fou_b, self.btn_start_level_fiv_b, self.btn_start_level_six_b = (None, )*6

    def fnc_menu_update(self):
        self.btn_start_level_one_b = pygame.draw.rect(screen, (0, 255, 0),  (0, 0, SCREEN_WIDTH/3, SCREEN_HEIGHT/2))
        self.btn_start_level_two_b = pygame.draw.rect(screen, (50, 200, 0), (SCREEN_WIDTH / 3, 0, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_thr_b = pygame.draw.rect(screen, (100, 150, 0), (SCREEN_WIDTH / 3 * 2, 0, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_fou_b = pygame.draw.rect(screen, (150, 100, 0), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_fiv_b = pygame.draw.rect(screen, (200, 50, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_six_b = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        screen.blit(img_mm_bg, (0, 0))


class Game:
    def __init__(self, parent, level):
        parent.game_running = True
        self.started = False
        self.player = Player()
        self.enemies = [Bomb()]
        self.timer = datetime.datetime.now().timestamp()
        self.delay = [4000, 3500, 3000, 2500, 2500, 2000]
        self.delay_s = [2500, 2000, 2000, 2000, 1500, 1000]
        self.delay_ch = [20, 20, 20, 20, 15, 15]
        self.level = level

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
        self.enemies.append(Bomb())

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
                    screen.blit(img_explosion, self.enemies[j].position)
                    if self.player.reload_streak > 0:
                        self.player.reload_streak -= 1
                self.enemies[j].fnc_bomb_update()
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
                        self.player.reload_streak += 1
                        screen.blit(img_explosion, self.enemies[j].position)
                        shell_buffer.append(i)
                        bomb_buffer.append(j)
                        self.player.score += 10
            for i in range(len(shell_buffer)):
                del self.player.shells[shell_buffer[i]]
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
        screen.blit(f_twenty.render(f'H-Score: {self.player.userdata.get(f"level{self.level}")}', True, (200, 200, 200)),(0, 20))
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


class Bomb:
    def __init__(self):
        self.position = [random.randrange(900) + 50, -50]

    def fnc_bomb_update(self):
        self.fnc_bomb_move()

    def fnc_bomb_move(self):
        self.position = [self.position[0], self.position[1] + 3]


def fnc_collision(shell, bomb):
    __bomb_xy = [bomb[0], bomb[0] + 18, bomb[1], bomb[1] + 40]
    __shell_xy = [shell[0] - 5, shell[0] + 5, shell[1] - 5, shell[1] + 5]
    if (__bomb_xy[3] < __shell_xy[2]) or (__bomb_xy[2] > __shell_xy[3]) or (__bomb_xy[1] < __shell_xy[0]) or (__bomb_xy[0] > __shell_xy[1]):
        return False
    else:
        return True


img_player_cannon = pygame.image.load('data/media/images/player/cannon.png')
img_player_turret_bg = pygame.image.load('data/media/images/player/turret_bg.png')
img_player_turret_fg = pygame.image.load('data/media/images/player/turret_fg.png')
img_player_char_harry = pygame.image.load('data/media/images/player/col_harry.png')
img_player_char_george = pygame.image.load('data/media/images/player/cpt_george.png')
img_player_char_charles = pygame.image.load('data/media/images/player/lt_charles.png')
img_player_cross = pygame.image.load('data/media/images/player/cross.png')
img_enemy_bomb = pygame.image.load('data/media/images/enemy/bomb.png')
img_mm_bg = pygame.image.load('data/media/images/mm_bg.jpg')
img_explosion = pygame.image.load('data/media/images/explosion.png')

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
