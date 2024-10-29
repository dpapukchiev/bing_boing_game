from dataclasses import dataclass
from typing import Dict

@dataclass
class GameStats:
    """Statistics from a completed game"""
    turns_taken: int
    bing_count: int
    boing_count: int
    total_marked: int
    boing_efficiency: float
    marks_per_turn: float
    won: bool
    final_state: Dict[str, str]