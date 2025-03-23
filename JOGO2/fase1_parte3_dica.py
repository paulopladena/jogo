import pygame
import sys
import carrega_vidas

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("jogo_fase1_parte3_dica")

# Carregar imagens
perso_parado_d = pygame.image.load('sprited1.png').convert_alpha()
perso_mov_d2 = pygame.image.load('sprited2.png').convert_alpha()
perso_mov_d3 = pygame.image.load('sprited3.png').convert_alpha()
perso_parado_e = pygame.image.load('spritee1.png').convert_alpha()
perso_mov_e2 = pygame.image.load('spritee2.png').convert_alpha()
perso_mov_e3 = pygame.image.load('spritee3.png').convert_alpha()
pedra_img = pygame.image.load('pedra.png').convert_alpha()
chao_img = pygame.image.load('tijolo.png').convert_alpha()
inimigo_img = pygame.image.load('inimigo.png').convert_alpha()
cacto_img = pygame.image.load('cacto.png').convert_alpha()
placa_img = pygame.image.load('placa2.png').convert_alpha()
vida_img = pygame.image.load('vida.png').convert_alpha()
dica_img = pygame.image.load('dica.png')
caixa_dialogo_img = pygame.image.load('caixa_dialogo.png')
farao_img = pygame.image.load('farao.png')
game_over_img = pygame.image.load('fim de jogo.png')

fonte = pygame.font.SysFont(None, 24)

# Cores
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

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
        #print(self.rect.x)
        #if self.rect.x >= 900:
            # import jogo_fase1_parte3
            # jogo_fase1_parte2.jogo2()

        # Verificar colisão horizontal com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                self.levar_dano()
                # Ajustar posição com base no movimento
                if movimento > 0:  # Indo para a direita
                    self.rect.right = plataforma.rect.left
                elif movimento < 0:  # Indo para a esquerda
                    self.rect.left = plataforma.rect.right

        # for placa in placas:
        #     if self.rect.colliderect(placa.rect):
        #         # Ajustar posição com base no movimento
        #         if movimento > 0:  # Indo para a direita
        #             self.rect.right = placa.rect.left
        #         elif movimento < 0:  # Indo para a esquerda
        #             self.rect.left = placa.rect.right

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
            screen.blit(caixa_dialogo_img, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

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
            screen.blit(caixa_dialogo_img, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

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
        self.mensagem_resposta = None  # Mensagem temporária de acerto/erro
        self.mensagem_timer = 0
        self.contador = 0
        self.personagem = personagem
        self.questoes = [
            {
                "imagem": pygame.image.load("pergunta.png"),
                "opcoes": {
                    "A": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 75, 40, 40),
                    "B": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 150, 40, 40),
                    "C": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 225, 40, 40),
                    "D": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 300, 40, 40)
                },
                "correta": "A"
            },
            {
                "imagem": pygame.image.load("pergunta2.png"),
                "opcoes": {
                    "A": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 75, 40, 40),
                    "B": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 150, 40, 40),
                    "C": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 225, 40, 40),
                    "D": pygame.Rect(SCREEN_WIDTH // 4 + 5, SCREEN_HEIGHT // 4 + 300, 40, 40)
                },
                "correta": "B"
            }
        ]

    def mostrar_mensagem(self):
        """Exibe a pergunta, as opções e a mensagem de acerto/erro."""
        questao = self.questoes[self.questao_atual]
        screen.blit(questao["imagem"], (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))

        for opcao, rect in questao["opcoes"].items():
            cor = BLACK  # Padrão: preto
            if self.resposta_selecionada:
                if opcao == self.resposta_selecionada:
                    cor = GREEN if opcao == questao["correta"] else RED  # Verde ou vermelho

            pygame.draw.rect(screen, cor, rect)  # Desenha quadrado da opção
            texto = fonte.render(opcao, True, WHITE)
            screen.blit(texto, (rect.x + 15, rect.y + 10))

        # Exibe a mensagem "Acertou!" ou "Errou!" por 1 segundo
        if self.mensagem_resposta:
            msg_texto = fonte.render(self.mensagem_resposta, True, WHITE)
            screen.blit(msg_texto, (350, 400))

            # Checa se o tempo de exibição já passou
            if pygame.time.get_ticks() > self.mensagem_timer:
                self.mensagem_resposta = None  # Limpa mensagem
                self.ir_para_proxima_pergunta()

    def selecionar_opcao(self, mouse_pos):
        """Verifica clique na opção e exibe mensagem de acerto ou erro."""
        questao = self.questoes[self.questao_atual]

        for opcao, rect in questao["opcoes"].items():
            if rect.collidepoint(mouse_pos):
                self.resposta_selecionada = opcao

                if opcao == questao["correta"]:
                    self.mensagem_resposta = " "
                    self.contador += 1
                else:
                    self.mensagem_resposta = " "
                    self.personagem.levar_dano()

                self.mensagem_timer = pygame.time.get_ticks() + 1000  # Exibe por 1 segundo
                break

    def ir_para_proxima_pergunta(self):
        """Passa para a próxima pergunta após exibir a mensagem."""
        if self.questao_atual < len(self.questoes) - 1:
            self.questao_atual += 1
            self.resposta_selecionada = None  # Reseta seleção
        if self.contador == 2:
            import carrega_vidas
            import fase2_parte1
            fase2_parte1.jogo(carrega_vidas.vidas_personagem)


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

def desenhar_dica(tela):
    tela.blit(dica_img, (10 + 4 * 40, 5))

mostrar_dica = False

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


        if keys[pygame.K_d]:
            papel.mostrar_dica = True
            if papel.mostrar_dica:
                papel.mostrar_mensagem()

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

        # **Desenha as vidas na tela**
        desenhar_dica(screen)  # Mantém a dica na tela
        desenhar_vidas(screen, personagem.vidas)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


jogo()
