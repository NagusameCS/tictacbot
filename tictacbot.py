#==================================================
# ___    __     ___       __      __   __  ___
#  |  | /  `     |   /\  /  `    |__) /  \  | 
#  |  | \__,     |  /~~\ \__,    |__) \__/  | 
#==================================================
# NagusameCS
#==================================================


import pyautogui
pyautogui.FAILSAFE = False
import cv2
import numpy as np
from PIL import ImageGrab, Image, ImageDraw
import os
import time
import json

# Global variables to track moves, board area, and settings
board_area = None
settings = {
    "sensitivity": 0.8,
    "delay_between_moves": 0.5  # Reduced delay for faster gameplay
}

# Load or initialize game stats
stats_file = "game_stats.json"
default_stats = {"wins": 0, "losses": 0, "draws": 0, "moves_played": 0}

if os.path.exists(stats_file):
    with open(stats_file, "r") as f:
        game_stats = json.load(f)
    # Ensure all required keys are present
    for key, value in default_stats.items():
        if key not in game_stats:
            game_stats[key] = value
else:
    game_stats = default_stats.copy()

def save_stats():
    """Save game stats to a file."""
    with open(stats_file, "w") as f:
        json.dump(game_stats, f, indent=4)

def capture_screen(region=None):
    """
    Captures a screenshot of the specified region.
    If no region is specified, captures the entire screen.
    :param region: Tuple (x, y, width, height) defining the region to capture.
    :return: Captured image as a numpy array.
    """
    screenshot = ImageGrab.grab(bbox=region)
    return np.array(screenshot)

def detect_game_board(image):
    """
    Detects the Tic-Tac-Toe board using the board template and divides it into 9 cells.
    :param image: Screenshot image as a numpy array.
    :return: 2D array representing the board state and grid coordinates.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    board_template_path = os.path.join("templates", "bT.png")
    board_template = cv2.imread(board_template_path, 0)
    if board_template is None:
        raise FileNotFoundError(f"Board template not found at {board_template_path}")

    res = cv2.matchTemplate(gray, board_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < settings["sensitivity"]:
        raise ValueError("Board template not detected. Ensure the game is visible on the screen.")

    x_min, y_min = max_loc
    x_max, y_max = x_min + board_template.shape[1], y_min + board_template.shape[0]
    cell_width = (x_max - x_min) // 3
    cell_height = (y_max - y_min) // 3

    return [[' ' for _ in range(3)] for _ in range(3)], (x_min, y_min, cell_width, cell_height)

def evaluate_board_state(image, grid_info):
    """
    Evaluates the current state of the board by checking each cell for X or O.
    :param image: Screenshot image as a numpy array.
    :param grid_info: Tuple (x_min, y_min, cell_width, cell_height) of the grid.
    :return: Updated 2D array representing the board state.
    """
    x_min, y_min, cell_width, cell_height = grid_info
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x_template = cv2.imread(os.path.join("templates", "xT.png"), 0)
    o_template = cv2.imread(os.path.join("templates", "oT.png"), 0)

    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in range(3):
        for col in range(3):
            x1, y1 = x_min + col * cell_width, y_min + row * cell_height
            x2, y2 = x1 + cell_width, y1 + cell_height
            cell = gray[y1:y2, x1:x2]

            if np.max(cv2.matchTemplate(cell, x_template, cv2.TM_CCOEFF_NORMED)) > settings["sensitivity"]:
                board[row][col] = 'X'
            elif np.max(cv2.matchTemplate(cell, o_template, cv2.TM_CCOEFF_NORMED)) > settings["sensitivity"]:
                board[row][col] = 'O'

    return board

def detect_winner(image):
    """
    Detects if there is a winner or a draw using the win templates.
    :param image: Screenshot image as a numpy array.
    :return: 'X', 'O', 'Draw', or None if no winner is detected.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templates = {"X": "xwT.png", "O": "owT.png", "Draw": "oxT.png"}

    for result, template_path in templates.items():
        template = cv2.imread(os.path.join("templates", template_path), 0)
        if template is None:
            raise FileNotFoundError(f"Template {template_path} not found in the 'templates' folder.")
        if np.max(cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)) > settings["sensitivity"]:
            return result
    return None

