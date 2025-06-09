import pygame
import sys
import carrega_vidas

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fase2_parte3")

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
seta_img = pygame.image.load('placa.png').convert_alpha()
placa_img = pygame.image.load('placa2.png').convert_alpha()
aviso_img = pygame.image.load('aviso6.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()
chefe_img = pygame.image.load('pesquisador.png').convert_alpha()
dica_img = pygame.image.load('dica.png')

fonte = pygame.font.SysFont(None, 24)

# Cores
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

som = pygame.mixer.Sound('byte-blast-8-bit-arcade-music-background-music-for-video-208780.ogg')
canal = pygame.mixer.Channel(0)

lista_certo = []
lista_errado = []
lista2 = []

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
        self.vidas = carrega_vidas.vidas_personagem  # ➜ Inicia com 3 vidas

    def levar_dano(self):
        """Ativa o estado de dano e reduz uma vida."""
        if not self.dano_ativo:
            self.tempo_dano = pygame.time.get_ticks()
            self.dano_ativo = True
            self.vidas -= 1  # ➜ Perde uma vida ao levar dano
            carrega_vidas.vidas_personagem = self.vidas

            if self.vidas < 0:
                canal.pause()
                import game_over
                game_over.tela_fim()

    def update(self, movimento, plataformas, chaos, inimigos, chefes):
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


        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect) and self.velocidade_y >= 0:
                #self.rect.bottom = inimigo.rect.top
                self.velocidade_y = 0
                self.no_chao = True
                self.levar_dano()

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

