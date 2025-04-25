import pygame
import random

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#BANCO DE QUESTÕES
bq = [
            {
                "imagem": pygame.image.load("1.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Interpretação crítica de dados estatísticos",
                "nivel": 2,
                "dica": pygame.image.load("1D.png")
            },
            {
                "imagem": pygame.image.load("2.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Interpretação crítica de dados estatísticos",
                "nivel": 1,
                "dica": pygame.image.load("2D.png")
            },
            {
                "imagem": pygame.image.load("3.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Tomada de decisões baseada em probabilidades no cotidiano",
                "nivel": 1,
                "dica": pygame.image.load("3D.png")
            },
            {
                "imagem": pygame.image.load("4.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Tomada de decisões baseada em probabilidades no cotidiano",
                "nivel": 1,
                "dica": pygame.image.load("4D.png")
            },
            {
                "imagem": pygame.image.load("5.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Estatística aplicada à pesquisa e comunicação de dados",
                "nivel": 1,
                "dica": pygame.image.load("5D.png")
            },
            {
                "imagem": pygame.image.load("6.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Estatística aplicada à pesquisa e comunicação de dados",
                "nivel": 1,
                "dica": pygame.image.load("6D.png")
            },
            {
                "imagem": pygame.image.load("7.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Combinatória e princípios de contagem",
                "nivel": 2,
                "dica": pygame.image.load("7D.png")
            },
            {
                "imagem": pygame.image.load("8.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Combinatória e princípios de contagem",
                "nivel": 2,
                "dica": pygame.image.load("8D.png")
            },
            {
                "imagem": pygame.image.load("9.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Introdução à probabilidade e contagem de eventos aleatórios",
                "nivel": 2,
                "dica": pygame.image.load("9D.png")
            },
            {
                "imagem": pygame.image.load("10.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Introdução à probabilidade e contagem de eventos aleatórios",
                "nivel": 2,
                "dica": pygame.image.load("10D.png")
            },
            {
                "imagem": pygame.image.load("11.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Probabilidade e análise de eventos em experimentos sucessivos",
                "nivel": 3,
                "dica": pygame.image.load("11D.png")
            },
            {
                "imagem": pygame.image.load("12.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Probabilidade e análise de eventos em experimentos sucessivos",
                "nivel": 3,
                "dica": pygame.image.load("12D.png")
            },
            {
                "imagem": pygame.image.load("13.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Cálculo das medidas de tendência central e de dispersão",
                "nivel": 1,
                "dica": pygame.image.load("13D.png")
            },
            {
                "imagem": pygame.image.load("14.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Cálculo das medidas de tendência central e de dispersão",
                "nivel": 1,
                "dica": pygame.image.load("14D.png")
            },
            {
                "imagem": pygame.image.load("15.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Construção e interpretação de tabelas e gráficos de frequências",
                "nivel": 1,
                "dica": pygame.image.load("15D.png")
            },
            {
                "imagem": pygame.image.load("16.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Construção e interpretação de tabelas e gráficos de frequências",
                "nivel": 1,
                "dica": pygame.image.load("16D.png")
            },
            {
                "imagem": pygame.image.load("17.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Interpretação de conjuntos de dados",
                "nivel": 2,
                "dica": pygame.image.load("17D.png")
            },
            {
                "imagem": pygame.image.load("18.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Interpretação de conjuntos de dados",
                "nivel": 2,
                "dica": pygame.image.load("18D.png")
            },
            {
                "imagem": pygame.image.load("19.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Identificação de espaços amostrais e cálculo de probabilidades",
                "nivel": 2,
                "dica": pygame.image.load("19D.png")
            },
            {
                "imagem": pygame.image.load("20.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Identificação de espaços amostrais e cálculo de probabilidades",
                "nivel": 3,
                "dica": pygame.image.load("20D.png")
            },
        ]


vidas_personagem = 3


# FASE 1

mostrar_dica_fase1 = False

#FEEDBACK
lista_fase1 = []
lista_acerto_fase1 = []

#SELECIONA AS QUESTÕES E DICAS
quest_fase1 = []

for i in list(range(len(bq))):
    if bq[i]['nivel'] == 1:
        quest_fase1.append(i)

selec1 = random.sample(quest_fase1, 3)


# FASE 2

mostrar_dica_fase2 = False

#FEEDBACK
lista_fase2 = []
lista_acerto_fase2 = []

#SELECIONA AS QUESTÕES E DICAS
quest_fase2 = []

for i in list(range(20)):
    if bq[i]['nivel'] == 2:
        quest_fase2.append(i)

selec2 = random.sample(quest_fase2, 3)


# FASE 3

mostrar_dica_fase3 = False

#FEEDBACK
lista_fase3 = []
lista_acerto_fase3 = []

# SELECIONA AS QUESTÕES E DICAS
quest_fase3 = []

for i in list(range(20)):
    if bq[i]['nivel'] == 3:
        quest_fase3.append(i)

dif = [x for x in quest_fase2 if x not in selec2]
selec3 = quest_fase3 + random.sample((dif), 1)

