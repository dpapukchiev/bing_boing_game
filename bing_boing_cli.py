from default_strategy import DefaultStrategy
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

def main():
    """Main entry point for the game"""
    print("Welcome to Bing Boing!")
    
    # Get strategy selection from user
    SelectedStrategy = get_strategy_choice()
    
    # Initialize and start the game
    game = BingBoingGame(
        strategy=SelectedStrategy(),
        save_file="game_state.json"
    )
    game.initialize_game()
    game.display_state()
    game.play_game()

if __name__ == "__main__":
    main()