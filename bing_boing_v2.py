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

def save_game_state():
    """Save the current game state to a file, converting tuple keys to strings."""
    serializable_game_state = {str(option): status for option, status in game_state.items()}
    with open(SAVE_FILE, "w") as file:
        json.dump(serializable_game_state, file)

def load_game_state():
    """Load game state from file, converting string keys back to tuples, or initialize a new game state if file does not exist."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            loaded_state = json.load(file)
            # Convert keys back to tuples
            return {tuple(map(int, key.strip("()").split(", "))): status for key, status in loaded_state.items()}
    else:
        return {tuple(option): ['not_crossed'] * len(option) for option in options}

def mark_number_in_option(number):
    """Marks a number as crossed ('bing') in all rows and columns where it appears,
    and checks for boings (completions) with full recursive support for chain reactions."""
    updated = True
    while updated:
        updated = False  # Track if any updates happen in this pass
        for option, status in game_state.items():
            if number in option:
                index = option.index(number)
                if status[index] == 'not_crossed':
                    status[index] = 'bing'  # Mark the number as crossed
                    print(f"Marked {number} in option {option} as 'bing'")
                    updated = True
                    # Check for boing recursively across all related options
                    check_for_boing(option)
        save_game_state()  # Save the game state after marking

def check_for_boing(option):
    """Checks if a row or column can have a boing and applies it, with recursive support."""
    status = game_state[option]
    not_crossed_count = sum(1 for state in status if state == 'not_crossed')
    
    # If only one item is left uncrossed, mark it as 'boing'
    if not_crossed_count == 1:
        for i, state in enumerate(status):
            if state == 'not_crossed':
                status[i] = 'boing'  # Mark the remaining item as 'boing'
                print(f"Marked {option[i]} in option {option} as 'boing'")
                propagate_boing(option[i])  # Propagate boing to all instances of this number

def propagate_boing(number):
    """Propagates the boing state to all rows/columns where the number appears, with recursive scanning for further changes."""
    updated = True
    while updated:
        updated = False
        for option, status in game_state.items():
            if number in option:
                index = option.index(number)
                if status[index] == 'not_crossed':
                    status[index] = 'boing'
                    updated = True
                    check_for_boing(option)  # Check if this marking triggers more boings

def trigger_boings(number):
    """Triggers additional boings in rows/columns that contain the given number."""
    for option, status in game_state.items():
        if number in option:
            check_for_boing(option)  # Check each option that contains the number for boings

def check_boing_potential(number):
    """Calculates the boing potential for a number based on the game state."""
    boing_potential = 0
    for option, status in game_state.items():
        if number in option:
            # Count how many entries are marked as 'crossed'
            marked_count = sum(1 for state in status if state == 'crossed')
            if marked_count == len(status) - 1:
                boing_potential += 2  # Full boing if this play completes the option
            elif marked_count > 0:
                boing_potential += 1  # Partial boing if it moves closer to completion
    return boing_potential

def count_uncrossed_numbers(option):
    """Counts the number of uncrossed items in an option (row or column)."""
    return sum(1 for state in game_state[tuple(option)] if state == 'not_crossed')

def select_best_option(playable_options):
    """Selects the best number to play based on maximizing boing potential,
       with preference given to rows/columns with the fewest uncrossed items.
       In case of ties, it prefers the highest number and prioritizes numbers in multiple lists."""
    
    best_option = None
    max_boing_potential = 0
    max_number = 0  # Track the highest number as fallback
    fewest_uncrossed = float('inf')  # Initialize with a large number for comparison

    for number in playable_options:
        boing_potential = check_boing_potential(number)
        
        # Find the minimum number of uncrossed items across rows/columns containing this number
        min_uncrossed_count = min(
            count_uncrossed_numbers(tuple(option))  # Convert option to a tuple here
            for option in options if number in option
        )

        # Count how many rows/columns contain this number
        num_occurrences = sum(1 for option in options if number in option)

        # Selection logic based on fewest uncrossed items, then boing potential, and then the highest number
        if (min_uncrossed_count < fewest_uncrossed or
            (min_uncrossed_count == fewest_uncrossed and boing_potential > max_boing_potential) or
            (min_uncrossed_count == fewest_uncrossed and boing_potential == max_boing_potential and number > max_number)):

            fewest_uncrossed = min_uncrossed_count
            max_boing_potential = boing_potential
            max_number = number
            best_option = number

    # If no options have a boing potential or uncrossed preference, default to the highest number
    if best_option is None:
        best_option = max(playable_options)

    return best_option

def generate_options(red, white1, white2):
    """Generates possible numbers from dice rolls, excluding crossed numbers."""
    options = set()
    all_distinct_numbers = get_all_distinct_uncrossed_numbers()

    # For each white die, calculate with the red die
    for white in [white1, white2]:
        # Basic arithmetic operations
        options.add(red + white)         # Addition
        options.add(red - white)         # Subtraction
        options.add(white - red)         # Subtraction in reverse
        options.add(red * white)         # Multiplication
        if white != 0:
            options.add(red // white)    # Division (integer) if white isn't zero
        if red != 0:
            options.add(white // red)    # Division in reverse if red isn't zero
        options.add(red ** white)        # Power (red^white) if within a reasonable limit
        options.add(white ** red)        # Power (white^red) if within a reasonable limit

        # Concatenations in both orders
        options.add(int(f"{red}{white}"))
        options.add(int(f"{white}{red}"))

    # Filter to include only positive, non-crossed numbers in the grid
    return sorted(filter(lambda x: x > 0 and x in all_distinct_numbers, options))

def get_all_distinct_uncrossed_numbers():
    """Returns a set of all uncrossed numbers in the game grid."""
    uncrossed_numbers = set()
    for option, status in game_state.items():
        for num, state in zip(option, status):
            if state == 'not_crossed':  # Only include uncrossed numbers
                uncrossed_numbers.add(num)
    return uncrossed_numbers

def play_game():
    """Runs the CLI game loop, prompting for dice rolls and making moves."""
    while True:
        try:
            red = int(input("Enter red die value: "))
            white1 = int(input("Enter first white die value: "))
            white2 = int(input("Enter second white die value: "))
        except ValueError:
            print("Please enter valid integer dice values.")
            continue

        # Generate playable options based on dice values
        playable_options = generate_options(red, white1, white2)
        print("Playable options:", playable_options)

        # Select the best option to maximize boings
        best_choice = select_best_option(playable_options)
        if best_choice is not None:
            print("Best choice to maximize boings:", best_choice)
            mark_number_in_option(best_choice)
            display_game_state()
        else:
            print("No valid options available.")

        # Ask to continue or exit
        if input("Roll again? (y/n): ").strip().lower() != 'y':
            break

def display_game_state():
    """Displays the current game state with rows/columns and their crossed numbers,
       and shows the total count of unique 'bing' and 'boing' states."""
    
    bing_count = set()
    boing_count = set()

    # Display each row/column and count bings and boings
    print("\nCurrent game state:")
    for option, status in game_state.items():
        display_option = []
        for num, state in zip(option, status):
            # Track unique bings and boings by number
            if state == 'bing':
                bing_count.add(num)
            elif state == 'boing':
                boing_count.add(num)
                
            # Format display for each number
            display_option.append(f"{num}[{'O' if state == 'boing' else 'X' if state == 'bing' else '...'}]")
        
        # Display the formatted row/column
        print(" | ".join(display_option))

    # Print the unique count of bings and boings
    print(f"\nTotal unique bings (X): {len(bing_count)}")
    print(f"Total unique boings (O): {len(boing_count)}\n")

# Load or initialize game state
game_state = load_game_state()
display_game_state()

# Start the game
play_game()