import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fase2_dica")

# Carregar imagens
merg1d = pygame.image.load('mergulhador1_d.png').convert_alpha()
merg2d = pygame.image.load('mergulhador2_d.png').convert_alpha()
merg1e = pygame.image.load('mergulhador1_e.png').convert_alpha()
merg2e = pygame.image.load('mergulhador2_e.png').convert_alpha()
av_img = pygame.image.load('agua_viva.png').convert_alpha()
chao_img = pygame.image.load('chao.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()

# Cores
WHITE = (255, 255, 255)

# Classe do Personagem Principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = merg1d  # Salva a imagem original para restauração
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = SCREEN_HEIGHT - 600
        self.alternador = False
        self.ultima_tecla = None
        self.velocidade = 3
        self.contador_sprite = 0
        self.limite_troca_sprite = 10
        self.frame_delay = 10
        self.frame_contador = 0
        self.tempo_dano = None
        self.dano_ativo = False
        self.vidas = 10

    def levar_dano(self):
        """Ativa o estado de dano e reduz uma vida."""
        if not self.dano_ativo:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.vidas -= 1

            if self.vidas <= 0:
                print("GAME OVER")
                pygame.quit()
                sys.exit()

    def update(self, movimento, movimentov, plataformas, chaos):
        keys = pygame.key.get_pressed()

        # Verificar colisão com plataformas (inimigos)
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                self.levar_dano()

        # Evitar que saia da tela
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
        if self.rect.top <= 50:
            self.rect.top = 50

        self.rect.x += movimento
        self.rect.y += movimentov

        # Alternar sprites durante o movimento
        self.contador_sprite += 1
        if self.contador_sprite >= self.limite_troca_sprite:
            if movimento < 0:
                self.image_original = merg1e if self.alternador else merg2e
                self.ultima_tecla = pygame.K_LEFT
            elif movimento > 0:
                self.image_original = merg1d if self.alternador else merg2d
                self.ultima_tecla = pygame.K_RIGHT
            self.image = self.image_original  # Garante que a imagem base seja restaurada
            self.alternador = not self.alternador
            self.contador_sprite = 0

        # **Efeito de Dano**: Deixa a imagem vermelha por 1 segundo
        if self.dano_ativo:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano < 1000:  # Dura 1 segundo
                image_temp = self.image_original.copy()
                image_temp.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = image_temp
            else:
                self.dano_ativo = False  # Remove o efeito de dano
                self.image = self.image_original  # Restaura a imagem original

    def soltar_tecla(self, key):
        if key == pygame.K_LEFT:
            self.image_original = merg1e
        elif key == pygame.K_RIGHT:
            self.image_original = merg1d
        self.image = self.image_original



class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = av_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = chao_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Carregar as imagens do parallax
def carregar_parallax(caminhos_imagens, largura_tela):
    camadas = []
    for caminho in caminhos_imagens:
        imagem = pygame.image.load(caminho).convert_alpha()
        largura_imagem, altura_imagem = imagem.get_size()
        fator_escala = largura_tela / largura_imagem
        altura_ajustada = int(altura_imagem * fator_escala)
        imagem_escalada = pygame.transform.scale(imagem, (largura_tela, altura_ajustada))
        camadas.append(imagem_escalada)
    return camadas


# Desenhar o parallax com scroll
def desenhar_parallax(tela, parallax, deslocamento, largura_tela):
    for camada in parallax:
        posicao = -deslocamento % largura_tela
        tela.blit(camada, (posicao, 0))
        tela.blit(camada, (posicao - largura_tela, 0))

# Função para desenhar as vidas na tela
def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))  # ➜ Exibe os corações no topo

def jogo1():

    caminhos_imagens = [
        "mar.png"
    ]
    parallax = carregar_parallax(caminhos_imagens, SCREEN_WIDTH)

    # Inicializar sprites
    personagem = Personagem()
    plataformas = pygame.sprite.Group()
    chaos = pygame.sprite.Group()

    #AGUA VIVA

    #PARTE1 HORIZONTAL
    l1 = [(x, SCREEN_HEIGHT - 150) for x in range(200, 700, 100)] #CHAO
    l2 = [(x, SCREEN_HEIGHT - 350) for x in range(200, 600, 100)]
    l3 = [(x, SCREEN_HEIGHT - 550) for x in range(200, 700, 100)]
    l4 = [(x, SCREEN_HEIGHT - 700) for x in range(200, 700, 100)] #TOP
    p1 = l1 + l2 + l3 + l4

    #PARTE2 (DIAGONAL CRESCENTE)
    l5 = [(x, SCREEN_HEIGHT - (200 + (x - 200) // 2)) for x in range(700, 1300, 100)] #TOP
    l6 = [(x, SCREEN_HEIGHT - (-100 + (x - 200) // 2)) for x in range(700, 1200, 100)]
    p2 = l5 + l6

    # PARTE3 (DIAGONAL CRESCENTE)
    l7 = [(x, SCREEN_HEIGHT - (1200 - (x - 200) // 2)) for x in range(1200, 1600, 100)]  # TOP
    l8 = [(1500, y) for y in range(SCREEN_HEIGHT - 250, SCREEN_HEIGHT - 550, -100)]
    p3 = l7 + l8

    posicoes_obstaculos = p1 + p2 + p3

    for x, y in posicoes_obstaculos:
        plataformas.add(Plataforma(x, y))

    posicoes_chaos = [
        (-500, SCREEN_HEIGHT - 50),
        (-10, SCREEN_HEIGHT - 50),
        (700, SCREEN_HEIGHT - 50),
        (1400, SCREEN_HEIGHT - 50),
        (2100, SCREEN_HEIGHT - 50),
        (2800, SCREEN_HEIGHT - 50)
    ]
    for x, y in posicoes_chaos:
        chaos.add(Chao(x, y))

    clock = pygame.time.Clock()
    rodando = True

    deslocamento = 0  # Controle do deslocamento do fundo

    while rodando:

        movimento = 0
        movimentov = 0
        movimento_horizontal = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYUP:
                personagem.soltar_tecla(event.key)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            movimentov = -personagem.velocidade
        if keys[pygame.K_DOWN]:
            movimentov = personagem.velocidade

        if keys[pygame.K_LEFT]:
            movimento = -personagem.velocidade
            movimento_horizontal = -2*personagem.velocidade

        elif keys[pygame.K_RIGHT]:
            movimento = personagem.velocidade
            movimento_horizontal = 2*personagem.velocidade

        # Atualizar deslocamento do fundo
        deslocamento += movimento_horizontal

        # Atualizar posição do personagem
        personagem.update(movimento, movimentov, plataformas, chaos)

        # Desenhar fundo e sprites
        screen.fill(WHITE)
        desenhar_parallax(screen, parallax, deslocamento, SCREEN_WIDTH)

        # Atualizar posição das plataformas em relação ao movimento
        for plataforma in plataformas:
            plataforma.rect.x -= movimento_horizontal

        for chao in chaos:
            chao.rect.x -= movimento_horizontal

        # Desenhar plataformas e personagem
        plataformas.draw(screen)
        chaos.draw(screen)
        screen.blit(personagem.image, personagem.rect)

        # **Desenha as vidas na tela**
        desenhar_vidas(screen, personagem.vidas)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo1()
