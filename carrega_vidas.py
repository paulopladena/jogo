import pygame
import random

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# DESERTO
# 1F, 4F, 13F, 20F, 15F, 16F, 18F

# FLORESTA
# 3F, 6D, 7M, 8M, 10D, 12D, 19F

# NEVE
# 2F, 5D, 9D, 11D, 14F, 17F

# F = FÁCIL; M = MÉDIO; D = DIFÍCIL

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
                "correta": "C",
                "tema": "Interpretação crítica de dados estatísticos",
                "nivel": 1,
                "dica": pygame.image.load("12D.png"),
                "feedback": pygame.image.load("1F.png")
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
                "nivel": 3,
                "dica": pygame.image.load("12D.png"),
                "feedback": pygame.image.load("2F.png")
            },
            {
                "imagem": pygame.image.load("3.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "A",
                "tema": "Tomada de decisões baseada em probabilidades no cotidiano",
                "nivel": 2,
                "dica": pygame.image.load("34D.png"),
                "feedback": pygame.image.load("3F.png")
            },
            {
                "imagem": pygame.image.load("4.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "A",
                "tema": "Tomada de decisões baseada em probabilidades no cotidiano",
                "nivel": 1,
                "dica": pygame.image.load("34D.png"),
                "feedback": pygame.image.load("4F.png")
            },
            {
                "imagem": pygame.image.load("5.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Estatística aplicada à pesquisa e comunicação de dados",
                "nivel": 3,
                "dica": pygame.image.load("56D.png"),
                "feedback": pygame.image.load("5F.png")
            },
            {
                "imagem": pygame.image.load("6.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "A",
                "tema": "Estatística aplicada à pesquisa e comunicação de dados",
                "nivel": 2,
                "dica": pygame.image.load("56D.png"),
                "feedback": pygame.image.load("6F.png")
            },
            {
                "imagem": pygame.image.load("7.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Combinatória e princípios de contagem",
                "nivel": 2,
                "dica": pygame.image.load("78D.png"),
                "feedback": pygame.image.load("7F.png")
            },
            {
                "imagem": pygame.image.load("8.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Combinatória e princípios de contagem",
                "nivel": 2,
                "dica": pygame.image.load("78D.png"),
                "feedback": pygame.image.load("8F.png")
            },
            {
                "imagem": pygame.image.load("9.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "A",
                "tema": "Introdução à probabilidade e contagem de eventos aleatórios",
                "nivel": 3,
                "dica": pygame.image.load("910D.png"),
                "feedback": pygame.image.load("9F.png")
            },
            {
                "imagem": pygame.image.load("10.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Introdução à probabilidade e contagem de eventos aleatórios",
                "nivel": 2,
                "dica": pygame.image.load("910D.png"),
                "feedback": pygame.image.load("10F.png")
            },
            {
                "imagem": pygame.image.load("11.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "C",
                "tema": "Probabilidade e análise de eventos em experimentos sucessivos",
                "nivel": 3,
                "dica": pygame.image.load("1112D.png"),
                "feedback": pygame.image.load("11F.png")
            },
            {
                "imagem": pygame.image.load("12.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Probabilidade e análise de eventos em experimentos sucessivos",
                "nivel": 2,
                "dica": pygame.image.load("1112D.png"),
                "feedback": pygame.image.load("12F.png")
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
                "dica": pygame.image.load("1314D.png"),
                "feedback": pygame.image.load("13F.png")
            },
            {
                "imagem": pygame.image.load("14.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "D",
                "tema": "Cálculo das medidas de tendência central e de dispersão",
                "nivel": 3,
                "dica": pygame.image.load("1314D.png"),
                "feedback": pygame.image.load("14F.png")
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
                "dica": pygame.image.load("1516D.png"),
                "feedback": pygame.image.load("15F.png")
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
                "dica": pygame.image.load("1516D.png"),
                "feedback": pygame.image.load("16F.png")
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
                "nivel": 3,
                "dica": pygame.image.load("17D.png"),
                "feedback": pygame.image.load("17F.png")
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
                "nivel": 1,
                "dica": pygame.image.load("18D.png"),
                "feedback": pygame.image.load("18F.png")
            },
            {
                "imagem": pygame.image.load("19.png"),
                "opcoes": {
                    "A": pygame.Rect(0, SCREEN_HEIGHT // 4 + 175, 40, 40),
                    "B": pygame.Rect(0, SCREEN_HEIGHT // 4 + 245, 40, 40),
                    "C": pygame.Rect(0, SCREEN_HEIGHT // 4 + 315, 40, 40),
                    "D": pygame.Rect(0, SCREEN_HEIGHT // 4 + 380, 40, 40)
                },
                "correta": "B",
                "tema": "Identificação de espaços amostrais e cálculo de probabilidades",
                "nivel": 2,
                "dica": pygame.image.load("1920D.png"),
                "feedback": pygame.image.load("19F.png")
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
                "nivel": 1,
                "dica": pygame.image.load("1920D.png"),
                "feedback": pygame.image.load("20F.png")
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

# IDs das questões parecidas
parecidas = {15, 16}

# Tenta sortear até conseguir uma amostra que contenha no máximo uma das parecidas
while True:
    selec1 = random.sample(quest_fase1, 6)
    if len(parecidas.intersection(selec1)) <= 1:
        break


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

# IDs das questões parecidas
parecidas = {7, 8}

# Tenta sortear até conseguir uma amostra que contenha no máximo uma das parecidas
while True:
    selec2 = random.sample(quest_fase2, 6)
    if len(parecidas.intersection(selec2)) <= 1:
        break


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

# dif = [x for x in quest_fase2 if x not in selec2]
# selec3 = quest_fase3 + random.sample((dif), 6)
selec3 = random.sample(quest_fase3, 6)