class Seta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = seta_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Placa(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = placa_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mostrar_texto = False

    def mostrar_mensagem(self):
        if self.mostrar_texto:
            # Desenhar caixa de diálogo com imagem
            screen.blit(aviso_img, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

class Chao(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = chao_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Papel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dica_img
        self.rect = self.image.get_rect()
        self.mostrar_dica = False
        self.mostrar_botao_ok = False

    def mostrar_mensagem(self):
        if self.mostrar_dica:
            # Desenhar caixa de diálogo com imagem
            import carrega_vidas
            screen.blit(carrega_vidas.bq[carrega_vidas.selec2[0]]['dica'], (0, SCREEN_HEIGHT // 4))
            screen.blit(carrega_vidas.bq[carrega_vidas.selec2[1]]['dica'], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

class NPC(Personagem): # NPC herda a classe Personagem
    def __init__(self, x, y, personagem):
        super().__init__()
        self.image = chefe_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mostrar_texto = False
        self.pergunta_exibida = False
        self.questao_atual = 0
        self.resposta_selecionada = None
        self.contador_certo = 0
        self.contador_errado = 0
        self.estado_feedback = None
        self.tempo_estado = 0
        self.personagem = personagem
        self.questoes = [carrega_vidas.bq[i] for i in carrega_vidas.selec2]

    def mostrar_mensagem(self):
        questao = self.questoes[self.questao_atual]
        agora = pygame.time.get_ticks()

        if self.estado_feedback == 'correta':
            screen.blit(pygame.image.load('resposta_certa.png'), (0, 0))
            self.exibir_cronometro(agora)

            if agora > self.tempo_estado:
                self.estado_feedback = None
                self.ir_para_proxima_pergunta()

        elif self.estado_feedback == 'errada_1':
            screen.blit(pygame.image.load('resposta_errada.png'), (0, 0))
            self.exibir_cronometro(agora)

            if agora > self.tempo_estado:
                self.estado_feedback = 'errada_2'
                self.tempo_estado = agora + 10000  # exibe feedback por 10s

        elif self.estado_feedback == 'errada_2':
            screen.blit(pygame.image.load('feedback_questao.png'), (0, 0))
            screen.blit(questao["feedback"], (250, SCREEN_HEIGHT // 4))
            self.exibir_cronometro(agora)

            if agora > self.tempo_estado:
                self.estado_feedback = None
                self.ir_para_proxima_pergunta()

        else:
            # Exibe pergunta e opções
            screen.blit(questao["imagem"], (0, 0))
            for opcao, rect in questao["opcoes"].items():
                cor = WHITE
                if self.resposta_selecionada:
                    if opcao == self.resposta_selecionada:
                        cor = GREEN if opcao == questao["correta"] else RED
                pygame.draw.rect(screen, cor, rect)
                texto = fonte.render(opcao, True, BLACK)
                screen.blit(texto, (rect.x + 15, rect.y + 10))

    def selecionar_opcao(self, mouse_pos):
        """Verifica clique na opção e exibe mensagem de acerto ou erro."""

        if self.resposta_selecionada:
            return  # Impede múltiplos cliques

        questao = self.questoes[self.questao_atual]
        for opcao, rect in questao["opcoes"].items():
            if rect.collidepoint(mouse_pos):
                self.resposta_selecionada = opcao

                if opcao == questao["correta"]:
                    self.estado_feedback = 'correta'
                    self.tempo_estado = pygame.time.get_ticks() + 5000  # 5s
                    self.contador_certo += 1
                    lista2.append(questao["tema"])
                    lista_certo.append('certo')
                else:
                    self.estado_feedback = 'errada_1'
                    self.tempo_estado = pygame.time.get_ticks() + 10000  # 10s
                    self.personagem.levar_dano()
                    self.contador_errado += 1
                    lista2.append(questao["tema"])
                    lista_certo.append('errado')
                break

    def ir_para_proxima_pergunta(self):
        """Passa para a próxima pergunta após exibir a mensagem."""
        if self.questao_atual < len(self.questoes) - 1:
            self.questao_atual += 1
            self.resposta_selecionada = None  # Reseta seleção
        if self.contador_certo >= 2:
            canal.pause()
            tela_prox_fase()

    def exibir_cronometro(self, agora):
        segundos_restantes = max(0, (self.tempo_estado - agora) // 1000)
        fonte_cronometro = pygame.font.SysFont(None, 64)
        texto = fonte_cronometro.render(str(segundos_restantes), True, WHITE)
        screen.blit(texto, (SCREEN_WIDTH - 100, 20))  # canto superior direito

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

def desenhar_dica(tela):
    tela.blit(dica_img, (10 + 4 * 40, 5))

tela_fundo = pygame.image.load('proxima fase.png').convert_alpha()
tela_fundo2 = pygame.image.load('fim de jogo.png').convert_alpha()
# Fonte para texto
fonte = pygame.font.SysFont(None, 24)
fonte_grande = pygame.font.SysFont(None, 36)


def tela_prox_fase():
    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
    rodando = True

    while rodando:
        # Preencher a tela com a imagem da tela inicial

        screen.blit(tela_fundo, (0, 0))

        import carrega_vidas
        carrega_vidas.lista_fase2 = lista2
        carrega_vidas.lista_acerto_fase2 = lista_certo

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    x, y = event.pos
                    #print(f"Posição do mouse: X={x}, Y={y}")
                    if (329 > x > 199) & (712 > y > 653):
                        import carrega_vidas
                        import fase3_parte1
                        fase3_parte1.jogo(carrega_vidas.vidas_personagem)

                    if (846 > x > 705) & (707 > y > 639):
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(60)


def tela_fim():
    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
    rodando = True

    while rodando:

        screen.blit(tela_fundo2, (0, 0))

        import carrega_vidas
        carrega_vidas.lista_fase2 = lista2
        carrega_vidas.lista_acerto_fase2 = lista_certo

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    pygame.quit()
                    sys.exit()


        pygame.display.flip()
        clock.tick(60)

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
    setas = pygame.sprite.Group()
    placas = pygame.sprite.Group()
    chaos = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    chefes = pygame.sprite.Group()
    papel = Papel()

    #SETA
    posicoes_setas = [
        (1600, SCREEN_HEIGHT - 125)
    ]
    for x, y in posicoes_setas:
        setas.add(Seta(x, y))

    # PLACA
    posicoes_placas = [
        (250, SCREEN_HEIGHT - 125)
    ]
    for x, y in posicoes_placas:
        placas.add(Placa(x, y))

    # PESQUISADOR (CHEFE)
    posicoes_chefes = [
        (2200, SCREEN_HEIGHT - 195)
    ]
    for x, y in posicoes_chefes:
        chefes.add(NPC(x, y, personagem))

    #CHAO
    posicoes_chaos = [(x, SCREEN_HEIGHT - 50) for x in range(-100, 3000, 750)]
    for x, y in posicoes_chaos:
        chaos.add(Chao(x, y))

    # AGUIA
    l1 = [(500, y) for y in range(SCREEN_HEIGHT - 550, SCREEN_HEIGHT - 750, -100)]
    l2 = [(500, y) for y in range(SCREEN_HEIGHT - 200, SCREEN_HEIGHT - 250, -100)]
    l3 = [(x, SCREEN_HEIGHT - (-100 + (x - 200) // 2)) for x in range(1000, 1500, 200)]
    l4 = [(x, SCREEN_HEIGHT - (1100 - (x - 200) // 2)) for x in range(1600, 2000, 200)]


    posicoes_inimigos = l1 + l2 + l3 + l4

    for x, y in posicoes_inimigos:
        inimigos.add(Inimigo(x, y, velocidade=2, amplitude=60))

    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                chefe.selecionar_opcao(mouse_pos)

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
        personagem.update(movimento, plataformas, chaos, inimigos, chefes)

        # Atualizar posição das plataformas em relação ao movimento
        for plataforma in plataformas:
            plataforma.rect.x -= movimento_horizontal

        for seta in setas:
            seta.rect.x -= movimento_horizontal

        for placa in placas:
            placa.rect.x -= movimento_horizontal

        for chao in chaos:
            chao.rect.x -= movimento_horizontal

        for inimigo in inimigos:
            inimigo.rect.x -= movimento_horizontal

        for chefe in chefes:
            chefe.rect.x -= movimento_horizontal

        # Desenhar fundo e sprites
        screen.fill(WHITE)
        desenhar_parallax(screen, parallax, deslocamento, SCREEN_WIDTH)
        # Desenhar plataformas e personagem
        plataformas.draw(screen)
        chaos.draw(screen)
        setas.draw(screen)
        placas.draw(screen)
        inimigos.draw(screen)
        chefes.draw(screen)
        screen.blit(personagem.image, personagem.rect)

        #plataformas.update()
        inimigos.update()

        # Detectar interação com a NPC
        if pygame.sprite.collide_rect(personagem, chefe):
            texto = fonte.render("Pressione S para responder as perguntas", True, WHITE)
            screen.blit(texto, (chefe.rect.x - 100, chefe.rect.y - 8))
            if keys[pygame.K_s]:
                chefe.mostrar_texto = True
                if chefe.mostrar_texto:
                    chefe.mostrar_mensagem()

        # Desenha as vidas na tela
        desenhar_vidas(screen, personagem.vidas)

        # Detectar interação com a placa
        if pygame.sprite.collide_rect(personagem, placa):
            texto = fonte.render("Pressione S para ler", True, WHITE)
            screen.blit(texto, (placa.rect.x - 20, placa.rect.y - 50))
            if keys[pygame.K_s]:
                placa.mostrar_texto = True
                if placa.mostrar_texto:
                    placa.mostrar_mensagem()

        if carrega_vidas.mostrar_dica_fase2:
            desenhar_dica(screen)  # Mantém a dica na tela

            if keys[pygame.K_d]:
                papel.mostrar_dica = True
                if papel.mostrar_dica:
                    papel.mostrar_mensagem()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo()
