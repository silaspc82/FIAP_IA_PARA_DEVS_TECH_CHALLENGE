# -*- coding: utf-8 -*-
import pylab
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib
import pygame
import itertools
import sys
from typing import List, Tuple

matplotlib.use("Agg")

WIDTH, HEIGHT = 800, 800
FPS = 30
WHITE = (255, 255, 255)

def plotar_grafico(x: list, y: list, x_label: str = 'Generation', y_label: str = 'Fitness') -> None:
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Melhor rota para compras.")
    clock = pygame.time.Clock()
    generation_counter = itertools.count(start=1)

    screen.fill(WHITE)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    ax.plot(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    plt.tight_layout()

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()

    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)
    x = input('Aperte ENTER para finalizar.')

    pygame.quit()
    sys.exit()
