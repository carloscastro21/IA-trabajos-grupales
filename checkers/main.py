import pygame
import sys
from math import inf

pygame.font.init()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLDEN_ROD = (218, 165, 32)
DARK_GREEN = (0, 100, 0)
GREEN= (127, 255, 0, 200)

# Constantes
CROWN = pygame.image.load('checkers/crown.png')
CROWN = pygame.transform.scale(CROWN, (50, 50))
FONT= pygame.font.SysFont('lucidabright', size= 100, bold= True)
LOST_STR= FONT.render("PERDISTE!!!", True, WHITE)
WIN_STR= FONT.render("GANASTE!!!", True, WHITE)
WIDTH = 800
HEIGHT = 800
ROWS = 8
COLUMNS = 8
SQUARE_SIZE = WIDTH // COLUMNS
INIT_BOARD = [
            ['0', 'r', '0', 'r', '0', 'r', '0', 'r'],
            ['r', '0', 'r', '0', 'r', '0', 'r', '0'],
            ['0', 'r', '0', 'r', '0', 'r', '0', 'r'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['b', '0', 'b', '0', 'b', '0', 'b', '0'],
            ['0', 'b', '0', 'b', '0', 'b', '0', 'b'],
            ['b', '0', 'b', '0', 'b', '0', 'b', '0'],]
TEST_BOARD = [
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', 'r', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', 'R', '0', '0'],
            ['0', '0', 'b', '0', 'b', '0', 'B', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0'],]
COLOR= {'r':RED, 'b':BLACK, 'R':RED, 'B':BLACK, '0':WHITE}
TURN= {0:'r', 1:'b'}
class Game:
    def __init__(self, turn, depth= 3):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Checkers")
        self.board = Board()
        self.IA_player = IA(depth)
        self.turn = turn
        self.selected_piece = None
        self.valid_moves = []
        self.selected_bool= False
        self.game_over = False
        self.winner = False
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and self.turn: #Turno del jugador
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_row_col_from_mouse(pos)
                    self.select_piece(row, col)
                    if self.selected_bool:
                        if self.move_piece(self.selected_piece[0], self.selected_piece[1], row, col):
                            self.turn= 0
                            self.board.actualization()
                    else:
                        self.select_piece(row, col)
                if not self.turn: #Turno de la IA
                    self.board.board= self.IA_player.play(self.board)
                    self.turn= 1
                    self.board.actualization()
                self.valid_game()
            self.screen.fill(WHITE) # fondo blanco
            self.draw()
            pygame.display.update()
    
    def valid_game(self):
        if self.board.get_winner() == 'r': #Si el jugador pierde
            self.game_over = True
            screen_color= RED
            result= LOST_STR
        elif self.board.get_winner() == 'b': #Si la IA pierde
            self.winner = True
            screen_color= DARK_GREEN
            result= WIN_STR
        if self.game_over or self.winner:
            pygame.time.delay(1500)
            self.screen.fill(screen_color)
            self.screen.blit(result, (WIDTH//2 - LOST_STR.get_width()//2, HEIGHT//2 - LOST_STR.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1500)
            pygame.quit()
            sys.exit()
        
    def select_piece(self, row, col):
        if self.board.get_piece(row, col) in ['b', 'B']:
            self.selected_piece = (row, col)
            self.selected_bool = True
            self.valid_moves = self.board.get_valid_moves(row, col)

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col
    
    def move_piece(self, row1, col1, row2, col2):
        if self.valid_move(row2, col2):
            self.board.move_piece(row1, col1, row2, col2)
            self.selected_piece = None
            self.selected_bool = False
            self.valid_moves = []
            return True
        return False
    
    def valid_move(self, row, col):
        return [row, col] in self.valid_moves

    def draw(self):
        self.board.draw(self.screen)
        if self.selected_piece:
            self.draw_valid_moves()
    
    def draw_valid_moves(self):
        #Pintar los casilleros con los movimientos validos con color verde transparente
        for move in self.valid_moves:
            pygame.draw.rect(self.screen, GREEN, (move[1] * SQUARE_SIZE, move[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
        if self.valid_moves != []:
            pygame.draw.rect(self.screen, DARK_GREEN, (self.selected_piece[1] * SQUARE_SIZE, self.selected_piece[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
        else:
            pygame.draw.rect(self.screen, RED, (self.selected_piece[1] * SQUARE_SIZE, self.selected_piece[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
            
class Board: # Clase que representa el tablero
    def __init__(self, board: list= INIT_BOARD):
        self.board: list = board
        self.n_reds= sum(row.count(elem) for row in self.board for elem in ['r', 'R'])
        self.n_blacks= sum(row.count(elem) for row in self.board for elem in ['b', 'B']) 
        self.weight= self.n_reds - self.n_blacks #Peso del tablero/ estado del juego
    
    def draw(self, screen: pygame.surface.Surface):
        for row in range(ROWS):
            for col in range(COLUMNS):
                square_color = GOLDEN_ROD if (row + col) % 2 == 0 else WHITE
                pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece_color = COLOR[self.board[row][col]] 
                if self.board[row][col] != '0':
                    radius = SQUARE_SIZE // 2 - 10
                    pygame.draw.circle(screen, piece_color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), radius)
                    if self.board[row][col] == 'R' or self.board[row][col] == 'B':
                        #Dibujar la corona
                        screen.blit(CROWN, (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4))
    
    def move_piece(self, row1, col1, row2, col2):
        piece= self.board[row1][col1]
        self.board[row1][col1]= '0'
        self.board[row2][col2]= piece
        eat= abs(row1 - row2) == 2 and abs(col1 - col2) == 2
        if eat:
            self.board[(row1 + row2) // 2][(col1 + col2) // 2]= '0'
        #Coronar piezas
        if row2 == 0 and piece == 'b':
            self.board[row2][col2]= 'B'
        if row2 == 7 and piece == 'r':
            self.board[row2][col2]= 'R'
        self.actualization()

    def actualization(self):
        #Actualizar el peso del tablero
        self.n_reds= sum(row.count(elem) for row in self.board for elem in ['r', 'R'])
        self.n_blacks= sum(row.count(elem) for row in self.board for elem in ['b', 'B'])
        self.weight= self.n_reds - self.n_blacks #Peso del tablero/ estado del juego

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_winner(self):
        if self.n_blacks == 0:
            return 'r'
        if self.n_reds == 0:
            return 'b'
        return '0'

    def next_posibles_states(self, piece: str):
        """
        Obtiene los estados posibles del tablero para el color de pieza dado
        """
        posibles_states = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                now_piece= self.board[row][col].lower()
                if now_piece == piece:
                    for move in self.get_valid_moves(row, col):
                        new_board = self.get_board_copy()
                        new_board.move_piece(row, col, move[0], move[1])
                        posibles_states.append(new_board)
        return posibles_states
    
    def get_board_copy(self):
        return Board([row[:] for row in self.board])
    
    def get_valid_moves(self, row, col):
        """
        Obtiene los movimientos posibles de una pieza ya sea reina o peon del juego de damas
        en la posición (row, col)
        """
        valid_moves = [] # Lista de movimientos posibles con la forma [row, col, eat = True] si se come una pieza
        piece= self.board[row][col]
        moves= []
        eat_moves= []
        targets= ['b', 'B'] if piece.lower() == 'r' else ['r', 'R']
        if piece == 'R' or piece == 'B': #Es reina
            #Mover solo en diagonales
            moves= [[row + 1, col-1], [row - 1, col-1], [row + 1, col+1], [row - 1, col+1]]
            eat_moves= [[row + 2, col-2], [row - 2, col-2], [row + 2, col+2], [row - 2, col+2]]
            eat_pieces= [[row + 1, col-1], [row - 1, col-1], [row + 1, col+1], [row - 1, col+1]]
        else: #Pieza roja o negra
            if piece == 'r': #Pieza roja
                moves= [[row + 1, col-1], [row + 1, col+1]]
                eat_moves= [[row + 2, col-2], [row + 2, col+2]]
                eat_pieces= [[row + 1, col-1], [row + 1, col+1]]
            else: #Pieza negra
                moves= [[row - 1, col-1], [row - 1, col+1]]
                eat_moves= [[row - 2, col-2], [row - 2, col+2]]
                eat_pieces= [[row - 1, col-1], [row - 1, col+1]]
        for i in range(len(moves)):
            if self.is_valid_move(moves[i][0], moves[i][1]):
                valid_moves.append(moves[i])
            if self.is_valid_move(eat_moves[i][0], eat_moves[i][1]) and self.board[eat_pieces[i][0]][eat_pieces[i][1]] in targets:
                valid_moves.append(eat_moves[i])
        return valid_moves

    def is_valid_move(self, row, col):
        return 0 <= row < ROWS and 0 <= col < COLUMNS and self.board[row][col] == '0'

class IA:
    def __init__(self, depth):
        self.depth= depth    
    #Algoritmo Minimax devuelve un tablero con el mejor movimiento de la IA
    def minimax(self, board: Board, minimizePlayer: bool, depth= 3): #minimizePlayer: True si es el turno de la IA
        now_turn= int(not minimizePlayer)
        if depth == 0 or board.get_winner() != '0' or board.next_posibles_states(TURN[now_turn]) == []:
            return board
        best_move: Board= None
        if minimizePlayer: #Es el turno de la IA
            best_value= -inf
            for move in board.next_posibles_states(TURN[now_turn]):
                value= self.minimax(move, False, depth - 1).weight
                if value > best_value:
                    best_value= value
                    best_move= move
            return best_move
        else: #Es el turno del jugador
            best_value= inf
            for move in board.next_posibles_states(TURN[now_turn]):
                value= self.minimax(move, True, depth - 1).weight
                if value < best_value:
                    best_value= value
                    best_move= move
            return best_move
        
    def minimax_alpha_beta(self, board: Board, minimizePlayer: bool, depth= 3, alpha= -inf, beta= inf): #minimizePlayer: True si es el turno de la IA
        now_turn= int(not minimizePlayer)
        if depth == 0 or board.get_winner() != '0' or board.next_posibles_states(TURN[now_turn]) == []:
            return board
        best_move: Board= None
        if minimizePlayer: #Es el turno de la IA
            best_value= -inf
            for move in board.next_posibles_states(TURN[now_turn]):
                value= self.minimax_alpha_beta(move, False, depth - 1, alpha, beta).weight
                if value > best_value:
                    best_value= value
                    best_move= move
                alpha= max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_move
        else: #Es el turno del jugador
            best_value= inf
            for move in board.next_posibles_states(TURN[now_turn]):
                value= self.minimax_alpha_beta(move, True, depth - 1, alpha, beta).weight
                if value < best_value:
                    best_value= value
                    best_move= move
                beta= min(beta, best_value)
                if beta <= alpha:
                    break
            return best_move
        

    def play(self, board):
        best_state= self.minimax_alpha_beta(board, True, self.depth)
        return best_state.board

if __name__ == '__main__':
    first= int(input('Quién juega primero? 0=IA o 1=Player : '))%2
    depth= 1 + int(input('Profundidad del árbol de Minimax(1-4): '))%5
    game = Game(first,depth)
