from strategy_interface import Strategy
from typing import List, Dict, Set, Tuple
from number_state import NumberState

class DefaultStrategy(Strategy):
    """Default strategy implementation focusing on maximizing boings"""
    
    def select_best_option(
        self, 
        playable_options: Set[int], 
        game_state: Dict[str, NumberState], 
        options: List[List[int]]
    ) -> int:
        """
        Select the best number to mark based on boing potential and line completion.
        
        Args:
            playable_options: Set of valid numbers that can be marked
            game_state: Current state of all numbers in the game
            options: List of all valid number combinations (lines)
            
        Returns:
            The best number to mark next
        """
        best_option = None
        max_boing_potential = -1
        max_number = 0
        fewest_uncrossed = float('inf')

        for number in playable_options:
            # Calculate metrics for this number
            boing_potential = self._check_boing_potential(number, game_state, options)
            min_uncrossed_count = self._get_min_uncrossed_line_count(number, game_state, options)

            # Update best option if this number is better
            if (min_uncrossed_count < fewest_uncrossed or
                (min_uncrossed_count == fewest_uncrossed and boing_potential > max_boing_potential) or
                (min_uncrossed_count == fewest_uncrossed and boing_potential == max_boing_potential and number > max_number)):
                
                fewest_uncrossed = min_uncrossed_count
                max_boing_potential = boing_potential
                max_number = number
                best_option = number

        # If no best option found, return the highest available number
        return best_option or max(playable_options)
    
    def _check_boing_potential(
        self, 
        number: int, 
        game_state: Dict[str, NumberState], 
        options: List[List[int]]
    ) -> int:
        """
        Calculate the potential for creating boings by marking this number.
        
        Args:
            number: The number being evaluated
            game_state: Current state of all numbers
            options: List of all valid number combinations
            
        Returns:
            A score indicating how likely this number is to create boings
        """
        boing_potential = 0
        str_number = str(number)
        
        for option in options:
            if number in option:
                marked_count = sum(1 for num in option 
                                 if game_state[str(num)] != NumberState.not_crossed)
                                 
                # High potential if this would leave only one number uncrossed
                if marked_count == len(option) - 2:
                    boing_potential += 2
                # Some potential if line already has some marked numbers
                elif marked_count > 0:
                    boing_potential += 1
                    
        return boing_potential

    def _get_min_uncrossed_line_count(
        self, 
        number: int, 
        game_state: Dict[str, NumberState], 
        options: List[List[int]]
    ) -> int:
        """
        Find the minimum number of uncrossed numbers in any line containing this number.
        
        Args:
            number: The number being evaluated
            game_state: Current state of all numbers
            options: List of all valid number combinations
            
        Returns:
            The minimum count of uncrossed numbers in any line containing this number
        """
        uncrossed_counts = []
        
        for option in options:
            if number in option:
                uncrossed_count = self._count_uncrossed_numbers(option, game_state)
                uncrossed_counts.append(uncrossed_count)
                
        return min(uncrossed_counts) if uncrossed_counts else float('inf')

    def _count_uncrossed_numbers(
        self, 
        option: List[int], 
        game_state: Dict[str, NumberState]
    ) -> int:
        """
        Count how many numbers in a line are not yet crossed.
        
        Args:
            option: List of numbers in the line
            game_state: Current state of all numbers
            
        Returns:
            Count of uncrossed numbers in the line
        """
        return sum(1 for num in option 
                  if game_state[str(num)] == NumberState.not_crossed)

    def explain_selection(
        self,
        playable_options: Set[int],
        game_state: Dict[str, NumberState],
        options: List[List[int]]
    ) -> Tuple[int, str]:
        """
        Select the best number and provide detailed explanation of the calculation.
        
        Args:
            playable_options: Set of valid numbers that can be marked
            game_state: Current state of all numbers in the game
            options: List of all valid number combinations (lines)
            
        Returns:
            Tuple of (selected_number, explanation_string)
        """
        # Track metrics for all options
        option_metrics = {}
        
        for number in playable_options:
            boing_potential = self._check_boing_potential(number, game_state, options)
            min_uncrossed_count = self._get_min_uncrossed_line_count(number, game_state, options)
            option_metrics[number] = {
                'boing_potential': boing_potential,
                'min_uncrossed_count': min_uncrossed_count
            }
        
        # Now find the best option with same logic as select_best_option
        best_option = None
        max_boing_potential = -1
        max_number = 0
        fewest_uncrossed = float('inf')

        for number, metrics in option_metrics.items():
            boing_potential = metrics['boing_potential']
            min_uncrossed_count = metrics['min_uncrossed_count']

            # Update best option if this number is better
            if (min_uncrossed_count < fewest_uncrossed or
                (min_uncrossed_count == fewest_uncrossed and boing_potential > max_boing_potential) or
                (min_uncrossed_count == fewest_uncrossed and boing_potential == max_boing_potential and number > max_number)):
                
                fewest_uncrossed = min_uncrossed_count
                max_boing_potential = boing_potential
                max_number = number
                best_option = number

        # If no best option found, use the highest available number
        if best_option is None:
            best_option = max(playable_options)
            explanation = f"No optimal choice found. Selected highest number: {best_option}"
            return best_option, explanation
            
        # Prepare detailed explanation
        explanation = f"Selected {best_option} because:\n"
        explanation += f"- Min uncrossed numbers in any line: {option_metrics[best_option]['min_uncrossed_count']}\n"
        explanation += f"- Boing potential score: {option_metrics[best_option]['boing_potential']}\n"
        
        # Add comparison to other options
        filtered_options = playable_options - {best_option}
        if filtered_options:
            explanation += "Comparison with other options:\n"
            for number in sorted(filtered_options):
                explanation += f"- Number {number}: min_uncrossed={option_metrics[number]['min_uncrossed_count']}, boing_potential={option_metrics[number]['boing_potential']}\n"
                
        return best_option, explanation