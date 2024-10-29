from strategy_interface import Strategy
from typing import List, Dict, Set
from number_state import NumberState
import random

class ChainReactionMaximiser(Strategy):
    """Strategy that simulates moves to find the one creating the longest chain reaction of boings"""
    
    def select_best_option(self, playable_options: Set[int], game_state: Dict[str, NumberState], 
                          options: List[List[int]]) -> int:
        best_option = None
        max_chain_length = -1
        
        for number in playable_options:
            chain_length = self._simulate_chain_reaction(number, game_state.copy(), options)
            
            if chain_length > max_chain_length:
                max_chain_length = chain_length
                best_option = number
            elif chain_length == max_chain_length and best_option is not None:
                # If equal chain lengths, prefer the number that appears in more lines
                current_lines = sum(1 for option in options if number in option)
                best_lines = sum(1 for option in options if best_option in option)
                if current_lines > best_lines:
                    best_option = number
        
        return best_option or max(playable_options)
    
    def _simulate_chain_reaction(self, number: int, game_state: Dict[str, NumberState], 
                               options: List[List[int]]) -> int:
        """
        Simulate marking a number and count resulting chain reactions.
        
        Args:
            number: The number to simulate marking
            game_state: Copy of current game state
            options: List of all valid number combinations
            
        Returns:
            Total number of boings that would be created in the chain reaction
        """
        boings_created = 0
        affected_lines = set()
        
        # Mark the initial number as bing
        game_state[str(number)] = NumberState.bing
        
        # Keep track of which lines have already triggered boings
        processed_lines = set()
        
        # Continue until no new boings are created
        while True:
            new_boings_this_round = 0
            
            # Find all lines that need to be checked
            lines_to_check = set()
            for i, option in enumerate(options):
                if i not in processed_lines:  # Only check unprocessed lines
                    marked_count = sum(1 for num in option 
                                     if game_state[str(num)] != NumberState.not_crossed)
                    unmarked_count = len(option) - marked_count
                    
                    if unmarked_count == 1:  # This line will create a boing
                        lines_to_check.add(i)
            
            if not lines_to_check:
                break
                
            # Process all found lines
            for line_index in lines_to_check:
                option = options[line_index]
                # Find the unmarked number in this line
                for num in option:
                    if game_state[str(num)] == NumberState.not_crossed:
                        game_state[str(num)] = NumberState.boing
                        new_boings_this_round += 1
                        break
                processed_lines.add(line_index)
            
            boings_created += new_boings_this_round
            if new_boings_this_round == 0:
                break
        
        return boings_created
    
    def _get_affected_lines(self, number: int, options: List[List[int]]) -> Set[int]:
        """Get indices of all lines containing the given number"""
        return {i for i, option in enumerate(options) if number in option}

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