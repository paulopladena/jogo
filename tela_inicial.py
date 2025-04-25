import pygame
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela Inicial")

# Cores
WHITE = (255, 255, 255)

som = pygame.mixer.Sound('the-return-of-the-8-bit-era-301292.ogg')
canal = pygame.mixer.Channel(0)

tela_fundo = pygame.image.load('capa.png').convert_alpha()

def tela_tutorial():
    ativo = True
    while ativo:
        tela_tutorial = pygame.image.load('tutorial.png').convert_alpha()
        screen.blit(tela_tutorial, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                ativo = False

def tela_ini():

    clock = pygame.time.Clock()
    canal.play(som, loops=-1)
    rodando = True

    while rodando:
        # Preencher a tela com a imagem da tela inicial
        screen.blit(tela_fundo, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    x, y = event.pos
                    #print(f"Posição do mouse: X={x}, Y={y}")
                    if (610 > x > 380) & (415 > y > 360):
                        canal.pause()
                        import fase1_parte1
                        fase1_parte1.jogo()

                    if (567 > x > 425) & (572 > y > 519):
                        pygame.quit()
                        sys.exit()

                    if (631 > x > 359) & (731 > y > 672):
                        tela_tutorial()


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()
tela_ini()