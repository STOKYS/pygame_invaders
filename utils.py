import json

import pygame

FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

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
img_explosion = pygame.image.load('data/media/images/explosion.png')
img_enemy_nbomb = pygame.image.load('data/media/images/enemy/nbomba.png')
img_enemy_bigbomb = pygame.image.load('data/media/images/enemy/big_bomb.png')
img_mm_bg = pygame.image.load('data/media/images/mm_bg.jpg')
