import sys
import os

from player.computer import Computer
from player.human import Human

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from pygame import gfxdraw


class GUI:
    def __init__(self, game):
        self.game = game
        self.__board = self.game.board
        self.piece_size = 100
        self.slot_size = int(self.piece_size / 2) - 10
        self.rows = 6
        self.columns = 7
        board_size = (self.columns * self.piece_size, (self.rows + 1) * self.piece_size)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Connect 4')
        self.background = (34, 40, 49)
        self.foreground = (0, 191, 255)
        self.computer = (255, 215, 0)
        self.player = (242, 163, 101)
        self.font = pygame.font.SysFont('Consolas', 30)
        self.screen = pygame.display.set_mode(board_size)
        self.draw_board()
        self.run_loop()

    def run_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.listen()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        break
            break

    def listen(self):
        listening = True
        while listening:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.player_animation(event)
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    verdict = self.on_click(event)
                    if verdict is not None:
                        if verdict == 'draw':
                            self.write_draw()
                        if verdict == 'win':
                            self.write_win()
                        listening = False
                        break
                    verdict = self.computer_move()
                    if verdict is not None:
                        if verdict == 'draw':
                            self.write_draw()
                        if verdict == 'lose':
                            self.write_lose()
                        listening = False

    def player_animation(self, event):
        position = event.pos
        column = position[0]
        self.draw_top_rect()
        self.draw_circle(self.screen, self.player, column, self.slot_size + 5, self.slot_size)
        pygame.display.update()

    def computer_move(self):
        latest_move, verdict = self.game.move(self.game.player1, 1, -1, -1)
        self.draw_piece(self.game.player1, latest_move.line, latest_move.column)
        return verdict

    def get_pos(self, event):
        position = event.pos
        column = position[0] // 100
        row = self.__board.get_bottom_of_column(column)
        return row, column

    def wrong_column(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return self.get_pos(event)
                if event.type == pygame.MOUSEMOTION:
                    self.player_animation(event)

    def on_click(self, event):
        row, column = self.get_pos(event)
        verdict = None
        while row == -1:
            row, column = self.wrong_column()
        if row != -1:
            latest_move, verdict = self.game.move(self.game.player2, 2, row, column)
            self.draw_piece(self.game.player2, row, column)
        if verdict is not None:
            return verdict

    def draw_top_rect(self):
        pygame.draw.rect(self.screen, self.background, (0, 0, self.columns * self.piece_size, self.piece_size))

    def draw_circle(self, surface, color, x, y, radius, ):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def draw_board(self):
        self.screen.fill(self.background)
        for column in range(self.columns):
            for row in range(1, self.rows + 1):
                pygame.draw.rect(self.screen, self.foreground,
                                 (column * self.piece_size, row * self.piece_size, self.piece_size, self.piece_size))
                self.draw_circle(self.screen, self.background,
                                 column * self.piece_size + self.slot_size + 10,
                                 row * self.piece_size + 5 + self.slot_size,
                                 self.slot_size)
        pygame.display.update()

    def draw_piece(self, player, row, column):
        if type(player) == Computer:
            self.draw_circle(self.screen, self.computer,
                             column * self.piece_size + self.slot_size + 10,
                             (row + 1) * self.piece_size + 5 + self.slot_size,
                             self.slot_size + 1)

        if type(player) == Human and -1 < row < 6:
            self.draw_circle(self.screen, self.player,
                             column * self.piece_size + self.slot_size + 10,
                             (row + 1) * self.piece_size + 5 + self.slot_size,
                             self.slot_size + 1)

        pygame.display.update()

    def write_draw(self):
        self.draw_top_rect()
        text_surface = self.font.render("It's a draw!", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 10))
        text_surface = self.font.render("Click anywhere to play again.", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 40))
        pygame.display.update()

    def write_lose(self):
        self.draw_top_rect()
        text_surface = self.font.render("You lost!", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 10))
        text_surface = self.font.render("Click anywhere to play again.", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 40))
        pygame.display.update()

    def write_win(self):
        self.draw_top_rect()
        text_surface = self.font.render("You have won!", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 10))
        text_surface = self.font.render("Click anywhere to play again.", True, (255, 255, 255))
        self.screen.blit(text_surface, (0, 40))
        pygame.display.update()
