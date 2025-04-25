import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tela Inicial")

# Cores
WHITE = (255, 255, 255)

#som = pygame.mixer.Sound('very-lush-and-swag-loop-74140.ogg')
#canal = pygame.mixer.Channel(0)

def tela_fim():

    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        # Preencher a tela com a imagem da tela inicial

        tela_fundo = pygame.image.load('fim de jogo.png').convert_alpha()
        screen.blit(tela_fundo, (0, 0))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    pygame.quit()
                    sys.exit()


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

tela_fim()