def compute_best_move(board):
    """
    Computes the best move using an enhanced Minimax algorithm with forward-thinking.
    Evaluates paths to maximize the bot's chances of winning while accounting for the opponent's moves.
    :param board: 2D array representing the current board state.
    :return: Tuple (row, col) for the best move.
    """
    def minimax(board, depth, is_maximizing, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning to evaluate the best move.
        :param board: Current board state.
        :param depth: Current depth of the search tree.
        :param is_maximizing: True if the bot is maximizing its score, False if minimizing.
        :param alpha: Best value that the maximizer currently can guarantee.
        :param beta: Best value that the minimizer currently can guarantee.
        :return: Score of the board state.
        """
        if check_winner(board, 'X'):
            return -10 + depth  # Penalize for opponent win
        if check_winner(board, 'O'):
            return 10 - depth  # Reward for bot win
        if is_draw(board):
            return 0  # Neutral score for a draw

        if is_maximizing:
            max_eval = -float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = 'O'  # Simulate bot move
                        eval = minimax(board, depth + 1, False, alpha, beta)
                        board[r][c] = ' '  # Undo move
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break  # Prune the branch
            return max_eval
        else:
            min_eval = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == ' ':
                        board[r][c] = 'X'  # Simulate opponent move
                        eval = minimax(board, depth + 1, True, alpha, beta)
                        board[r][c] = ' '  # Undo move
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break  # Prune the branch
            return min_eval

    # Check for immediate victories or blocks
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                # Check for immediate victory
                board[r][c] = 'O'
                if check_winner(board, 'O'):
                    board[r][c] = ' '  # Undo move
                    print(f"Immediate victory move found at (row: {r}, col: {c})")
                    return (r, c)
                board[r][c] = ' '

                # Check for immediate block
                board[r][c] = 'X'
                if check_winner(board, 'X'):
                    board[r][c] = ' '  # Undo move
                    print(f"Immediate block move found at (row: {r}, col: {c})")
                    return (r, c)
                board[r][c] = ' '

    # Use Minimax to find the best move by simulating multiple moves ahead
    best_score = -float('inf')
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'O'  # Simulate bot move
                score = minimax(board, 0, False, -float('inf'), float('inf'))
                board[r][c] = ' '  # Undo move
                if score > best_score:
                    best_score = score
                    best_move = (r, c)

    if best_move:
        print(f"Best move determined by forward-thinking: (row: {best_move[0]}, col: {best_move[1]})")
    else:
        print("No valid move found.")
    return best_move

def map_board_to_screen(board, grid_info):
    """
    Maps the board grid to screen coordinates dynamically based on the detected grid.
    :param board: 2D array representing the board state.
    :param grid_info: Tuple (x_min, y_min, cell_width, cell_height) of the grid.
    :return: Dictionary mapping (row, col) to screen coordinates.
    """
    x_min, y_min, cell_width, cell_height = grid_info
    mapping = {}
    for row in range(3):
        for col in range(3):
            x = x_min + col * cell_width + cell_width // 2
            y = y_min + row * cell_height + cell_height // 2
            mapping[(row, col)] = (x, y)
    return mapping

def smooth_move_to(x, y, duration=None):
    """
    Instantly moves the mouse to the specified coordinates.
    :param x: Target x-coordinate.
    :param y: Target y-coordinate.
    :param duration: Ignored for instant movement.
    """
    pyautogui.moveTo(x, y)

def click_on_cell(coords):
    """
    Simulates a mouse movement to the specified screen coordinates and double-clicks on the cell.
    :param coords: Tuple (x, y) representing the screen coordinates.
    """
    try:
        smooth_move_to(coords[0], coords[1])
        pyautogui.click(x=coords[0], y=coords[1], clicks=2, interval=0.1)
    except Exception as e:
        print(f"Error clicking on cell: {e}")

def check_winner(board, player):
    """
    Checks if the given player has won.
    :param board: 2D array representing the board state.
    :param player: 'X' or 'O'.
    :return: True if the player has won, False otherwise.
    """
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """
    Checks if the game is a draw.
    :param board: 2D array representing the board state.
    :return: True if the game is a draw, False otherwise.
    """
    return all(cell != ' ' for row in board for cell in row)

def reset_game(grid_info):
    """
    Clicks the center of the grid to reset the game state.
    :param grid_info: Tuple (x_min, y_min, cell_width, cell_height) of the grid.
    """
    x_min, y_min, cell_width, cell_height = grid_info
    center_x = x_min + (3 * cell_width) // 2
    center_y = y_min + (3 * cell_height) // 2
    print("Resetting the game by clicking the center of the grid.")
    click_on_cell((center_x, center_y))

def main():
    """
    Main function to run the Tic-Tac-Toe bot.
    """
    global board_area

    screenshot = capture_screen()

    if board_area is None:
        try:
            board, board_area = detect_game_board(screenshot)
            print("Board detected. Starting game.")
        except Exception as e:
            print(f"Error detecting game board: {e}")
            return
    else:
        board = evaluate_board_state(screenshot, board_area)

    winner = detect_winner(screenshot)
    if winner:
        print(f"Game over! Result: {winner}")
        if winner == 'X':
            game_stats["losses"] += 1
        elif winner == 'O':
            game_stats["wins"] += 1
        elif winner == 'Draw':
            game_stats["draws"] += 1
        save_stats()
        reset_game(board_area)  # Reset the game after detecting the result
        return

    move = compute_best_move(board)
    if move:
        print(f"Best move determined: {move} (row: {move[0]}, col: {move[1]})")
        screen_mapping = map_board_to_screen(board, board_area)
        if move in screen_mapping:
            click_on_cell(screen_mapping[move])
            print(f"Clicked on cell (row: {move[0]}, col: {move[1]}).")
            game_stats["moves_played"] += 1
            save_stats()
        else:
            print(f"Error: Move {move} not found in screen mapping.")
    else:
        print("No valid move found.")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(settings["delay_between_moves"])
