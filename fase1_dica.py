import pygame
import sys
import carrega_vidas

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("jogo_fase1_dica")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
pedra_img = pygame.image.load('pedra.png').convert_alpha()
chao_img = pygame.image.load('chao.png').convert_alpha()
mumia_img = pygame.image.load('mumia.png').convert_alpha()
cacto_img = pygame.image.load('cacto.png').convert_alpha()
bg = pygame.image.load('bg_piramide.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()
dica_img = pygame.image.load('dica.png')


# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

som = pygame.mixer.Sound('lets-dance-126506.ogg')
canal = pygame.mixer.Channel(0)

dano = None

# Classe do Personagem Principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = perso_parado_d
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = SCREEN_HEIGHT - 600
        self.velocidade_y = 0
        self.no_chao = False
        self.alternador = False
        self.ultima_tecla = None
        self.frame_delay = 10  # Número de frames antes de trocar a imagem
        self.frame_contador = 0  # Contador para controlar a troca de frame
        self.tempo_dano = None
        self.vidas = 1

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 7
            self.frame_contador += 1
            if self.frame_contador >= self.frame_delay:
                self.alternador = not self.alternador
                self.frame_contador = 0  # Reinicia o contador

            self.image = perso_mov_e2 if self.alternador else perso_mov_e3
            self.ultima_tecla = pygame.K_LEFT


        elif keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += 7
            self.frame_contador += 1
            if self.frame_contador >= self.frame_delay:
                self.alternador = not self.alternador
                self.frame_contador = 0  # Reinicia o contador

            self.image = perso_mov_d2 if self.alternador else perso_mov_d3
            self.ultima_tecla = pygame.K_RIGHT

        else:
            if self.ultima_tecla == pygame.K_LEFT:
                self.image = perso_parado_e
            else:
                self.image = perso_parado_d

        # Gravidade ajustada e limite de velocidade
        self.velocidade_y += 0.8  # Ajuste fino da gravidade
        if self.velocidade_y > 7:  # Limite de velocidade de queda
            self.velocidade_y = 7
        self.rect.y += self.velocidade_y

        # Efeito de dano
        if self.tempo_dano is not None:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_dano < 1000:
                image_temp = self.image.copy()
                image_temp.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = image_temp
            else:
                self.tempo_dano = None  # Reseta o tempo de dano

        if self.vidas < 0:
            canal.pause()
            import game_over
            game_over.tela_fim()

        # Checar colisão com chão
        colidiu_chao = pygame.sprite.spritecollide(self, chaos, False)
        if colidiu_chao and self.velocidade_y >= 0:
            self.rect.bottom = colidiu_chao[0].rect.top
            self.no_chao = True
            self.velocidade_y = 0

        # Evitar que caia do chão
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.no_chao = True
            self.velocidade_y = 0

        # Pulo
        if keys[pygame.K_SPACE] and self.no_chao:
            self.velocidade_y = -15
            self.no_chao = False

        if pygame.sprite.spritecollide(self, inimigos, False) and self.tempo_dano is None:
            self.tempo_dano = pygame.time.get_ticks()
            self.vidas -= 1

        if self.rect.y <= 10 and (self.rect.x >= 360 and self.rect.x <= 633):
            canal.pause()
            import fase1_parte2
            fase1_parte2.jogo()

    def soltar_tecla(self, key):
        """
        Define a imagem apropriada quando uma tecla é liberada.
        """
        if key == pygame.K_LEFT:
            self.image = perso_parado_e  # Imagem parada olhando para a esquerda
        elif key == pygame.K_RIGHT:
            self.image = perso_parado_d  # Imagem parada olhando para a direita

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pedra_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        super().__init__()
        self.image = pygame.transform.scale(chao_img, (a, b))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, limite_esquerdo, limite_direito, limite_cima, limite_baixo):
        super().__init__()
        self.image_original = mumia_img  # Mantemos a imagem original
        self.image = self.image_original
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = 2
        self.altura = 2
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.limite_cima = limite_cima
        self.limite_baixo = limite_baixo
        self.direcao = 1  # 1 = Direita, -1 = Esquerda

    def update(self):
        self.rect.x += self.velocidade
        self.rect.y += self.altura

        # Verifica se a direção mudou
        if self.rect.right >= self.limite_direito or self.rect.left <= self.limite_esquerdo:
            self.velocidade = -self.velocidade  # Inverte a velocidade
            self.direcao *= -1  # Inverte a direção

            # Apenas faz o flip se a direção mudou
            if self.direcao == -1:
                self.image = pygame.transform.flip(self.image_original, True, False)  # Espelha horizontalmente
            else:
                self.image = self.image_original  # Retorna à imagem normal

        # Inverter direção vertical
        if self.rect.top >= self.limite_cima or self.rect.bottom <= self.limite_baixo:
            self.altura = -self.altura


