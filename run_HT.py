import sys

if sys.version_info[:2] < (3, 2):
    sys.exit("Hammer Time requires Python 3")

try:
    import pygame
except ImportError:
    sys.exit("Hammer Time requires Pygame 3+")

from hammertime.__main__ import main
main()

