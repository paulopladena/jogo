import pygame
import sys
import random
import carrega_vidas

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("jogo_fase1_dica")

# Carregar imagens
nave_img = pygame.image.load('nave.png').convert_alpha()
inimigo_img = pygame.image.load('inimigo.png').convert_alpha()
nave2_img = pygame.image.load('nave2.png').convert_alpha()
nave3_img = pygame.image.load('nave3.png').convert_alpha()
cacto_img = pygame.image.load('cacto.png').convert_alpha()
bg = pygame.image.load('bg_piramide.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()
dica_img = pygame.image.load('dica.png')
caixa_dialogo_img = pygame.image.load('caixa_dialogo.png')

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

som = pygame.mixer.Sound('cowbell-for-songs-phonk-217006.ogg')
som2 = pygame.mixer.Sound('winfantasia-6912.ogg')

canal = pygame.mixer.Channel(0)
canal2 = pygame.mixer.Channel(1)

# Grupo de tiros
tiros = pygame.sprite.Group()
tiros_inimigos = pygame.sprite.Group()  # Novo grupo para os tiros dos inimigos
tiros_chefe = pygame.sprite.Group()
tiros_especiais_chefe = pygame.sprite.Group()


class Tiro(pygame.sprite.Sprite):
    def __init__(self, x, y, color, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        self.rect.y += self.direction * 10  # Direção positiva = descendo (inimigos), negativa = subindo (jogador)
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_original = nave_img
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = SCREEN_HEIGHT - 150
        self.vidas = 7
        self.tempo_dano = 0
        self.dano_ativo = False
        self.ultimo_tiro = 0
        self.vitoria = False

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 7
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 7
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += 7

        if keys[pygame.K_SPACE]:
            self.atirar()

        # Verifica se já passou tempo suficiente para remover o efeito de dano
        if self.dano_ativo and pygame.time.get_ticks() - self.tempo_dano >= 200:
            self.image = self.image_original
            self.dano_ativo = False

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= 500:
            self.ultimo_tiro = agora
            tiro_esq = Tiro(self.rect.left + 15, self.rect.top, YELLOW, -1)
            tiro_dir = Tiro(self.rect.right - 15, self.rect.top, YELLOW, -1)
            tiros.add(tiro_esq, tiro_dir)

    def levar_dano(self):
        self.vidas -= 1
        if self.vidas < 0:
            canal.pause()
            import game_over
            game_over.tela_fim()

        else:
            self.tempo_dano = pygame.time.get_ticks()  # Registra o tempo do dano
            self.dano_ativo = True
            self.image = self.image_original.copy()
            self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)


class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, limite_esquerdo, limite_direito, limite_cima, limite_baixo):
        super().__init__()
        self.image_original = nave2_img
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 2
        self.altura = 2
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.limite_cima = limite_cima
        self.limite_baixo = limite_baixo
        self.direcao = 1
        self.vida = 5
        self.tempo_dano = 0
        self.dano_ativo = False
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocidade
        self.rect.y += self.altura

        if self.rect.right >= self.limite_direito or self.rect.left <= self.limite_esquerdo:
            self.velocidade = -self.velocidade
            self.direcao *= -1
            if self.direcao == -1:
                self.image = pygame.transform.flip(self.image_original, True, False)
            else:
                self.image = self.image_original

        if self.rect.top >= self.limite_cima or self.rect.bottom <= self.limite_baixo:
            self.altura = -self.altura

        # Verifica se o efeito de dano deve desaparecer
        if self.dano_ativo and pygame.time.get_ticks() - self.tempo_dano >= 200:
            self.image = self.image_original
            self.dano_ativo = False

        # Inimigo atira a cada 2 segundos
        self.atirar()

    def levar_tiro(self):
        self.vida -= 1
        if self.vida < 0:
            self.kill()
        else:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.image = self.image_original.copy()
            self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= 2000:  # 2 segundos entre cada tiro
            self.ultimo_tiro = agora
            tiro = Tiro(self.rect.centerx, self.rect.bottom, RED, 1)  # Tiro para baixo
            tiros_inimigos.add(tiro)

