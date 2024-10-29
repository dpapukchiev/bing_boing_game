from strategy_interface import Strategy

class DefaultStrategy(Strategy):
    """Default strategy implementation focusing on maximizing boings"""
    def select_best_option(self, playable_options, game_state, options):
        best_option = None
        max_boing_potential = -1
        max_number = 0
        fewest_uncrossed = float('inf')

        for number in playable_options:
            boing_potential = self._check_boing_potential(number, game_state, options)
            min_uncrossed_count = min(
                self._count_uncrossed_numbers(option, game_state)
                for option in options if number in option
            )

            if (min_uncrossed_count < fewest_uncrossed or
                (min_uncrossed_count == fewest_uncrossed and boing_potential > max_boing_potential) or
                (min_uncrossed_count == fewest_uncrossed and boing_potential == max_boing_potential and number > max_number)):
                
                fewest_uncrossed = min_uncrossed_count
                max_boing_potential = boing_potential
                max_number = number
                best_option = number

        return best_option or max(playable_options)
    
    def _check_boing_potential(self, number, game_state, options):
        boing_potential = 0
        
        for option in options:
            if number in option:
                marked_count = sum(1 for num in option if game_state[str(num)] != 'not_crossed')
                if marked_count == len(option) - 1:
                    boing_potential += 2
                elif marked_count > 0:
                    boing_potential += 1
        return boing_potential

    def _count_uncrossed_numbers(self, option, game_state):
        return sum(1 for num in option if game_state[str(num)] == 'not_crossed')