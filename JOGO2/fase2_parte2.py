import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fase2_parte2")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
plataforma_img = pygame.image.load('plataforma_madeira.png').convert_alpha()
chao_img = pygame.image.load('chao_terra.png').convert_alpha()
aguia_img = pygame.image.load('aguia.png').convert_alpha()
placa_img = pygame.image.load('placa.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()

# Cores
WHITE = (255, 255, 255)

# Classe do Personagem Principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = perso_parado_d
        self.rect = self.image.get_rect()
        self.rect.x = 50  # Centralizar na tela
        self.rect.y = SCREEN_HEIGHT - 150
        self.velocidade_y = 0
        self.no_chao = False
        self.alternador = False
        self.ultima_tecla = None
        self.velocidade = 3
        self.contador_sprite = 0  # Contador para controlar a troca de sprites
        self.limite_troca_sprite = 10
        self.tempo_dano = None
        self.dano_ativo = False  # Indica se o efeito de dano está ativo
        self.vidas = 3  # ➜ Inicia com 3 vidas

    def levar_dano(self):
        """Ativa o estado de dano e reduz uma vida."""
        if not self.dano_ativo:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.vidas -= 1  # ➜ Perde uma vida ao levar dano

            if self.vidas <= 0:
                print("GAME OVER")  # ➜ Exibe game over no console
                pygame.quit()
                sys.exit()

    def update(self, movimento, plataformas, chaos, inimigos):
        keys = pygame.key.get_pressed()

        # Controle do pulo
        if keys[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -18
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

        # for placa in placas:
        #     if self.rect.colliderect(placa.rect) and self.velocidade_y >= 0:
        #         self.rect.bottom = placa.rect.top
        #         self.velocidade_y = 0
        #         self.no_chao = True

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
        if self.rect.x >= 900:
            rodando = False
            import fase3_parte2
            fase3_parte2.jogo()

        # Verificar colisão horizontal com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                # Ajustar posição com base no movimento
                if movimento > 0:  # Indo para a direita
                    self.rect.right = plataforma.rect.left
                elif movimento < 0:  # Indo para a esquerda
                    self.rect.left = plataforma.rect.right


        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect) and self.velocidade_y >= 0:
                self.rect.bottom = inimigo.rect.top
                self.velocidade_y = 0
                self.no_chao = True
                self.levar_dano()

        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect):
                self.levar_dano()
                # Ajustar posição com base no movimento
                if movimento > 0:  # Indo para a direita
                    self.rect.right = inimigo.rect.left
                elif movimento < 0:  # Indo para a esquerda
                    self.rect.left = inimigo.rect.right

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

        # Quando solta a tecla, volta ao sprite parado
        if movimento == 0:
            if self.ultima_tecla == pygame.K_LEFT:
                self.image = perso_parado_e
            else:
                self.image = perso_parado_d

        # **Efeito de Dano**: Deixa a imagem vermelha por 1 segundo
        if self.dano_ativo:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano < 1000:  # Dura 1 segundo
                image_temp = self.image.copy()
                image_temp.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = image_temp
            else:
                self.dano_ativo = False  # Remove o efeito de dano

    def soltar_tecla(self, key):
        if key == pygame.K_LEFT:
            self.image = perso_parado_e
        elif key == pygame.K_RIGHT:
            self.image = perso_parado_d

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=2, amplitude=50):
        super().__init__()
        self.image = aguia_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = velocidade  # Velocidade do movimento vertical
        self.amplitude = amplitude  # Distância máxima que a plataforma pode se mover
        self.y_inicial = y  # Posição inicial
        self.direcao = 1  # 1 para descer, -1 para subir

    def update(self):
        # Move a plataforma dentro do intervalo definido por amplitude
        self.rect.y += self.velocidade * self.direcao

        # Inverte a direção se atingir os limites superior ou inferior
        if abs(self.rect.y - self.y_inicial) >= self.amplitude:
            self.direcao *= -1


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidade=2, amplitude=50):
        super().__init__()
        self.image = plataforma_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = velocidade  # Velocidade do movimento vertical
        self.amplitude = amplitude  # Distância máxima que a plataforma pode se mover
        self.y_inicial = y  # Posição inicial
        self.direcao = 1  # 1 para descer, -1 para subir

    def update(self):
        # Move a plataforma dentro do intervalo definido por amplitude
        self.rect.y += self.velocidade * self.direcao

        # Inverte a direção se atingir os limites superior ou inferior
        if abs(self.rect.y - self.y_inicial) >= self.amplitude:
            self.direcao *= -1

