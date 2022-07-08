import sys
import copy
import pygame
import random
from pygame.locals import (
    QUIT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN
)

width, height = 600, 700
BG_COLOR = (7, 86, 115)
LINE_COLOR = (10, 10, 10)
CROSS_COLOR = (255, 0, 0)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()

board_regions = (
    # indexes 0 1 2
    ([i for i in range(0, int(width / 3))], [i for i in range(0, int(height / 3))]),
    ([i for i in range(int(width / 3), 2 * int(width / 3))], [i for i in range(0, int(height / 3))]),
    ([i for i in range(2 * int(width / 3), width)], [i for i in range(0, int(height / 3))]),
    # indexes 3 4 5
    ([i for i in range(0, int(width / 3))], [i for i in range(int(height / 3), 2 * int(height / 3))]),
    ([i for i in range(int(width / 3), 2 * int(width / 3))], [i for i in range(int(height / 3), 2 * int(height / 3))]),
    ([i for i in range(2 * int(width / 3), width)], [i for i in range(int(height / 3), 2 * int(height / 3))]),
    # indexes 6 7 8
    ([i for i in range(0, int(width / 3))], [i for i in range(2 * int(height / 3), height)]),
    ([i for i in range(int(width / 3), 2 * int(width / 3))], [i for i in range(2 * int(height / 3), height)]),
    ([i for i in range(2 * int(width / 3), width)], [i for i in range(2 * int(height / 3), height)]),
)

region_centers = (
    # regions 0 1 2
    (int(width / 3 / 2), int(height / 3 / 2)),
    (width / 3 + int(width / 3 / 2), int(height / 3 / 2)),
    (2 * width / 3 + int(width / 3 / 2), int(height / 3 / 2)),
    # regions 3 4 5
    (int(width / 3 / 2), height / 3 + int(height / 3 / 2)),
    (width / 3 + int(width / 3 / 2), height / 3 + int(height / 3 / 2)),
    (2 * width / 3 + int(width / 3 / 2), height / 3 + int(height / 3 / 2)),
    # regions 6 7 8
    (int(width / 3 / 2), 2 * height / 3 + int(height / 3 / 2)),
    (width / 3 + int(width / 3 / 2), 2 * height / 3 + int(height / 3 / 2)),
    (2 * width / 3 + int(width / 3 / 2), 2 * height / 3 + int(height / 3 / 2))
)


def draw_cross(center):
    pygame.draw.line(screen, CROSS_COLOR, center, (center[0] + 60, center[1] + 60), 15)
    pygame.draw.line(screen, CROSS_COLOR, center, (center[0] + 60, center[1] - 60), 15)
    pygame.draw.line(screen, CROSS_COLOR, center, (center[0] - 60, center[1] + 60), 15)
    pygame.draw.line(screen, CROSS_COLOR, center, (center[0] - 60, center[1] - 60), 15)


# def draw_text(text, font, color, surface, x, y):
#     textobj = font.render(text, 1, color)
#     textrect = textobj.get_rect()
#     textrect.topleft = (x, y)
#     # surface.blit(textobj, textrect)


def draw_text(text_str, font_type, font_size, font_color, placement):
    font = pygame.font.SysFont(font_type, font_size)
    text_surface = font.render(text_str, 1, font_color)
    text_rect = text_surface.get_rect()
    text_rect.center = placement
    screen.blit(text_surface, text_rect)


