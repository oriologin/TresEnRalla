"""
Author: Jose L Balcazar, ORCID 0000-0003-4248-4528 
Copyleft: MIT License (https://en.wikipedia.org/wiki/MIT_License)

Headers for functions in abstract board for simple tic-tac-toe-like games, 2021.
Intended for Grau en Intel-ligencia Artificial, Programacio i Algorismes 1.
"""

# Import: 
# color GRAY; PLAYER_COLOR, NO_PLAYER
# board dimension BSIZ
from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, GRAY

# Data structure for stones
from collections import namedtuple

Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(stones_per_player=4):
    """Initialize stones and board, prepare functions to provide, act as their closure."""

    board = [[NO_PLAYER for _ in range(BSIZ)] for _ in range(BSIZ)]
    stones_list = [Stone(-1, -1, player) for player in range(len(PLAYER_COLOR)) for _ in range(stones_per_player)]
    current_player = 0
    game_end = False
    selected_stone = None  

    def stones():
        """Return iterable with the stones already played."""
        return (stone for stone in stones_list if stone.x != -1 and stone.y != -1)

    def select_st(i, j):
        """
        Select stone that current player intends to move.
        Player must select a stone of their own.
        To be called only after all stones are played.
        Report success by returning a boolean.
        """
        nonlocal selected_stone, current_player
        for stone in stones_list:
            if stone.x == i and stone.y == j and stone.color == current_player:
                print(f"Selected stone: {stone}")  # Debug
                selected_stone = stone
                return True
        print("No stone selected.")  # Debug
        return False

    def end():
        """Test whether there are 3 aligned stones."""
        # Check rows and columns
        for i in range(BSIZ):
            if all(board[i][j] == current_player for j in range(BSIZ)) or \
               all(board[j][i] == current_player for j in range(BSIZ)):
                return True

        # Check diagonals
        if all(board[i][i] == current_player for i in range(BSIZ)) or \
           all(board[i][BSIZ - 1 - i] == current_player for i in range(BSIZ)):
            return True

        return False

    def move_st(i, j):
        """
        If valid square, move the selected stone there and unselect it.
        Check for end of game, then switch to the next player if game isn't over.
        If square is not valid, do nothing and keep the stone selected.
        Returns:
            - bool indicating whether a stone is still selected,
            - the current player,
            - and a boolean indicating the end of the game.
        """
        
         
        nonlocal selected_stone, current_player, game_end, board

        print(f"Trying to move stone to ({i}, {j})")  # Depuración

        # Seleccionar automáticamente una piedra no colocada si no hay una seleccionada
        if not selected_stone:
            for stone in stones_list:
                if stone.color == current_player and stone.x == -1 and stone.y == -1:
                    selected_stone = stone
                    print(f"Auto-selected stone: {selected_stone}")  # Depuración
                    break

        # Verificar que la posición es válida y mover/colocar la piedra
        if selected_stone and 0 <= i < BSIZ and 0 <= j < BSIZ and board[i][j] == NO_PLAYER:
            print("Valid move.")  # Depuración

            # Si la piedra ya estaba colocada, liberar su posición anterior
            if selected_stone.x >= 0 and selected_stone.y >= 0:
                board[selected_stone.x][selected_stone.y] = NO_PLAYER

            # Colocar o mover la piedra a la nueva posición
            board[i][j] = selected_stone.color  # Usar el color de la piedra en lugar de current_player

            # Actualizar la posición de la piedra
            stones_list[stones_list.index(selected_stone)] = Stone(i, j, selected_stone.color)
            print(f"Updated stone: {stones_list[stones_list.index(selected_stone)]}")  # Depuración

            # Actualizar selected_stone después de mover
            selected_stone = None  # Deseleccionar la piedra

            # Verificar si el juego ha terminado
            game_end = end()

            # Cambiar al siguiente jugador si el juego no ha terminado
            if not game_end:
                current_player = 1 - current_player  # Cambiar entre 0 y 1

            # Si aún quedan piedras por colocar, el siguiente jugador debe seleccionar una
            if not game_end and selected_stone is None:
                for stone in stones_list:
                    if stone.color == current_player and stone.x == -1 and stone.y == -1:
                        selected_stone = stone
                        break  # Si hay una piedra por colocar, seleccionarla

            return False, current_player, game_end

        print("Invalid move.")  # Depuración
        return True, current_player, game_end



    def draw_txt(end=False):
        """Use ASCII characters to draw the board."""
        symbols = {NO_PLAYER: ".", 0: "X", 1: "O"}
        
        print("\nCurrent Board:")
        for i in range(BSIZ):
            print(" ".join(symbols[board[i][j]] for j in range(BSIZ)))
        
        if end:
            print(f"\nGame over! Player {symbols[current_player]} wins!")
        else:
            print(f"\nPlayer {symbols[current_player]}'s turn.")

    # Return these 4 functions to make them available to the main program
    return stones, select_st, move_st, draw_txt
