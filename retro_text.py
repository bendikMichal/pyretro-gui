
import os
import pygame

pygame.font.init()

from .path_handler import base_path

font = pygame.font.Font(base_path + "/fonts/retrofont.ttf", 16)
small_font = pygame.font.Font(base_path + "/fonts/retrofont.ttf", 15)
small_font.set_italic(True)
bold_font = pygame.font.Font(base_path + "/fonts/retrofont.ttf", 16)
bold_font.set_bold(True)

# font = pygame.font.Font(base_path + "/fonts/W95FA.otf", 14)
# font.set_bold(True)
