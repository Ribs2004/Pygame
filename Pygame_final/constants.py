import pygame

pygame.init()

# Dimensões da tela #
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
GAME_TITLE = "Undertale Battle"

# Variaveis do jogo #
PLAYER_LIVES = 3
TIME_BEWTEEN_LEVELS = 4000

LEVELS = {
    1: {
        "length": 40000
    },
    2: {
        "length": 60000
    },
    3: {
        "length": 120000
    },
}

# Cores #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Imagens #
HEART_IMG = pygame.image.load("assets/images/heart.png")
HEART_INVICIBLE_IMG = pygame.image.load("assets/images/heart_invicible.png")
BOSS_IMG = pygame.image.load("assets/images/boss.png")
BOSS_IMG = pygame.transform.scale(BOSS_IMG, (BOSS_IMG.get_width() // 3, BOSS_IMG.get_height() // 3))
DANGER_IMG = pygame.image.load("assets/images/danger.png")

# Fontes #
FONT_30 = pygame.font.Font("freesansbold.ttf", 30)
FONT_50 = pygame.font.Font("freesansbold.ttf", 50)
FONT_100 = pygame.font.Font("freesansbold.ttf", 100)
FONT_150 = pygame.font.Font("freesansbold.ttf", 150)

# Sons #
BACKGROUND_MUSIC = pygame.mixer.Sound("assets/sounds/background_music.mp3")
LOST_SOUND = pygame.mixer.Sound("assets/sounds/lost.mp3")
HURT_SOUND = pygame.mixer.Sound("assets/sounds/hurt.wav")
