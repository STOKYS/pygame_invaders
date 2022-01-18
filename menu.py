import pygame

from utils import SCREEN_WIDTH, SCREEN_HEIGHT, screen, img_mm_bg, fnc_read_user_data


class Menu:
    def __init__(self, parent):
        parent.menu_running = True
        self.user_data = fnc_read_user_data()
        self.btn_start_level_one_b, self.btn_start_level_two_b, self.btn_start_level_thr_b, self.btn_start_level_fou_b, self.btn_start_level_fiv_b, self.btn_start_level_six_b = (None, )*6
        pygame.display.set_caption("Invaders")

    def fnc_menu_update(self):
        self.btn_start_level_one_b = pygame.draw.rect(screen, (0, 255, 0),  (0, 0, SCREEN_WIDTH/3, SCREEN_HEIGHT/2))
        self.btn_start_level_two_b = pygame.draw.rect(screen, (50, 200, 0), (SCREEN_WIDTH / 3, 0, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_thr_b = pygame.draw.rect(screen, (100, 150, 0), (SCREEN_WIDTH / 3 * 2, 0, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_fou_b = pygame.draw.rect(screen, (150, 100, 0), (0, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_fiv_b = pygame.draw.rect(screen, (200, 50, 0), (SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        self.btn_start_level_six_b = pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH / 3 * 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2))
        screen.blit(img_mm_bg, (0, 0))