from strategy_interface import Strategy
from typing import List, Dict, Set
from number_state import NumberState
import random

class AggressiveBoingStrategy(Strategy):
    """Strategy that aggressively pursues boings by prioritizing moves that create immediate boings"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        best_option = None
        max_immediate_boings = -1

        for number in playable_options:
            immediate_boings = 0
            for option in options:
                if number in option:
                    uncrossed = sum(1 for num in option 
                                  if game_state[str(num)] == NumberState.not_crossed)
                    if uncrossed == 2:  # This move will create a boing
                        immediate_boings += 1
            
            if immediate_boings > max_immediate_boings:
                max_immediate_boings = immediate_boings
                best_option = number

        return best_option or max(playable_options)

class LineCompletionStrategy(Strategy):
    """Strategy that focuses on completing lines sequentially"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        best_option = None
        min_remaining = float('inf')
        
        for number in playable_options:
            for option in options:
                if number in option:
                    remaining = sum(1 for num in option 
                                  if game_state[str(num)] == NumberState.not_crossed)
                    if remaining < min_remaining:
                        min_remaining = remaining
                        best_option = number
        
        return best_option or min(playable_options)

class BalancedStrategy(Strategy):
    """Strategy that balances between creating boings and completing lines"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        best_option = None
        best_score = float('-inf')
        
        for number in playable_options:
            boing_potential = 0
            completion_potential = 0
            
            for option in options:
                if number in option:
                    uncrossed = sum(1 for num in option 
                                  if game_state[str(num)] == NumberState.not_crossed)
                    if uncrossed == 2:  # Will create boing
                        boing_potential += 3
                    elif uncrossed == 3:  # Close to creating boing
                        completion_potential += 2
                    else:
                        completion_potential += 1
            
            score = boing_potential * 0.6 + completion_potential * 0.4
            if score > best_score:
                best_score = score
                best_option = number
        
        return best_option or max(playable_options)

class RandomStrategy(Strategy):
    """Strategy that makes random choices among available options"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        return random.choice(list(playable_options))

class MaxNumberStrategy(Strategy):
    """Strategy that always chooses the highest available number"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        return max(playable_options)