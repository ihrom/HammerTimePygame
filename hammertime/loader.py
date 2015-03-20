import pygame
import os.path

# This is the directory in which graphics will be stored
IMAGE_DIR = 'hammertime\\graphics'
SOUND_DIR = 'hammertime\\sounds'

def load_image(name):
    path = os.path.join(IMAGE_DIR, name + '.png')
    surf = pygame.image.load(path).convert()
    return surf

def load_sound(name):
    path = os.path.join(SOUND_DIR, name + '.ogg')
    sound = pygame.mixer.Sound(path)
    return sound



