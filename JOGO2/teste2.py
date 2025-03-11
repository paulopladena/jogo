import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo 2")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
pedra_img = pygame.image.load('pedra.png').convert_alpha()
chao_img = pygame.image.load('chao.png').convert_alpha()

# Cores
WHITE = (255, 255, 255)

# Classe do Personagem Principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = perso_parado_d
        self.rect = self.image.get_rect()
        self.rect.x = 36  # Centralizar na tela
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocidade_y = 0
        self.no_chao = False
        self.alternador = False
        self.ultima_tecla = None
        self.velocidade = 3
        self.contador_sprite = 0  # Contador para controlar a troca de sprites
        self.limite_troca_sprite = 10

    def update(self, movimento, plataformas, chaos):
        keys = pygame.key.get_pressed()

        # Controle do pulo
        if keys[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -15
            self.no_chao = False

        # Gravidade
        self.velocidade_y += 0.8
        if self.velocidade_y > 7:
            self.velocidade_y = 7
        self.rect.y += self.velocidade_y

        # Verificar colisão com o chão e plataformas
        self.no_chao = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect) and self.velocidade_y >= 0:
                self.rect.bottom = plataforma.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        for chao in chaos:
            if self.rect.colliderect(chao.rect) and self.velocidade_y >= 0:
                self.rect.bottom = chao.rect.top
                self.velocidade_y = 0
                self.no_chao = True

        # Evitar que caia do chão
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.no_chao = True
            self.velocidade_y = 0

        self.rect.x += movimento

        # Verificar colisão horizontal com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Ajustar posição com base no movimento
                if movimento > 0:  # Indo para a direita
                    self.rect.right = plataforma.rect.left
                elif movimento < 0:  # Indo para a esquerda
                    self.rect.left = plataforma.rect.right

        for chao in chaos:
            if self.rect.colliderect(chao.rect):
                # Ajustar posição com base no movimento
                if movimento > 0:  # Indo para a direita
                    self.rect.right = chao.rect.left
                elif movimento < 0:  # Indo para a esquerda
                    self.rect.left = chao.rect.right

        # Alternar sprites durante o movimento
        self.contador_sprite += 1
        if self.contador_sprite >= self.limite_troca_sprite:
            if movimento < 0:
                if self.alternador:
                    self.image = perso_mov_e2
                else:
                    self.image = perso_mov_e3
                self.alternador = not self.alternador
                self.ultima_tecla = pygame.K_LEFT
            elif movimento > 0:
                if self.alternador:
                    self.image = perso_mov_d2
                else:
                    self.image = perso_mov_d3
                self.alternador = not self.alternador
                self.ultima_tecla = pygame.K_RIGHT
            self.contador_sprite = 0

    def soltar_tecla(self, key):
        if key == pygame.K_LEFT:
            self.image = perso_parado_e
        elif key == pygame.K_RIGHT:
            self.image = perso_parado_d


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pedra_img
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


def jogo1():

    caminhos_imagens = [
        "ceu.png",
        "deserto_fundo1.png",
        "deserto_fundo2.png",
        "deserto_perto.png"
    ]
    parallax = carregar_parallax(caminhos_imagens, SCREEN_WIDTH)

    # Inicializar sprites
    personagem = Personagem()
    plataformas = pygame.sprite.Group()
    chaos = pygame.sprite.Group()

    # ** Adicionar obstáculos manualmente **
    posicoes_obstaculos = [
        (600, SCREEN_HEIGHT - 100),  # Obstáculo 1
        (1200, SCREEN_HEIGHT - 100),  # Obstáculo 2
        (1800, SCREEN_HEIGHT - 100),  # Obstáculo 3
        (2300, SCREEN_HEIGHT - 100),  # Obstáculo 4
    ]
    for x, y in posicoes_obstaculos:
        plataformas.add(Plataforma(x, y))

    posicoes_chaos = [
        (-10, SCREEN_HEIGHT - 500),  # Obstáculo 1
        (700, SCREEN_HEIGHT - 300),  # Obstáculo 2
        (1400, SCREEN_HEIGHT - 450),  # Obstáculo 3
        (2100, SCREEN_HEIGHT - 400),  # Obstáculo 4
    ]
    for x, y in posicoes_chaos:
        chaos.add(Chao(x, y))

    clock = pygame.time.Clock()
    rodando = True

    deslocamento = 0  # Controle do deslocamento do fundo

    while rodando:

        movimento = 0
        movimento_horizontal = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
            if event.type == pygame.KEYUP:
                personagem.soltar_tecla(event.key)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            movimento = -personagem.velocidade
            movimento_horizontal = -2*personagem.velocidade
        elif keys[pygame.K_RIGHT]:
            movimento = personagem.velocidade
            movimento_horizontal = 2*personagem.velocidade

        # Atualizar deslocamento do fundo
        deslocamento += movimento_horizontal

        # Atualizar posição do personagem
        personagem.update(movimento, plataformas, chaos)

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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo1()
