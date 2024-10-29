from default_strategy import DefaultStrategy
from map import FileMap
from strategies import (
    AggressiveBoingStrategy,
    LineCompletionStrategy,
    BalancedStrategy,
    RandomStrategy,
    MaxNumberStrategy,
    ChainReactionMaximiser
)
from bing_boing_game import BingBoingGame
from typing import Dict, Type

def get_available_strategies() -> Dict[int, tuple]:
    """
    Returns a dictionary of available strategies with their performance metrics.
    The strategies are sorted by Boing efficiency in descending order.
    """
    return {
        1: (BalancedStrategy, "Balanced Strategy"),
        2: (LineCompletionStrategy, "Line Completion Strategy"),
        3: (AggressiveBoingStrategy, "Aggressive Boing Strategy"),
        4: (ChainReactionMaximiser, "Chain Reaction Maximiser"),
        5: (DefaultStrategy, "Default Strategy"),
        6: (RandomStrategy, "Random Strategy"),
        7: (MaxNumberStrategy, "Max Number Strategy"),
    }

def display_strategies() -> None:
    """Displays the numbered list of available strategies with their efficiency."""
    print("\nAvailable strategies:")
    print("-" * 50)
    for number, (_, description) in get_available_strategies().items():
        print(f"{number}. {description}")
    print("-" * 50)

def get_strategy_choice() -> Type:
    """
    Prompts the user to choose a strategy and returns the selected strategy class.
    Returns BalancedStrategy if input is invalid.
    """
    display_strategies()
    
    try:
        choice = int(input("\nSelect strategy number (1-7): "))
        strategies = get_available_strategies()
        if choice in strategies:
            selected_strategy = strategies[choice][0]
            print(f"\nUsing {strategies[choice][1]}")
            return selected_strategy
        else:
            print("\nInvalid choice. Using Balanced Strategy (best performance).")
            return BalancedStrategy
    except ValueError:
        print("\nInvalid input. Using Balanced Strategy (best performance).")
        return BalancedStrategy

def get_map_choice() -> str:
    """Prompts the user to choose a map (blue or yellow) and returns the file path."""
    print("\nAvailable maps:")
    print("-" * 50)
    print("1. Blue Map")
    print("2. Yellow Map")
    print("-" * 50)
    
    choice = input("Select map number (1 or 2): ").strip()
    if choice == "1":
        print("\nUsing Blue Map")
        return "./maps/blue.csv"
    elif choice == "2":
        print("\nUsing Yellow Map")
        return "./maps/yellow.csv"
    else:
        print("\nInvalid choice. Defaulting to Blue Map.")
        return "./maps/blue.csv"

def main():
    """Main entry point for the game"""
    print("Welcome to Bing Boing!")
    
    # Get strategy and map selections from user
    SelectedStrategy = get_strategy_choice()
    selected_map = get_map_choice()
    
    # Initialize and start the game
    game = BingBoingGame(
        strategy=SelectedStrategy(),
        save_file="game_state.json",
        map=selected_map
    )
    game.initialize_game()
    game.display_state()
    game.play_game()

if __name__ == "__main__":
    main()
