import curses
import random

# --- Constants ---
# Screen dimensions (not directly used if using getmaxyx for main game window, but good for reference)
SCREEN_HEIGHT = 20
SCREEN_WIDTH = 60

# Game Speed Parameters
INITIAL_SNAKE_SPEED = 200  # Initial delay in milliseconds (slower start)
MIN_SNAKE_SPEED = 60       # Minimum delay in milliseconds (fastest speed)
SPEED_INCREMENT_INTERVAL = 5 # Score interval at which speed increases
SPEED_DECREMENT_AMOUNT = 15 # Amount (ms) by which delay decreases when speeding up

# --- Helper Functions ---
def create_food(snake, screen_height, screen_width):
    """
    Generates coordinates for a new food item.
    Ensures food does not spawn on the snake's body or on the border.
    """
    # Food should be placed within the bordered area (1 to height-2, 1 to width-2)
    food_y, food_x = -1, -1
    while True:
        food_y = random.randint(1, screen_height - 2) # Min y=1, Max y=sh-2
        food_x = random.randint(1, screen_width - 2)  # Min x=1, Max x=sw-2
        if [food_y, food_x] not in snake:
            break
    return [food_y, food_x]

# --- Main Game Function ---
def main(stdscr):
    """
    Main function to run the Snake game.
    stdscr: The main window object provided by curses.wrapper.
    """
    # --- Initial Curses Setup ---
    curses.curs_set(0)  # Hide the actual terminal cursor
    sh, sw = stdscr.getmaxyx() # Get screen height and width

    # --- Start Screen ---
    stdscr.clear() # Clear screen before showing start messages
    title_msg = "SNAKE GAME"
    instr_msg1 = "Use ARROW KEYS to move the snake."
    instr_msg2 = "Eat the food to grow and score."
    instr_msg3 = "Avoid hitting the walls or yourself!"
    instr_msg4 = "Press any key to start..."

    stdscr.addstr(sh // 2 - 4, sw // 2 - len(title_msg) // 2, title_msg)
    stdscr.addstr(sh // 2 - 2, sw // 2 - len(instr_msg1) // 2, instr_msg1)
    stdscr.addstr(sh // 2 - 1, sw // 2 - len(instr_msg2) // 2, instr_msg2)
    stdscr.addstr(sh // 2, sw // 2 - len(instr_msg3) // 2, instr_msg3)
    stdscr.addstr(sh // 2 + 2, sw // 2 - len(instr_msg4) // 2, instr_msg4)

    stdscr.refresh() # Display the start screen
    stdscr.nodelay(0) # Make getch() blocking to wait for user input
    stdscr.getch()    # Wait for any key press to start
    stdscr.nodelay(1) # Restore non-blocking getch() for the game loop

    # --- Game Initialization ---
    # Speed
    current_speed = INITIAL_SNAKE_SPEED
    stdscr.timeout(current_speed)  # Set initial game speed (delay for getch)

    # Snake
    # Snake body is a list of [y, x] coordinates. Head is at snake[0].
    # Starts near center-left, 3 segments long, moving right.
    snake = [
        [sh // 2, sw // 4 + 2], # Head
        [sh // 2, sw // 4 + 1],
        [sh // 2, sw // 4 + 0]  # Tail
    ]
    direction = curses.KEY_RIGHT # Initial snake direction

    # Food
    food = create_food(snake, sh, sw)

    # Score
    score = 0

    # Game State
    game_over = False

    # --- Main Game Loop ---
    while not game_over:
        # --- Input Handling ---
        # Store previous direction to prevent direct reversal.
        # getch() is non-blocking due to stdscr.nodelay(1) and stdscr.timeout().
        prev_direction = direction
        key = stdscr.getch()

        if key != curses.ERR: # If a key was pressed
            if key == curses.KEY_UP and prev_direction != curses.KEY_DOWN:
                direction = curses.KEY_UP
            elif key == curses.KEY_DOWN and prev_direction != curses.KEY_UP:
                direction = curses.KEY_DOWN
            elif key == curses.KEY_LEFT and prev_direction != curses.KEY_RIGHT:
                direction = curses.KEY_LEFT
            elif key == curses.KEY_RIGHT and prev_direction != curses.KEY_LEFT:
                direction = curses.KEY_RIGHT

        # --- Snake Movement Calculation ---
        head_y, head_x = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head_y, head_x + 1]
        elif direction == curses.KEY_LEFT:
            new_head = [head_y, head_x - 1]
        elif direction == curses.KEY_UP:
            new_head = [head_y - 1, head_x]
        elif direction == curses.KEY_DOWN:
            new_head = [head_y + 1, head_x]
        # else: # This case should ideally not be reached if direction is always valid
        #    new_head = [head_y, head_x + 1] # Default movement

        # --- Collision Detection ---
        # Wall collision (checks if new_head is outside the playable area inside the border)
        if not (1 <= new_head[0] < sh - 1 and 1 <= new_head[1] < sw - 1):
            game_over = True
            continue # Skip current iteration, proceed to game over sequence

        # Self-collision (checks if new_head is already in the snake's body)
        if new_head in snake:
            game_over = True
            continue # Skip current iteration, proceed to game over sequence

        # --- Update Game State (if no collision) ---
        snake.insert(0, new_head) # Add new head to the snake

        # Food consumption and snake growth
        if new_head == food:
            food = create_food(snake, sh, sw) # Generate new food
            score += 1 # Increment score

            # Dynamic speed adjustment
            if score % SPEED_INCREMENT_INTERVAL == 0:
                current_speed = max(MIN_SNAKE_SPEED, current_speed - SPEED_DECREMENT_AMOUNT)
                stdscr.timeout(current_speed) # Update game speed
        else:
            snake.pop() # Remove tail if no food was eaten (snake maintains length)

        # --- Drawing / Rendering ---
        stdscr.clear() # Clear screen for new frame

        # Draw border (around the entire window)
        stdscr.border(0)

        # Display score (top-left, inside the border)
        score_text = f"Score: {score}"
        stdscr.addstr(0, 2, score_text)

        # Display food (using ACS_DIAMOND character)
        try:
            if 1 <= food[0] < sh -1 and 1 <= food[1] < sw -1: # Check bounds just in case
                 stdscr.addch(food[0], food[1], curses.ACS_DIAMOND)
        except curses.error:
            pass # Ignore error if food char can't be placed (should be rare)

        # Display snake (using ACS_CKBOARD character for segments)
        for segment_y, segment_x in snake:
            try:
                if 1 <= segment_y < sh -1 and 1 <= segment_x < sw -1: # Check bounds
                    stdscr.addch(segment_y, segment_x, curses.ACS_CKBOARD)
            except curses.error:
                pass # Ignore error if snake char can't be placed

        stdscr.refresh() # Refresh screen to show all updates

    # --- Game Over Sequence ---
    if game_over:
        stdscr.clear()
        stdscr.border(0) # Re-draw border for the game over screen
        final_score_msg = f"Game Over! Your Score: {score}"

        # Calculate position for the message to be centered
        msg_y = sh // 2
        msg_x = sw // 2 - len(final_score_msg) // 2
        stdscr.addstr(msg_y, msg_x, final_score_msg)

        stdscr.nodelay(0)  # Make getch() blocking to wait for a key press
        stdscr.refresh()   # Show game over message
        stdscr.getch()     # Wait for a key press before exiting

# --- Script Execution ---
if __name__ == "__main__":
    # curses.wrapper initializes curses, calls main(), and handles cleanup
    curses.wrapper(main)