class Papel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = dica_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mostrar_dica = False
        self.mostrar_botao_ok = False

    def mostrar_mensagem(self):
        if self.mostrar_dica:
            # Desenhar caixa de diálogo com imagem
            import carrega_vidas
            screen.blit(carrega_vidas.bq[carrega_vidas.selec1[0]]['dica'], (0, SCREEN_HEIGHT//4))
            screen.blit(carrega_vidas.bq[carrega_vidas.selec1[1]]['dica'], (SCREEN_WIDTH//2, SCREEN_HEIGHT//4))


def fase1():
    global personagem, papel, inimigos, chaos, todos_sprites

    personagem = Personagem()

    papel = Papel(400, SCREEN_HEIGHT - 100)

    chao1 = Chao(500, SCREEN_HEIGHT - 300, 100, 100) #inicial
    chao2 = Chao(700, SCREEN_HEIGHT - 550, 100, 100)
    chao3 = Chao(400, SCREEN_HEIGHT - 350, 100, 100)
    chao4 = Chao(300, SCREEN_HEIGHT - 450, 100, 100)
    chao5 = Chao(800, SCREEN_HEIGHT - 150, 100, 100)
    chao6 = Chao(0, SCREEN_HEIGHT - 50, 1200, 1000)
    chaos = pygame.sprite.Group()

    lista_chaos = [chao1, chao2, chao3, chao4, chao5, chao6]
    chaos.add(lista_chaos)

    inimigo1 = Inimigo(200, SCREEN_HEIGHT - 170, 100, 750, 0, 0)
    inimigo2 = Inimigo(550, SCREEN_HEIGHT - 170, 300, 750, 0, 0)
    inimigo3 = Inimigo(350, SCREEN_HEIGHT - 170, 150, 600, 0, 0)
    inimigos = pygame.sprite.Group()

    lista_inimigos = [inimigo1, inimigo2, inimigo3]
    inimigos.add(lista_inimigos)

    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(personagem, papel, lista_inimigos, lista_chaos)

def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))  # ➜ Exibe os corações no topo

def desenhar_dica(tela):
    tela.blit(dica_img, (10 + 4 * 40, 5))


def jogo1():

    fase1()
    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
    rodando = True

    while rodando:

        screen.fill(WHITE)
        screen.blit(bg, (0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.KEYUP:
                personagem.soltar_tecla(event.key)

        # Detectar interação com o papel
        if pygame.sprite.collide_rect(personagem, papel):
            carrega_vidas.mostrar_dica_fase1 = True
            # global mostrar_dica
            # mostrar_dica = True
            todos_sprites.remove(papel)


        todos_sprites.update()
        todos_sprites.draw(screen)

        desenhar_vidas(screen, personagem.vidas)

        if carrega_vidas.mostrar_dica_fase1:
            desenhar_dica(screen)  # Mantém a dica na tela
            if keys[pygame.K_d]:
                papel.mostrar_dica = True
                if papel.mostrar_dica:
                    papel.mostrar_mensagem()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo1()
