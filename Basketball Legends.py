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
        
#definindo a calsse dos canos/cesta
class Cesta(pygame.sprite.Sprite):

    def __init__(self, inverted,posicao_x,tamanho):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('./assets/images/cesta.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(cesta_width,cesta_height))
        
        self.rect = self.image.get_rect()
        self.rect[0] = posicao_x
        
        #canos invertidos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - tamanho)
        else:
            self.rect[1] = height - tamanho
        
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= velocidade_jogo
#definindo a classe da moeda invisel para o colisão com o score       
class Moeda(pygame.sprite.Sprite):

    def __init__(self,xpos,ypos):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('./assets/images/moeda.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(coin_width,coin_height))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos
        
        
    def update(self):
        self.rect[0] -= velocidade_jogo
    
        
        
# posicionando os canos e a moeda
def cestas_aleatorias(posicao_x):
    tam = random.randint(100,300)
    ycoin = tam + gap/2
    cesta = Cesta(False, posicao_x, tam)
    cesta_invertida = Cesta(True, posicao_x, height - tam - gap)
    moeda = Moeda(posicao_x,ycoin)
    coin_group.add(moeda)
    
    return (cesta, cesta_invertida)

def fora_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()
pygame.font.init()

#recebe as fontes e tamanho
textfont = pygame.font.Font('./assets/fonts/Down_Hill.ttf', 30)
titlefont = pygame.font.Font('./assets/fonts/Down_Hill.ttf', 38)

# display screen
window = pygame.display.set_mode((width, height))
pygame.display.set_caption(titulo)

#carrega todas os backrounds diferentes (ja estão na width e height certas)
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

#definindo os grupos
coin_group = pygame.sprite.Group()

ball_group = pygame.sprite.Group()
ball = Ball()
ball_group.add(ball)



cesta_group = pygame.sprite.Group()

#invertendo a cesta
for a in range(2):
    cestas = cestas_aleatorias(width * a + 700)
    cesta_group.add(cestas[0])
    cesta_group.add(cestas[1])

#contadores
i = 0
k = 0
x = 0

clock = pygame.time.Clock()

#carregando os sons
ball_bounce = pygame.mixer.Sound('./assets/sounds/bounce.wav')
coin_sound = pygame.mixer.Sound('./assets/sounds/coin_sound.wav')
music = pygame.mixer.music.load('./assets/sounds/soundtrack.mp3')
pygame.mixer.music.play(-1)
window_open = True

#rotina/loop  eventos
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
