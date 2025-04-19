from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple
from number_state import NumberState

class Strategy(ABC):
    """Abstract base class for game playing strategies"""
    @abstractmethod
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], options: List[List[int]]) -> int:
        """Select the best option from available moves"""
        pass
        
    def explain_selection(self, playable_options: Set[int], game_state: Dict[str, NumberState], options: List[List[int]]) -> Tuple[int, str]:
        """
        Select the best option and return an explanation of the calculation.
        By default, uses select_best_option and returns a generic explanation.
        
        Returns:
            Tuple of (selected_number, explanation_string)
        """
        best_choice = self.select_best_option(playable_options, game_state, options)
        explanation = "No detailed explanation available for this strategy."
        return best_choice, explanation