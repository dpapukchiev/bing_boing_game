from abc import ABC, abstractmethod

class Strategy(ABC):
    """Abstract base class for game playing strategies"""
    @abstractmethod
    def select_best_option(self, playable_options, game_state, options):
        """Select the best option from available moves"""
        pass