import json
import os
from default_strategy import DefaultStrategy

class BingBoingGame:
    """Main game class implementing the Bing Boing game logic"""
    
    OPTIONS = [
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

    def __init__(self, strategy=None, save_file="game_state.json"):
        self.save_file = save_file
        self.strategy = strategy or DefaultStrategy()
        self.game_state = None

    def initialize_game(self):
        """Initialize the game by either loading a saved state or starting fresh"""
        if os.path.exists(self.save_file):
            while True:
                choice = input("Saved game found. Load it? (y/n): ").strip().lower()
                if choice in ['y', 'n']:
                    if choice == 'y':
                        self.load_game_state()
                    else:
                        self.new_game()
                    break
                print("Please enter 'y' or 'n'")
        else:
            self.new_game()

    def new_game(self):
        """Start a new game with fresh state"""
        self.game_state = {str(num): 'not_crossed' for num in self.get_all_numbers()}
        self.save_game_state()

    def get_all_numbers(self):
        """Returns a set of all numbers in the game grid"""
        return set(num for option in self.OPTIONS for num in option)

    def save_game_state(self):
        """Save the current game state to a file"""
        with open(self.save_file, "w") as file:
            json.dump(self.game_state, file)

    def load_game_state(self):
        """Load game state from file"""
        with open(self.save_file, "r") as file:
            self.game_state = json.load(file)

    def mark_number(self, number, mark_type='bing'):
        """Mark a number and handle chain reactions"""
        number = str(number)
        if self.game_state[number] == 'not_crossed':
            self.game_state[number] = mark_type
            print(f"Marked {number} as '{mark_type}'")
            if mark_type == 'bing':
                self.check_for_boings()
            self.save_game_state()

    def check_for_boings(self):
        """Check for and handle chain reactions of boings"""
        updated = True
        while updated:
            updated = False
            for option in self.OPTIONS:
                option_status = [self.game_state[str(num)] for num in option]
                not_crossed_count = sum(1 for state in option_status if state == 'not_crossed')
                
                if not_crossed_count == 1:
                    for num in option:
                        if self.game_state[str(num)] == 'not_crossed':
                            self.mark_number(num, 'boing')
                            updated = True
                            break

    def generate_options(self, red, white1, white2):
        """Generate all possible moves from dice values"""
        options = set()
        playable_numbers = {num for num in self.get_all_numbers() 
                           if self.game_state[str(num)] == 'not_crossed'}

        for white in [white1, white2]:
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

            options.add(int(f"{red}{white}"))
            options.add(int(f"{white}{red}"))

        return sorted(num for num in options if num > 0 and num in playable_numbers)

    def display_state(self):
        """Display the current game state"""
        print("\nCurrent game state:")
        
        bing_count = sum(1 for state in self.game_state.values() if state == 'bing')
        boing_count = sum(1 for state in self.game_state.values() if state == 'boing')
        
        for option in self.OPTIONS:
            display_option = []
            for num in option:
                state = self.game_state[str(num)]
                display_option.append(f"{num}[{'O' if state == 'boing' else 'X' if state == 'bing' else '...'}]")
            print(" | ".join(display_option))

        print(f"\nTotal bings (X): {bing_count}")
        print(f"Total boings (O): {boing_count}\n")

    def play_turn(self, red, white1, white2):
        """Play a single turn with the given dice values"""
        playable_options = self.generate_options(red, white1, white2)
        print("Playable options:", playable_options)

        if playable_options:
            best_choice = self.strategy.select_best_option(playable_options, self.game_state, self.OPTIONS)
            print("Best choice to maximize boings:", best_choice)
            self.mark_number(best_choice)
            self.display_state()
            return True
        else:
            print("No valid options available.")
            return False

    def play_game(self):
        """Run the interactive game loop"""
        print("\nEnter dice values as three digits (e.g., '356')")
        print("Enter 'q' to quit\n")
        
        while True:
            dice_input = input("Dice values: ").strip().lower()
            if dice_input == 'q':
                break
                
            try:
                red, white1, white2 = map(int, list(dice_input))
                self.play_turn(red, white1, white2)
            except ValueError:
                print("Invalid input. Please enter three digits without spaces (e.g., '356')")