class Chefe(pygame.sprite.Sprite):
    def __init__(self, x, y, limite_esquerdo, limite_direito, limite_cima, limite_baixo):
        super().__init__()
        self.image_original = nave3_img
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 2
        self.altura = 2
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.limite_cima = limite_cima
        self.limite_baixo = limite_baixo
        self.direcao = 1
        self.vida = 15
        self.tempo_dano = 0
        self.dano_ativo = False
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.velocidade
        self.rect.y += self.altura

        if self.rect.right >= self.limite_direito or self.rect.left <= self.limite_esquerdo:
            self.velocidade = -self.velocidade
            self.direcao *= -1
            if self.direcao == -1:
                self.image = pygame.transform.flip(self.image_original, True, False)
            else:
                self.image = self.image_original

        if self.rect.top >= self.limite_cima or self.rect.bottom <= self.limite_baixo:
            self.altura = -self.altura

        # Verifica se o efeito de dano deve desaparecer
        if self.dano_ativo and pygame.time.get_ticks() - self.tempo_dano >= 200:
            self.image = self.image_original
            self.dano_ativo = False

        # Inimigo atira a cada 2 segundos
        self.atirar()

    def levar_tiro(self):
        self.vida -= 1
        if self.vida < 0:
            self.kill()
        else:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.image = self.image_original.copy()
            self.image.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= 2000:  # 2 segundos entre cada tiro
            self.ultimo_tiro = agora
            tiro_chefe_esq = Tiro(self.rect.left + 50, self.rect.bottom, RED, 1)
            tiro_chefe_dir = Tiro(self.rect.right - 50, self.rect.bottom, RED, 1)
            tiros_chefe.add(tiro_chefe_esq, tiro_chefe_dir)


    def iniciar_tiro_especial(self):
        self.atacando_especial = True
        self.ultimo_tiro_especial = pygame.time.get_ticks()
        for i in range(10):
            tiros_especiais_chefe.add(Tiro(self.rect.centerx, self.rect.bottom + (i * 20), RED, 1))

class Papel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = dica_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mostrar_dica = False

    def mostrar_mensagem(self):
        if self.mostrar_dica:
            import carrega_vidas
            screen.blit(carrega_vidas.bq[carrega_vidas.selec3[0]]['dica'], (0, SCREEN_HEIGHT // 4))
            screen.blit(carrega_vidas.bq[carrega_vidas.selec3[1]]['dica'], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

def fase1():
    global personagem, papel, inimigos, chefe, todos_sprites

    personagem = Personagem()
    papel = Papel(450, SCREEN_HEIGHT - 300)

    inimigo1 = Inimigo(200, SCREEN_HEIGHT - 500, 100, 750, 0, 0)
    inimigo2 = Inimigo(550, SCREEN_HEIGHT - 400, 300, 750, 0, 0)
    inimigo3 = Inimigo(350, SCREEN_HEIGHT - 300, 150, 600, 0, 0)
    inimigos = pygame.sprite.Group([inimigo1, inimigo2, inimigo3])

    chefe = pygame.sprite.GroupSingle(Chefe(350, SCREEN_HEIGHT - 750, 150,  600, 0, 0))
    todos_sprites = pygame.sprite.Group(personagem, inimigos, chefe)

def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))

def desenhar_dica(tela):
    tela.blit(dica_img, (10 + 7 * 40, 5))

def jogo1():
    fase1()
    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
    rodando = True
    tempo_vitoria = None

    while rodando:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        # Detecta colisão entre tiros do jogador e inimigos
        for tiro in tiros:
            inimigos_atingidos = pygame.sprite.spritecollide(tiro, inimigos, False)
            chefe_atingido = pygame.sprite.spritecollide(tiro, chefe, False)

            for inimigo in inimigos_atingidos:
                inimigo.levar_tiro()
                tiro.kill()
            if chefe_atingido:
                chefe.sprite.levar_tiro()
                tiro.kill()

        # Detecta colisão entre tiros inimigos e o personagem
        if pygame.sprite.spritecollide(personagem, tiros_inimigos, True):
            personagem.levar_dano()
        if pygame.sprite.spritecollide(personagem, tiros_chefe, True):
            personagem.levar_dano()

        # Verifica se todos os inimigos e o chefe foram derrotados
        if not inimigos and not chefe and not personagem.vitoria:
            canal.pause()
            canal2.play(som2)
            personagem.vitoria = True
            tempo_vitoria = pygame.time.get_ticks()
            todos_sprites.add(papel)

        if personagem.vitoria:

            if pygame.time.get_ticks() - tempo_vitoria >= 5000:  # 5 segundos
                rodando = False
                import fase3_parte3
                fase3_parte3.jogo()

        if pygame.sprite.collide_rect(personagem, papel):
            carrega_vidas.mostrar_dica_fase3 = True
            todos_sprites.remove(papel)


        todos_sprites.update()
        tiros.update()
        tiros_inimigos.update()
        tiros_chefe.update()

        todos_sprites.draw(screen)
        tiros.draw(screen)
        tiros_inimigos.draw(screen)
        tiros_chefe.draw(screen)

        desenhar_vidas(screen, personagem.vidas)

        if carrega_vidas.mostrar_dica_fase3:
            desenhar_dica(screen)


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

jogo1()
