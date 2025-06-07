# Curses Snake Game

## Description
A classic snake game implemented in Python using the `curses` library. The player controls a snake that moves around the screen, eating food to grow longer and score points. The game's speed increases as the score gets higher, adding to the challenge.

## Features
*   Classic snake gameplay.
*   Score tracking.
*   Progressive difficulty (speed increases with score).
*   Start screen with game title and instructions.
*   Game over screen displaying the final score.
*   Visuals rendered in the terminal using the `curses` library, including a game border and special characters for the snake and food (`curses.ACS_CKBOARD` and `curses.ACS_DIAMOND`).

## Requirements
*   Python 3.x
*   A terminal environment that supports the Python `curses` library. This is standard on Linux and macOS. For Windows, you might need to install the `windows-curses` package (`pip install windows-curses`) or run the game within the Windows Subsystem for Linux (WSL).

## How to Play
1.  **Run the script** from your terminal:
    ```bash
    python snake_game.py
    ```
2.  **Start Game:** Press any key on the start screen to begin.
3.  **Controls:** Use the **ARROW KEYS** (Up, Down, Left, Right) to change the snake's direction.
4.  **Objective:**
    *   Eat the food (typically a diamond symbol: ♦) to make the snake grow longer and increase your score.
    *   Avoid running into the game borders or the snake's own body.
5.  **Difficulty:** The game speeds up as your score increases!

## Note on Display
The game uses `curses` for text-based graphics. The appearance of certain characters (like the snake body and food) may vary slightly depending on your terminal emulator, font, and system's `curses` implementation.