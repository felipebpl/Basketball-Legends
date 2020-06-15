# -*- coding: utf-8 -*-
"""
Created on Thu May 14 00:09:47 2020

@author: felem
"""
import pygame
import random

#título do jogo
titulo = ' Basketball Legends '

#valores
width = 600
height = 450

cesta_width = 120
cesta_height = 500

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

class Cesta(pygame.sprite.Sprite):

    def __init__(self, inverted,posicao_x,tamanho):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./assets/images/cesta.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(cesta_width,cesta_height))
        
        self.rect = self.image.get_rect()
        self.rect[0] = posicao_x
        
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - tamanho)
        else:
            self.rect[1] = height - tamanho
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= velocidade_jogo
    



def cestas_aleatorias(posicao_x):
    tam = random.randint(100,300)
    cesta = Cesta(False, posicao_x, tam)
    cesta_invertida = Cesta(True, posicao_x, height - tam - gap)
    return (cesta, cesta_invertida)

def fora_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

# display screen
pygame.init()
pygame.font.init()

textfont = pygame.font.Font('./assets/fonts/Down_Hill.ttf', 30)
titlefont = pygame.font.Font('./assets/fonts/Down_Hill.ttf', 38)

window = pygame.display.set_mode((width, height))
pygame.display.set_caption(titulo)

backgrounds = [pygame.image.load('./assets/images/background_intro.png').convert_alpha(),
               pygame.image.load('./assets/images/background_jordan.png').convert_alpha(),
               pygame.image.load('./assets/images/background_bird.png').convert_alpha(),
               pygame.image.load('./assets/images/background_kobe.png').convert_alpha(),
               pygame.image.load('./assets/images/background_magic.png').convert_alpha(),
               pygame.image.load('./assets/images/background_lebron.png').convert_alpha(),
               pygame.image.load('./assets/images/background_karim.png').convert_alpha(),
               pygame.image.load('./assets/images/background_shaq.png').convert_alpha(),
               pygame.image.load('./assets/images/background_pippen.png').convert_alpha(),
               pygame.image.load('./assets/images/background_rodman.png').convert_alpha(),
               pygame.image.load('./assets/images/background_curry.png').convert_alpha(),
               pygame.image.load('./assets/images/background_end.png').convert_alpha()]

moeda = pygame.image.load('./assets/images/moeda.png').convert_alpha()




ball_group = pygame.sprite.Group()
ball = Ball()
ball_group.add(ball)

cesta_group = pygame.sprite.Group()
for a in range(2):
    cestas = cestas_aleatorias(width * a + 700)
    cesta_group.add(cestas[0])
    cesta_group.add(cestas[1])

i = 0
k = 0
x = 0

clock = pygame.time.Clock()

ball_bounce = pygame.mixer.Sound('./assets/sounds/bounce.wav')

music = pygame.mixer.music.load('./assets/sounds/soundtrack.mp3')
pygame.mixer.music.play(-1)

window_open = True

while window_open :

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            window_open = False

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_RETURN:
                title_screen = False
                
            if not game_over and event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                ball_bounce.play()
                ball.jump()

            if game_over and event.key == pygame.K_RETURN:
                title_screen = True
                game_over = False
                score = 0
                ball.rect[1] = 0
          

    posicao_fundo = x % backgrounds[i].get_rect().width

    window.blit(backgrounds[i], (posicao_fundo - backgrounds[i].get_rect().width, 0))

    if posicao_fundo < width:
        window.blit(backgrounds[(i+1) % len(backgrounds)], (posicao_fundo,0))
        
    if game_over:
         # GAMEOVER sombreado
        txt_gameover2 = titlefont.render("Game Over", 1, (255,60,0))
        window.blit(txt_gameover2, (245, 200))
        
        # GAMEOVER principal
        txt_gameover1 = titlefont.render("Game Over", 1, (255,255,255))
        window.blit(txt_gameover1, (240, 195))
        
        #Formantando a pontuação
        txt_score = textfont.render("Final Score: {0}".format(score), 1, (255,255,0))
        window.blit(txt_score, (245, 230))
        
        
    elif title_screen:
            
        # START sombreado
        txt_title_sombra = titlefont.render("Basketball Legends", 1, (255,60,0))
        window.blit(txt_title_sombra, (165, 25))
        
        #START principal
        txt_title = titlefont.render("Basketball Legends", 1, (255,255,255))
        window.blit(txt_title, (160, 20))

        
        animacao_frame = animacao_frame + 1
        
        if animacao_frame <= 15:
            press_start = textfont.render("Press ENTER to START", 1, (255,255,255))
            window.blit(press_start, (160, 380))
            
        if animacao_frame > 20:
            animacao_frame = 0
            
    else:

        # Definindo a dificuldade
        if score < 10: 
           velocidade_jogo = 3
           gravity = 1
           gap = 200
           
        if score > 10:
           velocidade_jogo = 4
           gravity = 1
           gap = 150
           
        if score > 20:
           velocidade_jogo = 6
           gravity = 1.2
           gap = 140
           
        if score > 30:
           velocidade_jogo = 9
           gravity = 1.3
           gap = 115
           
        if score > 35:
           velocidade_jogo = 13
           gravity = 1.4
           gap = 99
           
        if score > 40:
           velocidade_jogo = 14
           gravity = 1.4
           gap = 90
           
            
            
        x -= 2
        
        txt_score = textfont.render("Score {0}".format(score), 1, (255,255,0))
        window.blit(txt_score, (5, 10))

        if posicao_fundo == 0:
            i = (i+1) % len(backgrounds)
        
        
        
        if fora_tela(cesta_group.sprites()[0]):
            
            cesta_group.remove(cesta_group.sprites()[0])
            cesta_group.remove(cesta_group.sprites()[0])

            cestas = cestas_aleatorias(width * 2)

            cesta_group.add(cestas[0])
            cesta_group.add(cestas[1])

        ball_group.update()
        cesta_group.update()
    
    
        ball_group.draw(window)
        cesta_group.draw(window)

    pygame.display.update()
    
    if pygame.sprite.groupcollide(ball_group, cesta_group, False, False, pygame.sprite.collide_mask):
        game_over = True
    
    
    clock.tick(FPS)

pygame.quit()

