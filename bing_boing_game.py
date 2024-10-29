import json
import os
import random
from default_strategy import DefaultStrategy
from game_stats import GameStats

class BingBoingGame:
    """Main game class implementing the Bing Boing game logic"""
    
    ROWS_AND_COLUMNS = [
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

    def __init__(self, strategy=None, save_file="game_state.json", simulation_mode=False):
        self.save_file = save_file
        self.strategy = strategy or DefaultStrategy()
        self.simulation_mode = simulation_mode
        self.game_state = None
        self.turns_taken = 0
        self.game_won = False

    def initialize_game(self):
        """Initialize the game by either loading a saved state or starting fresh"""
        if not self.simulation_mode and os.path.exists(self.save_file):
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
        self.turns_taken = 0
        self.game_won = False
        self.save_game_state()

    def get_all_numbers(self):
        """Returns a set of all numbers in the game grid"""
        return set(num for option in self.ROWS_AND_COLUMNS for num in option)

    def save_game_state(self):
        """Save the current game state to a file"""
        save_data = {
            'game_state': self.game_state,
            'turns_taken': self.turns_taken,
            'game_won': self.game_won
        }
        with open(self.save_file, "w") as file:
            json.dump(save_data, file)

    def load_game_state(self):
        """Load game state from file"""
        with open(self.save_file, "r") as file:
            save_data = json.load(file)
            self.game_state = save_data['game_state']
            self.turns_taken = save_data.get('turns_taken', 0)  # Default to 0 for backward compatibility
            self.game_won = save_data.get('game_won', False)  # Default to False for backward compatibility

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
            for option in self.ROWS_AND_COLUMNS:
                option_status = [self.game_state[str(num)] for num in option]
                not_crossed_count = sum(1 for state in option_status if state == 'not_crossed')
                
                if not_crossed_count == 1:
                    for num in option:
                        if self.game_state[str(num)] == 'not_crossed':
                            self.mark_number(num, 'boing')
                            updated = True
                            break

    def check_win_condition(self):
        """Check if the game is won by checking if no more moves are possible"""
        # Get all remaining uncrossed numbers
        remaining_numbers = {num for num in self.get_all_numbers() 
                           if self.game_state[str(num)] == 'not_crossed'}
        
        if not remaining_numbers:
            self.game_won = True
            return True
            
        # Check if any remaining numbers can form valid pairs
        # This is a simple check - you might want to make it more sophisticated
        for option in self.ROWS_AND_COLUMNS:
            uncrossed_in_option = sum(1 for num in option 
                                    if self.game_state[str(num)] == 'not_crossed')
            if uncrossed_in_option > 1:
                return False
                
        self.game_won = True
        return True

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
    
    def simulate_game(self) -> GameStats:
        """Run a complete game simulation with random dice rolls"""
        self.new_game()
        
        while not self.game_won:
            red, white1, white2 = self.roll_dice()
            if not self.simulation_mode:
                print(f"\nRolled: Red={red}, White1={white1}, White2={white2}")
            
            playable_options = self.generate_options(red, white1, white2)
            
            if playable_options:
                best_choice = self.strategy.select_best_option(playable_options, self.game_state, self.ROWS_AND_COLUMNS)
                if not self.simulation_mode:
                    print(f"Choosing: {best_choice}")
                self.mark_number(best_choice)
                self.turns_taken += 1
            
            self.check_win_condition()
            
            if not self.simulation_mode:
                self.display_state()
        
        return self.collect_stats()
    
    def collect_stats(self) -> GameStats:
        """Collect and return game statistics"""
        bing_count = sum(1 for state in self.game_state.values() if state == 'bing')
        boing_count = sum(1 for state in self.game_state.values() if state == 'boing')
        total_marked = bing_count + boing_count
        
        return GameStats(
            turns_taken=self.turns_taken,
            bing_count=bing_count,
            boing_count=boing_count,
            total_marked=total_marked,
            boing_efficiency=boing_count / total_marked * 100 if total_marked > 0 else 0,
            marks_per_turn=total_marked / self.turns_taken if self.turns_taken > 0 else 0,
            won=self.game_won,
            final_state=self.game_state.copy()
        )

    def display_state(self):
        """Display the current game state"""
        print("\nCurrent game state:")
        
        bing_count = sum(1 for state in self.game_state.values() if state == 'bing')
        boing_count = sum(1 for state in self.game_state.values() if state == 'boing')
        remaining_count = sum(1 for state in self.game_state.values() if state == 'not_crossed')
        
        for option in self.ROWS_AND_COLUMNS:
            display_option = []
            for num in option:
                state = self.game_state[str(num)]
                display_option.append(f"{num}[{'O' if state == 'boing' else 'X' if state == 'bing' else '...'}]")
            print(" | ".join(display_option))

        print(f"\nTurns taken: {self.turns_taken}")
        print(f"Total bings (X): {bing_count}")
        print(f"Total boings (O): {boing_count}")
        print(f"Remaining numbers: {remaining_count}\n")

    def roll_dice(self):
        """Simulate rolling the dice"""
        red = random.randint(1, 6)
        white1 = random.randint(1, 6)
        white2 = random.randint(1, 6)
        print(f"\nRolled: Red={red}, White1={white1}, White2={white2}")
        return red, white1, white2

    def play_turn(self, red, white1, white2):
        """Play a single turn with the given dice values"""
        if self.game_won:
            print("Game is already won! Start a new game to play again.")
            return False

        playable_options = self.generate_options(red, white1, white2)
        print("Playable options:", playable_options)

        if playable_options:
            best_choice = self.strategy.select_best_option(playable_options, self.game_state, self.ROWS_AND_COLUMNS)
            print("Best choice to maximize boings:", best_choice)
            self.mark_number(best_choice)
            self.turns_taken += 1
            self.display_state()
            
            if self.check_win_condition():
                print(f"\n🎉 Congratulations! You've won the game in {self.turns_taken} turns! 🎉")
                self.display_final_stats()
            return True
        else:
            print("No valid options available.")
            if self.check_win_condition():
                print(f"\n🎉 Congratulations! You've won the game in {self.turns_taken} turns! 🎉")
                self.display_final_stats()
            return False

    def display_final_stats(self):
        """Display final game statistics"""
        bing_count = sum(1 for state in self.game_state.values() if state == 'bing')
        boing_count = sum(1 for state in self.game_state.values() if state == 'boing')
        total_marked = bing_count + boing_count
        
        print("\nFinal Game Statistics:")
        print("----------------------")
        print(f"Total turns taken: {self.turns_taken}")
        print(f"Numbers marked as bing (X): {bing_count}")
        print(f"Numbers marked as boing (O): {boing_count}")
        print(f"Total numbers marked: {total_marked}")
        print(f"Boing efficiency ratio: {(boing_count / total_marked * 100):.1f}%")
        print(f"Average marks per turn: {(total_marked / self.turns_taken):.1f}")

    def play_game(self):
        """Run the interactive game loop with simulation mode support"""
        if self.simulation_mode:
            return self.simulate_game()
            
        print("\nEnter dice values as three digits (e.g., '356')")
        print("Press 'a' for auto-roll")
        print("Enter 'q' to quit\n")
        
        while True:
            dice_input = input("Dice values or command: ").strip().lower()
            if dice_input == 'q':
                break
            elif dice_input == 'a':
                red, white1, white2 = self.roll_dice()
                self.play_turn(red, white1, white2)
            else:
                try:
                    red, white1, white2 = map(int, list(dice_input))
                    self.play_turn(red, white1, white2)
                except ValueError:
                    print("Invalid input. Please enter three digits without spaces (e.g., '356') or 'a' for auto-roll")
        
        return self.collect_stats()     