import sys
from game import Game
from constants import *

# Configurações da tela
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)


def menu():
    running = True
    clock = pygame.time.Clock()

    # Texto do início
    text = FONT_50.render("Aperte enter para iniciar o jogo", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while running:
        # Analisa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Mostra o texto na tela
        SCREEN.fill(BLACK)
        SCREEN.blit(text, text_rect)

        # Atualiza o display 60x por segundo
        clock.tick(60)
        pygame.display.update()

    play_game()


def game_over():
    running = True
    clock = pygame.time.Clock()

    # Texto 'Game Over'
    game_over_text = FONT_100.render("GAME OVER", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.4))

    # Texto para reiniciar
    restart_text = FONT_50.render("Aperte enter para reiniciar", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.6))

    while running:
        # Analisa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Mostra os textos na tela
        SCREEN.fill(BLACK)
        SCREEN.blit(restart_text, restart_text_rect)
        SCREEN.blit(game_over_text, game_over_text_rect)

        # Atualiza o jogo 60x por segundo
        clock.tick(60)
        pygame.display.update()

    play_game()


def winning_screen():
    running = True
    clock = pygame.time.Clock()

    # Texto "Você Ganhou"
    win_text = FONT_100.render("VOCÊ GANHOU!", True, WHITE)
    win_text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.4))

    # Texto para reiniciar
    restart_text = FONT_50.render("Aperte enter para reiniciar", True, WHITE)
    restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.6))

    while running:
        # Analisa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Mostra os textos na tela
        SCREEN.fill(BLACK)
        SCREEN.blit(restart_text, restart_text_rect)
        SCREEN.blit(win_text, win_text_rect)

        # Atualiza o jogo 60x por segundo
        clock.tick(60)
        pygame.display.update()

    play_game()


def play_game():
    running = True
    clock = pygame.time.Clock()
    game = Game()
    BACKGROUND_MUSIC.play(-1)

    while running:
        # Analisa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Armazena os botões apertados
        keys = pygame.key.get_pressed()

        # Preenche a tela de preto
        SCREEN.fill(BLACK)

        # Desenha e atualizza o jogo
        game.update(keys)
        game.draw(SCREEN)

        # Checa se o jogador tem menos de uma vida
        if game.lives < 1:
            BACKGROUND_MUSIC.stop()
            LOST_SOUND.play()
            game_over()

        # Checa se o jogo acabou
        if game.game_over:
            BACKGROUND_MUSIC.stop()
            winning_screen()

        # Atualiza o jogo 60x por segundo
        clock.tick(60)
        pygame.display.update()


menu()
