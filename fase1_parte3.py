import pygame
import sys
import carrega_vidas

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("fase1_parte3")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
pedra_img = pygame.image.load('pedra.png').convert_alpha()
chao_img = pygame.image.load('tijolo.png').convert_alpha()
cacto_img = pygame.image.load('cacto.png').convert_alpha()
placa_img = pygame.image.load('placa2.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()
dica_img = pygame.image.load('dica.png')
farao_img = pygame.image.load('farao.png')
aviso_img = pygame.image.load('aviso3.png').convert_alpha()

# Cores
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

som = pygame.mixer.Sound('8-bit-arcade-138828.ogg')
canal = pygame.mixer.Channel(0)

lista_certo = []
lista_errado = []
lista1 = []

# Classe do Personagem Principal
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = perso_parado_d
        self.rect = self.image.get_rect()
        self.rect.x = 300  # Centralizar na tela
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
        self.vidas = carrega_vidas.vidas_personagem

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

    def update(self, movimento, plataformas, chaos, placas, faraos):
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
                self.levar_dano()

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
                self.levar_dano()
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

        # Quando solta a tecla, volta ao sprite parado
        if movimento == 0:
            if self.ultima_tecla == pygame.K_LEFT:
                self.image = perso_parado_e
            else:
                self.image = perso_parado_d

        # Efeito de Dano: Deixa a imagem vermelha por 1 segundo
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
    def __init__(self, x, y, a, b):
        super().__init__()
        self.image = pygame.transform.scale(chao_img, (a, b))
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
            screen.blit(carrega_vidas.bq[carrega_vidas.selec1[0]]['dica'], (0, SCREEN_HEIGHT // 4))
            screen.blit(carrega_vidas.bq[carrega_vidas.selec1[1]]['dica'], (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))

class NPC(Personagem): # NPC herda a classe Personagem
    def __init__(self, x, y, personagem):
        super().__init__()
        self.image = farao_img
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
        self.questoes = [carrega_vidas.bq[i] for i in carrega_vidas.selec1]

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
                    lista1.append(questao["tema"])
                    lista_certo.append('certo')
                else:
                    self.estado_feedback = 'errada_1'
                    self.tempo_estado = pygame.time.get_ticks() + 10000  # 10s
                    self.personagem.levar_dano()
                    self.contador_errado += 1
                    lista1.append(questao["tema"])
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
    for camada in parallax:
        posicao = -deslocamento % largura_tela
        tela.blit(camada, (posicao, 0))
        tela.blit(camada, (posicao - largura_tela, 0))

# Função para desenhar as vidas na tela
def desenhar_vidas(tela, vidas):
    for i in range(vidas):
        tela.blit(vida_img, (10 + i * 40, 10))  # Exibe os corações no topo

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
        carrega_vidas.lista_fase1 = lista1
        carrega_vidas.lista_acerto_fase1 = lista_certo


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    x, y = event.pos
                    #print(f"Posição do mouse: X={x}, Y={y}")
                    if (329 > x > 199) & (712 > y > 653):
                        import carrega_vidas
                        import fase2_parte1
                        fase2_parte1.jogo(carrega_vidas.vidas_personagem)

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
        carrega_vidas.lista_fase1 = lista1
        carrega_vidas.lista_acerto_fase1 = lista_certo

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
        "ceu.png",
        "deserto_fundo1.png",
        "deserto_fundo2.png",
        "deserto_perto.png"
    ]
    parallax = carregar_parallax(caminhos_imagens, SCREEN_WIDTH)

    # Inicializar sprites
    personagem = Personagem()
    plataformas = pygame.sprite.Group()
    placas = pygame.sprite.Group()
    chaos = pygame.sprite.Group()
    faraos = pygame.sprite.Group()
    papel = Papel()

    #PLACA
    posicoes_placas = [
        (500, SCREEN_HEIGHT - 120)
    ]
    for x, y in posicoes_placas:
        placas.add(Placa(x, y))

    #CHAO
    posicoes_chaos = [
        (800, SCREEN_HEIGHT - 200, 1600, 200),
        (1200, SCREEN_HEIGHT - 400, 800, 200),
        (1400, SCREEN_HEIGHT - 600, 400, 200)
    ]
    for x, y, a, b in posicoes_chaos:
        chaos.add(Chao(x,y,a,b))

    # FARAO
    posicoes_faraos = [
        (1550, SCREEN_HEIGHT - 750)
    ]
    for x, y in posicoes_faraos:
        faraos.add(NPC(x, y, personagem))

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
                farao.selecionar_opcao(mouse_pos)

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
        personagem.update(movimento, plataformas, chaos, placas, faraos)

        # Atualizar posição das plataformas em relação ao movimento
        for plataforma in plataformas:
            plataforma.rect.x -= movimento_horizontal

        for placa in placas:
            placa.rect.x -= movimento_horizontal

        for chao in chaos:
            chao.rect.x -= movimento_horizontal

        for farao in faraos:
            farao.rect.x -= movimento_horizontal

        # Desenhar fundo e sprites
        screen.fill(WHITE)
        desenhar_parallax(screen, parallax, deslocamento, SCREEN_WIDTH)
        # Desenhar plataformas e personagem
        chaos.draw(screen)
        placas.draw(screen)
        faraos.draw(screen)
        screen.blit(personagem.image, personagem.rect)


        # Detectar interação com a placa
        if pygame.sprite.collide_rect(personagem, placa):
            texto = fonte.render("Pressione S para ler", True, WHITE)
            screen.blit(texto, (placa.rect.x - 20, placa.rect.y - 50))
            if keys[pygame.K_s]:
                placa.mostrar_texto = True
                if placa.mostrar_texto:
                    placa.mostrar_mensagem()

        # Detectar interação com a NPC
        if pygame.sprite.collide_rect(personagem, farao):
            texto = fonte.render("Pressione S para responder as perguntas", True, BLACK)
            screen.blit(texto, (farao.rect.x - 40, farao.rect.y - 8))
            if keys[pygame.K_s]:
                farao.mostrar_texto = True
                if farao.mostrar_texto:
                    farao.mostrar_mensagem()

        # Desenha as vidas na tela
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


jogo()
