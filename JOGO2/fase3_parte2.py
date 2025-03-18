import pygame
import sys
import carrega_vidas

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fase3_parte2")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
nave_img = pygame.image.load('nave_mold.png').convert_alpha()
chao_img = pygame.image.load('chao_gelo.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Controle de estado
personagem_na_nave = False  # Define se o personagem já entrou na nave

# Grupo de tiros
tiros = pygame.sprite.Group()


class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = perso_parado_d
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 200
        self.velocidade_y = 0
        self.no_chao = False
        self.alternador = False
        self.ultima_tecla = None
        self.frame_delay = 10
        self.frame_contador = 0
        self.vidas = carrega_vidas.vidas_personagem

    def update(self):
        global personagem_na_nave

        if personagem_na_nave:
            return  # Para de atualizar o personagem se ele já entrou na nave

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
            self.frame_contador += 1
            if self.frame_contador >= self.frame_delay:
                self.alternador = not self.alternador
                self.frame_contador = 0
            self.image = perso_mov_e2 if self.alternador else perso_mov_e3
            self.ultima_tecla = pygame.K_LEFT

        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 7
            self.frame_contador += 1
            if self.frame_contador >= self.frame_delay:
                self.alternador = not self.alternador
                self.frame_contador = 0
            self.image = perso_mov_d2 if self.alternador else perso_mov_d3
            self.ultima_tecla = pygame.K_RIGHT

        else:
            self.image = perso_parado_e if self.ultima_tecla == pygame.K_LEFT else perso_parado_d

        self.velocidade_y += 0.8
        if self.velocidade_y > 7:
            self.velocidade_y = 7
        self.rect.y += self.velocidade_y

        colidiu_chao = pygame.sprite.spritecollide(self, chaos, False)
        if colidiu_chao and self.velocidade_y >= 0:
            self.rect.bottom = colidiu_chao[0].rect.top
            self.no_chao = True
            self.velocidade_y = 0

        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.no_chao = True
            self.velocidade_y = 0

        if keys[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -15
            self.no_chao = False

        # Verificar se o personagem entrou na nave
        if self.rect.colliderect(nave.rect) and keys[pygame.K_s]:
            personagem_na_nave = True  # Ativa o modo nave
            todos_sprites.remove(self)  # Remove o personagem da tela

        if self.rect.x >= 935:
            rodando = False
            import carrega_vidas
            import fase3_parte3
            fase3_parte3.jogo(carrega_vidas.vidas_personagem)


class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, color, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.y += self.direction * 10  # Tiros para cima (-1)
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = SCREEN_HEIGHT - 500
        self.vidas = 7
        self.ultimo_tiro = 0

    def update(self):
        if not personagem_na_nave:
            return  # A nave só pode ser controlada após o personagem entrar

        colidiu_chao = pygame.sprite.spritecollide(self, chaos, False)
        if colidiu_chao:
            self.rect.y += 20

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 7
        if keys[pygame.K_UP] and self.rect.top > -300:
            self.rect.y -= 7
            print(self.rect.y)
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT - 70:
            self.rect.y += 7

        if keys[pygame.K_SPACE]:  # Pressiona espaço para atirar
            self.atirar()

        if keys[pygame.K_UP] and self.rect.y <=  -300:
            rodando = False
            import fase3_dica
            fase3_dica.jogo()

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= 500:  # Intervalo entre tiros
            self.ultimo_tiro = agora
            tiro_esq = Tiro(self.rect.left + 70 , self.rect.top, YELLOW, -1)
            tiro_dir = Tiro(self.rect.right - 70, self.rect.top, YELLOW, -1)
            tiros.add(tiro_esq, tiro_dir)


class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        super().__init__()
        self.image_original = pygame.transform.scale(chao_img, (a, b))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dano_ativo = False
        self.vida = 10

    def update(self):
        # Verifica se o efeito de dano deve desaparecer
        if self.dano_ativo and pygame.time.get_ticks() - self.tempo_dano >= 200:
            self.image = self.image_original
            self.dano_ativo = False

    def levar_tiro(self):
        self.vida -= 1
        if self.vida < 0:
            self.kill()
        else:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.image = self.image_original.copy()
            self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

def fase1():
    global personagem, chaos, nave, todos_sprites

    personagem = Personagem()

    chao1 = Chao(0, SCREEN_HEIGHT - 50, 1200, 100)
    chao2 = Chao(0, SCREEN_HEIGHT - 800, 1200, 100)
    chaos = pygame.sprite.Group(chao1, chao2)

    nave = Nave()

    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(nave, chao1, chao2, personagem)  # Adiciona a nave e o personagem ao início


def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))


def jogo1():
    fase1()
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        for tiro in tiros:
            chao_atingido = pygame.sprite.spritecollide(tiro, chaos, False)

            for chao in chao_atingido:
                chao.levar_tiro()
                tiro.kill()

        todos_sprites.update()
        tiros.update()

        todos_sprites.draw(screen)
        tiros.draw(screen)

        desenhar_vidas(screen, nave.vidas)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo1()
