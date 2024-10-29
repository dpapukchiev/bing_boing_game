from dataclasses import dataclass
from typing import List
import statistics
from bing_boing_game import BingBoingGame
from strategy_interface import Strategy
from game_stats import GameStats
from number_state import NumberState

@dataclass
class SimulationResults:
    """Results from multiple game simulations"""
    strategy_name: str
    games_played: int
    avg_turns: float
    avg_boing_efficiency: float
    avg_boing_count: float
    avg_marks_per_turn: float
    win_rate: float
    best_game: GameStats
    worst_game: GameStats
    all_games: List[GameStats]

def run_simulation(strategy: Strategy, num_games: int = 100) -> SimulationResults:
    """Run multiple games with a given strategy and return aggregated results"""
    games: List[GameStats] = []
    
    for _ in range(num_games):
        game = BingBoingGame(strategy=strategy, simulation_mode=True)
        stats = game.simulate_game()
        games.append(stats)
    
    # Sort games by efficiency for finding best/worst games
    sorted_games = sorted(games, key=lambda x: (
        x.boing_efficiency,
        x.marks_per_turn,
        -x.turns_taken
    ), reverse=True)
    
    return SimulationResults(
        strategy_name=strategy.__class__.__name__,
        games_played=num_games,
        avg_turns=statistics.mean(game.turns_taken for game in games),
        avg_boing_efficiency=statistics.mean(game.boing_efficiency for game in games),
        avg_boing_count=statistics.mean(game.boing_count for game in games),
        avg_marks_per_turn=statistics.mean(game.marks_per_turn for game in games),
        win_rate=sum(1 for game in games if game.won) / num_games * 100,
        best_game=sorted_games[0],
        worst_game=sorted_games[-1],
        all_games=games
    )

def print_simulation_results(results: SimulationResults):
    """Print formatted simulation results"""
    print(f"\nSimulation Results for {results.strategy_name}")
    print("=" * 50)
    print(f"Games played: {results.games_played}")
    print(f"Average turns per game: {results.avg_turns:.2f}")
    print(f"Average boing efficiency: {results.avg_boing_efficiency:.2f}%")
    print(f"Average marks per turn: {results.avg_marks_per_turn:.2f}")
    print(f"Win rate: {results.win_rate:.2f}%")
    
    print("\nBest Game:")
    print(f"  Turns: {results.best_game.turns_taken}")
    print(f"  Boing efficiency: {results.best_game.boing_efficiency:.2f}%")
    print(f"  Marks per turn: {results.best_game.marks_per_turn:.2f}")
    print(f"  Boing count: {results.best_game.boing_count}")
    
    print("\nWorst Game:")
    print(f"  Turns: {results.worst_game.turns_taken}")
    print(f"  Boing efficiency: {results.worst_game.boing_efficiency:.2f}%")
    print(f"  Marks per turn: {results.worst_game.marks_per_turn:.2f}")
    print(f"  Boing count: {results.worst_game.boing_count}")

if __name__ == "__main__":
    # Example usage
    from default_strategy import DefaultStrategy
    
    strategy = DefaultStrategy()
    results = run_simulation(strategy, num_games=100)
    print_simulation_results(results)