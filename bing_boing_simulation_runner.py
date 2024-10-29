from dataclasses import dataclass
from typing import List
import statistics
from bing_boing_game import BingBoingGame
from strategy_interface import Strategy
from game_stats import GameStats
from default_strategy import DefaultStrategy
from tabulate import tabulate
from strategies import AggressiveBoingStrategy, LineCompletionStrategy, BalancedStrategy, RandomStrategy, MaxNumberStrategy

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

def compare_strategies(num_games: int = 100) -> None:
    """Run simulations for all strategies and compare results"""
    strategies = [
        DefaultStrategy(),
        AggressiveBoingStrategy(),
        LineCompletionStrategy(),
        BalancedStrategy(),
        RandomStrategy(),
        MaxNumberStrategy()
    ]
    
    results = []
    for strategy in strategies:
        print(f"\nRunning simulation for {strategy.__class__.__name__}...")
        result = run_simulation(strategy, num_games)
        results.append(result)
    
    # Create comparison table
    headers = ["Strategy", "Avg Turns", "Boing Efficiency", "Marks/Turn", "Average Boing Count"]
    table_data = []
    
    for result in results:
        table_data.append([
            result.strategy_name,
            f"{result.avg_turns:.2f}",
            f"{result.avg_boing_efficiency:.2f}%",
            f"{result.avg_marks_per_turn:.2f}",
            f"{result.avg_boing_count:.2f}"
        ])
    
    # Sort by average boing count
    table_data.sort(key=lambda x: float(x[4]), reverse=True)
    
    print("\nStrategy Comparison:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # Print detailed results for best strategy
    best_strategy = max(results, key=lambda x: x.avg_boing_efficiency)
    print(f"\nBest Strategy: {best_strategy.strategy_name}")
    print(f"Best game performance:")
    print(f"  Turns: {best_strategy.best_game.turns_taken}")
    print(f"  Boing efficiency: {best_strategy.best_game.boing_efficiency:.2f}%")
    print(f"  Marks per turn: {best_strategy.best_game.marks_per_turn:.2f}")
    print(f"  Boing count: {best_strategy.best_game.boing_count}")

if __name__ == "__main__":
    compare_strategies(num_games=100)