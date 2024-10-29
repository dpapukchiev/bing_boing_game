from default_strategy import DefaultStrategy
from bing_boing_game import BingBoingGame

def main():
    """Main entry point for the game"""
    print("Welcome to Bing Boing!")
    game = BingBoingGame(
        strategy=DefaultStrategy(),
        save_file="game_state.json",
        
    )
    game.initialize_game()
    game.display_state()
    game.play_game()

if __name__ == "__main__":
    main()