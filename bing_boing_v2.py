import json
import os

# Define the options with rows and columns for possible moves
options = [
    # rows
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [25, 26, 31],
    [21, 22, 23, 24],
    [35, 36, 41, 42],
    [32, 33, 34],
    [43, 44, 45, 46],
    [51, 52, 53, 54],
    [55, 56, 61, 62],
    [63, 64, 65, 66],
    
    # columns
    [1, 5, 9, 16],
    [2, 6, 10],
    [3, 7, 11],
    [4, 8, 12, 21],
    
    [13, 25, 35],
    [14, 26, 36],
    [15, 31, 41],
    [42, 51, 55, 63],
    
    [22, 32, 44],
    [23, 33, 45],
    [24, 34, 46],
    
    [52, 56, 64],
    [53, 61, 65],
    [43, 54, 62, 66]
]

SAVE_FILE = "game_state.json"

def get_all_numbers():
    """Returns a set of all numbers in the game grid."""
    return set(num for option in options for num in option)

def save_game_state():
    """Save the current game state to a file."""
    with open(SAVE_FILE, "w") as file:
        json.dump(game_state, file)

def load_game_state():
    """Load game state from file or initialize a new game state if file does not exist."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    else:
        # Initialize all numbers as not_crossed
        return {str(num): 'not_crossed' for num in get_all_numbers()}

def mark_number(number, mark_type='bing'):
    """Marks a number as bing or boing and checks for chain reactions."""
    number = str(number)  # Convert to string for consistency
    if game_state[number] == 'not_crossed':
        game_state[number] = mark_type
        print(f"Marked {number} as '{mark_type}'")
        if mark_type == 'bing':
            check_for_boings()
        save_game_state()

def check_for_boings():
    """Checks all rows and columns for potential boings."""
    updated = True
    while updated:
        updated = False
        for option in options:
            # Convert option numbers to strings for dictionary lookup
            option_status = [game_state[str(num)] for num in option]
            not_crossed_count = sum(1 for state in option_status if state == 'not_crossed')
            
            if not_crossed_count == 1:
                # Find the uncrossed number and mark it as boing
                for num in option:
                    if game_state[str(num)] == 'not_crossed':
                        mark_number(num, 'boing')
                        updated = True
                        break

def check_boing_potential(number):
    """Calculates the boing potential for a number based on the game state."""
    boing_potential = 0
    str_number = str(number)
    
    for option in options:
        if number in option:
            # Count marked numbers in this option
            marked_count = sum(1 for num in option if game_state[str(num)] != 'not_crossed')
            if marked_count == len(option) - 1:
                boing_potential += 2  # Full boing potential
            elif marked_count > 0:
                boing_potential += 1  # Partial boing potential
    return boing_potential

def count_uncrossed_numbers(option):
    """Counts the number of uncrossed items in an option."""
    return sum(1 for num in option if game_state[str(num)] == 'not_crossed')

def select_best_option(playable_options):
    """Selects the best number to play based on maximizing boing potential."""
    best_option = None
    max_boing_potential = -1
    max_number = 0
    fewest_uncrossed = float('inf')

    for number in playable_options:
        boing_potential = check_boing_potential(number)
        
        # Find minimum uncrossed count in any option containing this number
        min_uncrossed_count = min(
            count_uncrossed_numbers(option)
            for option in options if number in option
        )

        # Count occurrences of this number
        num_occurrences = sum(1 for option in options if number in option)

        if (min_uncrossed_count < fewest_uncrossed or
            (min_uncrossed_count == fewest_uncrossed and boing_potential > max_boing_potential) or
            (min_uncrossed_count == fewest_uncrossed and boing_potential == max_boing_potential and number > max_number)):
            
            fewest_uncrossed = min_uncrossed_count
            max_boing_potential = boing_potential
            max_number = number
            best_option = number

    return best_option or max(playable_options)

def generate_options(red, white1, white2):
    """Generates possible numbers from dice rolls."""
    options = set()
    playable_numbers = {num for num in get_all_numbers() 
                       if game_state[str(num)] == 'not_crossed'}

    for white in [white1, white2]:
        # Basic arithmetic operations
        options.add(red + white)
        options.add(red - white)
        options.add(white - red)
        options.add(red * white)
        if white != 0:
            options.add(red // white)
        if red != 0:
            options.add(white // red)
        options.add(red ** white)
        options.add(white ** red)

        # Concatenations
        options.add(int(f"{red}{white}"))
        options.add(int(f"{white}{red}"))

    return sorted(num for num in options if num > 0 and num in playable_numbers)

def display_game_state():
    """Displays the current game state with counts of bings and boings."""
    print("\nCurrent game state:")
    
    # Count unique bings and boings
    bing_count = sum(1 for state in game_state.values() if state == 'bing')
    boing_count = sum(1 for state in game_state.values() if state == 'boing')
    
    # Display each row/column
    for option in options:
        display_option = []
        for num in option:
            state = game_state[str(num)]
            display_option.append(f"{num}[{'O' if state == 'boing' else 'X' if state == 'bing' else '...'}]")
        print(" | ".join(display_option))

    print(f"\nTotal bings (X): {bing_count}")
    print(f"Total boings (O): {boing_count}\n")

def initialize_game():
    """Initialize the game by either loading a saved state or starting fresh."""
    global game_state
    
    if os.path.exists(SAVE_FILE):
        while True:
            choice = input("Saved game found. Load it? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                if choice == 'y':
                    game_state = load_game_state()
                else:
                    game_state = {str(num): 'not_crossed' for num in get_all_numbers()}
                    save_game_state()
                break
            print("Please enter 'y' or 'n'")
    else:
        game_state = {str(num): 'not_crossed' for num in get_all_numbers()}
        save_game_state()

def play_game():
    """Runs the game loop."""
    print("\nEnter dice values as: red white1 white2 (e.g., '3 5 6')")
    print("Enter 'q' to quit\n")
    
    while True:
        dice_input = input("Dice values: ").strip().lower()
        if dice_input == 'q':
            break
            
        try:
            red, white1, white2 = map(int, dice_input.split())
            playable_options = generate_options(red, white1, white2)
            print("Playable options:", playable_options)

            if playable_options:
                best_choice = select_best_option(playable_options)
                print("Best choice to maximize boings:", best_choice)
                mark_number(best_choice)
                display_game_state()
            else:
                print("No valid options available.")
                
        except ValueError:
            print("Invalid input. Please enter three numbers separated by spaces (e.g., '3 5 6')")

# Initialize and start the game
print("Welcome to Bing Boing!")
initialize_game()
display_game_state()
play_game()