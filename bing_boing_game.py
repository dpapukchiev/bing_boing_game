import json
import os
import random
from typing import Dict, List, Set, Tuple
from default_strategy import DefaultStrategy
from number_state import NumberState
from game_stats import GameStats

class BingBoingGame:
    """Main game class implementing the Bing Boing game logic"""
    
    OPTIONS: List[List[int]] = [
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

    def __init__(self, strategy=None, save_file: str = "game_state.json", simulation_mode: bool = False):
        self.save_file = save_file
        self.strategy = strategy or DefaultStrategy()
        self.simulation_mode = simulation_mode
        self.game_state: Dict[str, NumberState] = {}
        self.turns_taken: int = 0
        self.game_won: bool = False

    def initialize_game(self) -> None:
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

    def new_game(self) -> None:
        """Start a new game with fresh state"""
        self.game_state = {str(num): NumberState.not_crossed for num in self.get_all_numbers()}
        self.turns_taken = 0
        self.game_won = False
        self.save_game_state()

    def get_all_numbers(self) -> Set[int]:
        """Returns a set of all numbers in the game grid"""
        return set(num for option in self.OPTIONS for num in option)

    def save_game_state(self) -> None:
        """Save the current game state to a file"""
        save_data = {
            'game_state': {k: v.value for k, v in self.game_state.items()},
            'turns_taken': self.turns_taken,
            'game_won': self.game_won
        }
        with open(self.save_file, "w") as file:
            json.dump(save_data, file)

    def load_game_state(self) -> None:
        """Load game state from file"""
        with open(self.save_file, "r") as file:
            save_data = json.load(file)
            self.game_state = {k: NumberState(v) for k, v in save_data['game_state'].items()}
            self.turns_taken = save_data.get('turns_taken', 0)
            self.game_won = save_data.get('game_won', False)

    def mark_number(self, number: int, mark_type: NumberState = NumberState.bing) -> None:
        """Mark a number and handle chain reactions"""
        str_number = str(number)
        if self.game_state[str_number] == NumberState.not_crossed:
            self.game_state[str_number] = mark_type
            if not self.simulation_mode:
                print(f"Marked {number} as '{mark_type}'")
            if mark_type == NumberState.bing:
                self.check_for_boings()
            self.save_game_state()

    def check_for_boings(self) -> None:
        """Check for and handle chain reactions of boings"""
        updated = True
        while updated:
            updated = False
            for option in self.OPTIONS:
                option_states = [self.game_state[str(num)] for num in option]
                not_crossed_count = sum(1 for state in option_states 
                                      if state == NumberState.not_crossed)
                
                if not_crossed_count == 1:
                    for num in option:
                        if self.game_state[str(num)] == NumberState.not_crossed:
                            self.mark_number(num, NumberState.boing)
                            updated = True
                            break

    def check_win_condition(self) -> bool:
        """Check if the game is won by checking if no more moves are possible"""
        remaining_numbers = {num for num in self.get_all_numbers() 
                           if self.game_state[str(num)] == NumberState.not_crossed}
        
        if not remaining_numbers:
            self.game_won = True
            return True
            
        # Check if any remaining numbers can form valid pairs
        for option in self.OPTIONS:
            uncrossed_in_option = sum(1 for num in option 
                                    if self.game_state[str(num)] == NumberState.not_crossed)
            if uncrossed_in_option > 1:
                return False
                
        self.game_won = True
        return True

    def generate_options(self, red: int, white1: int, white2: int) -> List[int]:
        """Generate all possible moves from dice values"""
        options = set()
        playable_numbers = {num for num in self.get_all_numbers() 
                           if self.game_state[str(num)] == NumberState.not_crossed}

        for white in [white1, white2]:
            options.update([
                red + white,
                red - white,
                white - red,
                red * white,
            ])
            
            if white != 0:
                options.add(red // white)
            if red != 0:
                options.add(white // red)
                
            options.update([
                red ** white,
                white ** red,
                int(f"{red}{white}"),
                int(f"{white}{red}")
            ])

        return sorted(num for num in options if num > 0 and num in playable_numbers)

    def display_state(self) -> None:
        """Display the current game state"""
        if self.simulation_mode:
            return
            
        print("\nCurrent game state:")
        
        bing_count = sum(1 for state in self.game_state.values() 
                        if state == NumberState.bing)
        boing_count = sum(1 for state in self.game_state.values() 
                         if state == NumberState.boing)
        remaining_count = sum(1 for state in self.game_state.values() 
                            if state == NumberState.not_crossed)
        
        for option in self.OPTIONS:
            display_option = []
            for num in option:
                state = self.game_state[str(num)]
                symbol = 'O' if state == NumberState.boing else 'X' if state == NumberState.bing else '...'
                display_option.append(f"{num}[{symbol}]")
            print(" | ".join(display_option))

        print(f"\nTurns taken: {self.turns_taken}")
        print(f"Total bings (X): {bing_count}")
        print(f"Total boings (O): {boing_count}")
        print(f"Remaining numbers: {remaining_count}\n")

    def roll_dice(self) -> Tuple[int, int, int]:
        """Simulate rolling the dice"""
        red = random.randint(1, 6)
        white1 = random.randint(1, 6)
        white2 = random.randint(1, 6)
        if not self.simulation_mode:
            print(f"\nRolled: Red={red}, White1={white1}, White2={white2}")
        return red, white1, white2

    def play_turn(self, red: int, white1: int, white2: int) -> bool:
        """Play a single turn with the given dice values"""
        if self.game_won:
            if not self.simulation_mode:
                print("Game is already won! Start a new game to play again.")
            return False

        playable_options = self.generate_options(red, white1, white2)
        if not self.simulation_mode:
            print("Playable options:", playable_options)

        if playable_options:
            best_choice = self.strategy.select_best_option(set(playable_options), self.game_state, self.OPTIONS)
            if not self.simulation_mode:
                print("Best choice to maximize boings:", best_choice)
            self.mark_number(best_choice)
            self.turns_taken += 1
            self.display_state()
            
            if self.check_win_condition():
                if not self.simulation_mode:
                    print(f"\n🎉 Congratulations! You've won the game in {self.turns_taken} turns! 🎉")
                    self.display_final_stats()
            return True
        else:
            if not self.simulation_mode:
                print("No valid options available.")
            if self.check_win_condition():
                if not self.simulation_mode:
                    print(f"\n🎉 Congratulations! You've won the game in {self.turns_taken} turns! 🎉")
                    self.display_final_stats()
            return False

    def collect_stats(self) -> GameStats:
        """Collect and return game statistics"""
        bing_count = sum(1 for state in self.game_state.values() 
                        if state == NumberState.bing)
        boing_count = sum(1 for state in self.game_state.values() 
                         if state == NumberState.boing)
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

    def simulate_game(self) -> GameStats:
        """Run a complete game simulation with random dice rolls"""
        self.new_game()
        
        while not self.game_won:
            red, white1, white2 = self.roll_dice()
            self.play_turn(red, white1, white2)
        
        return self.collect_stats()

    def play_game(self) -> GameStats:
        """Run the interactive game loop or simulation"""
        if self.simulation_mode:
            return self.simulate_game()
            
        print("\nEnter dice values as three digits (e.g., '356')")
        print("Press 'a' for auto-roll")
        print("Enter 'q' to quit\n")
        
        while not self.game_won:
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

    def display_final_stats(self) -> None:
        """Display final game statistics"""
        if self.simulation_mode:
            return
            
        stats = self.collect_stats()
        print("\nFinal Game Statistics:")
        print("----------------------")
        print(f"Total turns taken: {stats.turns_taken}")
        print(f"Numbers marked as bing (X): {stats.bing_count}")
        print(f"Numbers marked as boing (O): {stats.boing_count}")
        print(f"Total numbers marked: {stats.total_marked}")
        print(f"Boing efficiency ratio: {stats.boing_efficiency:.1f}%")
        print(f"Average marks per turn: {stats.marks_per_turn:.1f}")