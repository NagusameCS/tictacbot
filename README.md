==================================================
 ___    __     ___       __      __   __  ___
  |  | /  `     |   /\  /  `    |__) /  \  | 
  |  | \__,     |  /~~\ \__,    |__) \__/  | 
==================================================
 NagusameCS
==================================================

# Tic-Tac-Toe Bot

This project is a Python-based Tic-Tac-Toe bot that uses computer vision and the Minimax algorithm to play the game autonomously. The bot can detect the game board, evaluate the current state, and make optimal moves while accounting for the opponent's strategy.

## Features

- **Board Detection**: Automatically detects the Tic-Tac-Toe board on the screen using a template image.
- **Game State Evaluation**: Evaluates the current state of the board to determine the best move.
- **Optimal Gameplay**: Uses an enhanced Minimax algorithm with alpha-beta pruning to simulate multiple moves ahead and maximize winning chances.
- **Immediate Victory and Block Detection**: Prioritizes immediate victories and blocks to prevent the opponent from winning.
- **Dynamic Reevaluation**: Recalculates the best move after every opponent move.
- **Cross-Platform Support**: Works on Windows, macOS, and Linux with appropriate permissions.

## Big notes

- This current form only works on **googles tic tac toe game** however can be used on other tic tac toe games provided that you switch out the templates for their equivalents

> https://www.google.com/search?q=tictac+toe&sca_esv=cc91aa7b516a412e&source=hp&ei=uCMIaIyUJarYkPIPq4_ayQk&iflsig=ACkRmUkAAAAAaAgxyLqr24LaXR8GA6UzEm9h6Yb_YARP&ved=0ahUKEwiM0L6Y4-yMAxUqLEQIHauHNpkQ4dUDCA8&uact=5&oq=tictac+toe&gs_lp=Egdnd3Mtd2l6GgIYAyIKdGljdGFjIHRvZTIHEAAYgAQYCjIHEAAYgAQYCjIHEC4YgAQYCjIHEAAYgAQYCjIKEAAYgAQYChiLAzIKEAAYgAQYChiLAzIKEAAYgAQYChiLAzIKEAAYgAQYChiLAzIKEAAYgAQYChiLAzIQEC4YgAQYqAMYmQMYChiLA0ijDlAAWPUMcAB4AJABAJgBngGgAY8JqgEDMi44uAEDyAEA-AEBmAIKoAK-CcICBRAAGIAEwgILEC4YgAQY0QMYxwHCAhEQLhiABBiYAxioAxiaAxiLA8ICDhAuGIAEGKgDGIsDGJsDwgIIEAAYgAQYiwPCAg4QLhiABBjRAxjHARjJA8ICDhAAGIAEGJIDGIoFGIsDwgIUEC4YgAQYpgMYxwEYqAMYiwMYrwHCAg4QLhiABBioAxiLAxieA8ICChAuGIAEGNQCGArCAgsQLhiABBjHARivAZgDAJIHBDAuMTCgB5xusgcEMC4xMLgHvgk&sclient=gws-wiz&sei=uyMIaOSZJ_HGkPIPvc7hwQM

- You **must** allow the program to both view your screen and move your mouse or else it cant work
- This program is Janky on purpose as its intended as an educational resource for debugging, it is not intended to be an entirely finished product
- In its current state it will not loose a tic tac toe game

## Requirements

### Python Dependencies
- Python 3.6 or higher
- `pyautogui`
- `opencv-python`
- `numpy`
- `Pillow`

Install the dependencies using pip:
```bash
pip install pyautogui opencv-python numpy pillow
```

### System Requirements
- **Windows**: Run the script as an administrator.
- **macOS**: Grant Accessibility and Screen Recording permissions to your terminal or IDE.
- **Linux**: Ensure `xdotool` and `xinput` are installed for mouse control.

## Setup

1. Clone the repository or copy the project files to your local machine.
2. Place the required template images (`bT.png`, `xT.png`, `oT.png`, `xwT.png`, `owT.png`, `oxT.png`) in a folder named `templates` in the project directory.
3. Run the `check_permissions.py` script to ensure the necessary permissions are granted:
   ```bash
   python check_permissions.py
   ```

## Usage

1. Start the Tic-Tac-Toe game on your screen.
2. Run the bot:
   ```bash
   python tictacbot.py
   ```
3. The bot will:
   - Detect the game board.
   - Evaluate the current state of the board.
   - Make optimal moves.
   - Reset the game after detecting a winner or a draw.

## File Descriptions

### `tictacbot.py`
The main script that runs the Tic-Tac-Toe bot. It includes functions for board detection, game state evaluation, move computation, and mouse control.

### `check_permissions.py`
A utility script to check and ensure the necessary permissions are granted for the bot to function correctly on different operating systems.

### `templates/`
A folder containing the following template images:
- `bT.png`: Template for detecting the empty board.
- `xT.png`: Template for detecting the "X" symbol.
- `oT.png`: Template for detecting the "O" symbol.
- `xwT.png`: Template for detecting a win by "X".
- `owT.png`: Template for detecting a win by "O".
- `oxT.png`: Template for detecting a draw.

### `game_stats.json`
A JSON file that tracks the bot's performance, including the number of wins, losses, draws, and moves played.

## How It Works

1. **Board Detection**:
   - The bot uses OpenCV's template matching to locate the Tic-Tac-Toe board on the screen.
   - The board is divided into a 3x3 grid for further analysis.

2. **Game State Evaluation**:
   - The bot evaluates each cell of the grid to determine if it contains an "X", "O", or is empty.

3. **Move Computation**:
   - The bot uses the Minimax algorithm with alpha-beta pruning to simulate multiple moves ahead and determine the best move.
   - It prioritizes immediate victories and blocks.

4. **Mouse Control**:
   - The bot uses `pyautogui` to move the mouse and click on the appropriate cell to make its move.

5. **Game Reset**:
   - After detecting a winner or a draw, the bot clicks the center of the grid to reset the game.

## Troubleshooting

- **Board Not Detected**:
  - Ensure the `bT.png` template matches the appearance of the empty board.
  - Adjust the `sensitivity` value in the `settings` dictionary in `tictacbot.py`.

- **Mouse Not Moving**:
  - Ensure the script has the necessary permissions for mouse control.
  - On macOS, grant Accessibility permissions to your terminal or IDE.

- **Screen Capture Issues**:
  - On macOS, grant Screen Recording permissions to your terminal or IDE.

- **Performance Issues**:
  - Reduce the depth of the Minimax algorithm by modifying the `minimax` function in `tictacbot.py`.

## License

This project is licensed under the GNU3 License. See the LICENSE file for details.

## Acknowledgments

- OpenCV for image processing.
- PyAutoGUI for mouse control.
- The Minimax algorithm for decision-making.
- Myself for this program