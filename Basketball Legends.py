import pygame
import random

#título do jogo
titulo = ' Basketball Legends '

#valores
width = 600
height = 450

cesta_width = 120
cesta_height = 500

coin_height = 50
coin_width = 50

gap = 120

title_screen = True
game_over = False
score = 0
animacao_frame = 0

velocidade = 9
velocidade_jogo = 3
gravity = 1

FPS = 30

#definindo o movimento da bola e das asas
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('./assets/images/bola-asa_alta.png').convert_alpha(),
                       pygame.image.load('./assets/images/bola-asa_media.png').convert_alpha(),
                       pygame.image.load('./assets/images/bola-asa_baixa.png').convert_alpha()]

        self.velocidade = velocidade

        self.bola_atual = 0

        self.image = pygame.image.load('./assets/images/bola-asa_alta.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = width / 150
        self.rect[1] = height / 40

    def update(self):
        self.bola_atual = (self.bola_atual + 1) % 3
        self.image = self.images[self.bola_atual]
        self.velocidade += gravity
        self.rect[1] += self.velocidade

    def jump(self):
        self.velocidade = -velocidade