def text_button(str_text, color, center):
    text = pygame.font.SysFont('impact', 36)
    text_surf = text.render(str_text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = center
    screen.blit(text_surf, text_rect)
    return text_rect


class TicTacToe:
    def __init__(self):
        self.player = 'X'
        self.opponent = 'O'
        self.cells = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        # self.cells = ['X', ' ', 'X', 'O', 'X', 'O', ' ', ' ', ' ']
        self.x_user = True
        self.o_user = True
        self.x_computer_level = 0
        self.o_computer_level = 0
        self.main_menu()

    def draw_board(self):
        screen.fill(BG_COLOR)
        # Draw game lines
        pygame.draw.line(screen, LINE_COLOR, (width / 3, 20), (width / 3, height - 20), 10)
        pygame.draw.line(screen, LINE_COLOR, (2 * width / 3, 20), (2 * width / 3, height - 20), 10)
        pygame.draw.line(screen, LINE_COLOR, (20, height / 3), (width - 20, height / 3), 10)
        pygame.draw.line(screen, LINE_COLOR, (20, 2 * height / 3), (width - 20, 2 * height / 3), 10)

        # Draw the symbols according to the cells
        for index in range(9):
            if self.cells[index] == 'X':
                draw_cross(region_centers[index])
            elif self.cells[index] == 'O':
                pygame.draw.circle(screen, (0, 0, 255), region_centers[index], 70, 10)

    def toggle_player(self):
        if self.player == 'X':
            self.player = 'O'
            self.opponent = 'X'
        else:
            self.player = 'X'
            self.opponent = 'O'

    def game_over(self):
        wins = [self.cells[0:3], self.cells[3:6], self.cells[6:], self.cells[0:9:3],
                self.cells[1:9:3], self.cells[2:9:3], self.cells[0:9:4], self.cells[2:7:2]]
        if ['X', 'X', 'X', ] in wins:
            print('X wins')
            return True
        elif ['O', 'O', 'O'] in wins:
            print('O wins')
            return True
        elif self.cells.count(' ') == 0:
            print('Draw')
            return True
        else:
            return False

    def game_evaluate(self, cells):
        if self.player == 'X':
            minimizer = 'O'
        else:
            minimizer = 'X'
        wins = [cells[0:3], cells[3:6], cells[6:], cells[0:9:3],
                cells[1:9:3], cells[2:9:3], cells[0:9:4], cells[2:7:2]]
        if [self.player, self.player, self.player] in wins:
            return 10
        elif [minimizer, minimizer, minimizer] in wins:
            return -10
        elif cells.count(' ') == 0:
            return 0
        else:
            return None

    def print_cells(self):
        print('---------')
        print(f"| {self.cells[0]} {self.cells[1]} {self.cells[2]} |")
        print(f"| {self.cells[3]} {self.cells[4]} {self.cells[5]} |")
        print(f"| {self.cells[6]} {self.cells[7]} {self.cells[8]} |")
        print('---------')

    def computer_move(self):
        if self.player == 'X':
            if self.x_computer_level == 1:
                print('Making move level "easy"')
                self.computer_easy()
            elif self.x_computer_level == 2:
                print('Making move level "medium"')
                self.computer_medium()
            elif self.x_computer_level == 3:
                print('Making move level "hard"')
                self.computer_hard()
        elif self.player == 'O':
            if self.o_computer_level == 1:
                print('Making move level "easy"')
                self.computer_easy()
            elif self.o_computer_level == 2:
                print('Making move level "medium"')
                self.computer_medium()
            elif self.o_computer_level == 3:
                print('Making move level "hard"')
                self.computer_hard()
        return

    def computer_easy(self):

        while True:
            rand_index = random.randint(0, 8)

            if self.cells[rand_index] == ' ':
                self.cells[rand_index] = self.player
                self.toggle_player()
                self.print_cells()
                break

    def computer_medium(self):
        # cells = copy.deepcopy(self.cells)
        index = 0
        for cell in self.cells:
            if cell == ' ':
                cells_copy1 = copy.deepcopy(self.cells)
                cells_copy2 = copy.deepcopy(self.cells)
                cells_copy1[index] = 'X'
                cells_copy2[index] = 'O'
                # check for possible win or loss then make the move at that index
                if self.game_evaluate(cells_copy1) is not None or self.game_evaluate(cells_copy2) is not None:
                    self.cells[index] = self.player
                    self.toggle_player()
                    self.print_cells()
                    return
                del cells_copy1
                del cells_copy2
            index += 1

        # make easy random move if no immediate win or loss
        self.computer_easy()

    def computer_hard(self):
        best_index = -1
        best_eval = -10000
        for index in range(9):
            if self.cells[index] == ' ':
                self.cells[index] = self.player
                evaluation = self.min_max(self.cells, 0, False)
                self.cells[index] = ' '
                if evaluation >= best_eval:
                    best_eval = evaluation
                    best_index = index
        self.cells[best_index] = self.player
        self.toggle_player()
        self.print_cells()

    def min_max(self, cells, depth, is_max):
        # terminating condition
        if self.game_evaluate(cells) is not None:
            return self.game_evaluate(cells)

        if is_max:
            best = -1000
            for index in range(9):
                if cells[index] == ' ':
                    cells[index] = self.player
                    best = max(self.min_max(cells, depth + 1, not is_max), best)
                    cells[index] = ' '
        else:
            best = 1000
            for index in range(9):
                if cells[index] == ' ':
                    cells[index] = self.opponent
                    best = min(self.min_max(cells, depth + 1, not is_max), best)
                    cells[index] = ' '

        return best

    def main_menu(self):
        pygame.init()
        # font = pygame.font.SysFont('impact', 30)
        x_options = ' '
        o_options = ' '
        while 1:
            screen.fill((7, 86, 115))
            mouse_pos = pygame.mouse.get_pos()

            draw_text('Main Menu', 'impact', 40, LINE_COLOR, (width / 2, height / 16))

            draw_text('X   :   ' + x_options, 'impact', 40, (255, 0, 0), (width / 4, height / 6))
            draw_text('O   :   ' + o_options, 'impact', 40, (20, 20, 250), (3 * width / 4, height / 6))

            # X options
            if text_button('USER', (255, 0, 0), (width / 4, height / 6 * 2)).collidepoint(mouse_pos) and click:
                x_options = 'USER'
                self.x_user = True
                self.x_computer_level = 0
            if text_button('EASY', (255, 0, 0), (width / 4, height / 6 * 3)).collidepoint(mouse_pos) and click:
                x_options = 'EASY AI'
                self.x_user = False
                self.x_computer_level = 1
            if text_button('MEDIUM', (255, 0, 0), (width / 4, height / 6 * 4)).collidepoint(mouse_pos) and click:
                x_options = 'MEDIUM AI'
                self.x_user = False
                self.x_computer_level = 2
            if text_button('HARD', (255, 0, 0), (width / 4, height / 6 * 5)).collidepoint(mouse_pos) and click:
                x_options = 'HARD AI'
                self.x_user = False
                self.x_computer_level = 3

            # O options
            if text_button('USER', (20, 20, 250), (3 * width / 4, height / 6 * 2)).collidepoint(mouse_pos) and click:
                o_options = 'USER'
                self.o_user = True
                self.o_computer_level = 0
            if text_button('EASY', (20, 20, 250), (3 * width / 4, height / 6 * 3)).collidepoint(mouse_pos) and click:
                o_options = 'EASY AI'
                self.o_user = False
                self.o_computer_level = 1
            if text_button('MEDIUM', (20, 20, 250), (3 * width / 4, height / 6 * 4)).collidepoint(mouse_pos) and click:
                o_options = 'MEDIUM AI'
                self.o_user = False
                self.o_computer_level = 2
            if text_button('HARD', (20, 20, 250), (3 * width / 4, height / 6 * 5)).collidepoint(mouse_pos) and click:
                o_options = 'HARD AI'
                self.o_user = False
                self.o_computer_level = 3

            if text_button('START TIC TAC TOE', LINE_COLOR, (width / 2, height / 16 * 15)).collidepoint(
                    mouse_pos) and click:
                print('start the game')
                if o_options != ' ' and x_options != ' ':
                    self.game_loop()

            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            pygame.display.update()
            clock.tick(30)

    def game_loop(self):
        self.cells = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        running = True
        while running:
            self.draw_board()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for index in range(9):
                        if x in board_regions[index][0] and y in board_regions[index][1]:
                            if self.cells[index] == ' ':
                                self.cells[index] = self.player
                                self.toggle_player()
                                self.draw_board()
            if self.game_over():
                self.draw_board()
                wait_loop = True
                while wait_loop:
                    # self.draw_board()

                    for ev in pygame.event.get():
                        if ev.type == KEYDOWN or ev.type == MOUSEBUTTONDOWN:
                            wait_loop = False
                            running = False
                    pygame.display.update()
                    clock.tick(30)
            else:
                if not self.x_user:
                    self.computer_move()
                if self.game_over():
                    continue
                if not self.o_user:
                    self.computer_move()

            pygame.display.flip()
            clock.tick(30)


TicTacToe()