class Placa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = placa_img
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
    alturas = [0, 150, 250, 350]  # Ajuste manual das alturas para cada camada

    for i, camada in enumerate(parallax):
        posicao = -deslocamento % largura_tela
        tela.blit(camada, (posicao, alturas[i]))
        tela.blit(camada, (posicao - largura_tela, alturas[i]))

# Função para desenhar as vidas na tela
def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))  # ➜ Exibe os corações no topo

def jogo():

    caminhos_imagens = [
        "sky_cloud.png",
        "mountain.png",
        "pine1.png",
        "pine2.png"
    ]
    parallax = carregar_parallax(caminhos_imagens, SCREEN_WIDTH)

    # Inicializar sprites
    personagem = Personagem()
    plataformas = pygame.sprite.Group()
    placas = pygame.sprite.Group()
    chaos = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()

    #PLATAFORMA

    # l1 = [(x, SCREEN_HEIGHT - (50 + (x - 200) // 2)) for x in range(600, 700, 100)]
    # l2 = [(x, SCREEN_HEIGHT - 350) for x in range(900, 2100, 400)]
    # p1 = l1+l2
    # for x, y in p1:
    #     plataformas.add(Plataforma(x, y, velocidade=2, amplitude=60))

    #PLACA
    posicoes_placas = [
        (250, SCREEN_HEIGHT - 125),
        (2300, SCREEN_HEIGHT - 125)
    ]
    for x, y in posicoes_placas:
        placas.add(Placa(x, y))

    #CHAO
    posicoes_chaos = [(x, SCREEN_HEIGHT - 50) for x in range(-100, 3000, 750)]
    for x, y in posicoes_chaos:
        chaos.add(Chao(x, y))

    # AGUIA
    posicoes_inimigos = [(x, SCREEN_HEIGHT - (550 - (x - 200) // 2)) for x in range(400, 1600, 100)]

    for x, y in posicoes_inimigos:
        inimigos.add(Inimigo(x, y, velocidade=2, amplitude=60))

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
            movimento_horizontal = -2 * personagem.velocidade

        elif keys[pygame.K_RIGHT]:
            movimento = personagem.velocidade
            movimento_horizontal = 2*personagem.velocidade

        # Atualizar deslocamento do fundo
        deslocamento += movimento_horizontal

        # Atualizar posição do personagem
        personagem.update(movimento, plataformas, chaos, inimigos)

        # Atualizar posição das plataformas em relação ao movimento
        for plataforma in plataformas:
            plataforma.rect.x -= movimento_horizontal

        for placa in placas:
            placa.rect.x -= movimento_horizontal

        for chao in chaos:
            chao.rect.x -= movimento_horizontal

        for inimigo in inimigos:
            inimigo.rect.x -= movimento_horizontal

        # Desenhar fundo e sprites
        screen.fill(WHITE)
        desenhar_parallax(screen, parallax, deslocamento, SCREEN_WIDTH)
        # Desenhar plataformas e personagem
        plataformas.draw(screen)
        chaos.draw(screen)
        placas.draw(screen)
        inimigos.draw(screen)
        screen.blit(personagem.image, personagem.rect)

        #plataformas.update()
        inimigos.update()

        # **Desenha as vidas na tela**
        desenhar_vidas(screen, personagem.vidas)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo()
