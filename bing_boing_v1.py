options = [
    # rows
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
    [25, 26, 31],
    [21, 22, 23, 24],
    [35, 36, 41, 42],
    [32, 33, 34],
    [43, 44, 45, 46],
    [51, 52, 53, 54],
    [55, 56, 61, 62],
    [63, 64, 65, 66],
    
    # columns
    [1, 5, 9, 16],
    [2, 6, 10],
    [3, 7, 11],
    [4, 8, 12, 21],
    
    [13, 25, 35],
    [14, 26, 36],
    [15, 31, 41],
    [42, 51, 55, 63],
    
    [22, 32, 44],
    [23, 33, 45],
    [24, 34, 46],
    
    [52, 56, 64],
    [53, 61, 65],
    [43, 54, 62, 66]
]

# this array stores the bing (X) or boing (O) for each option at the same index
resutls = []

def get_all_distinct_numbers(options):
    # Using a set to store distinct numbers from all sub-lists in options
    distinct_numbers = set()
    for sublist in options:
        distinct_numbers.update(sublist)
    return sorted(distinct_numbers)

def generate_options(red, white1, white2):
    # Generate basic arithmetic operations
    options = set()  # Use a set to avoid duplicates

    # For each white die, calculate with the red die
    for white in [white1, white2]:
        options.add(red + white)         # Addition
        options.add(red - white)         # Subtraction
        options.add(white - red)         # Subtraction in reverse
        options.add(red * white)         # Multiplication
        if white != 0:
            options.add(red // white)    # Division (integer) if white isn't zero
        if red != 0:
            options.add(white // red)    # Division in reverse if red isn't zero
        options.add(red ** white)        # Power (red^white)
        options.add(white ** red)        # Power (white^red)

        # Concatenations in both orders
        options.add(int(f"{red}{white}"))
        options.add(int(f"{white}{red}"))

    # Filter out 0 and negative values, and sort the result
    return sorted(filter(lambda x: x > 0, options))

def count_marked_in_option(option, results, options):
    """
    Counts how many numbers in a row or column are already marked as boings.
    
    Args:
        option (list): The row or column to check.
        results (list): List marking each row/column with 'O' for boings or None if unmarked.
        options (list): List of rows and columns, each containing a list of numbers.
        
    Returns:
        int: Count of marked boings in the row/column.
    """
    option_index = options.index(option)
    return sum(1 for num in option if results[option_index] == 'O')

def calculate_boing_potential(number, option, results, options):
    """
    Calculates the boing potential for a given number in a specific row or column.
    
    Args:
        number (int): The number being considered for play.
        option (list): The row or column to check.
        results (list): List marking each row/column with 'O' for boings or None if unmarked.
        options (list): List of rows and columns, each containing a list of numbers.
        
    Returns:
        int: The boing potential score (2 for a full boing, 1 for a partial boing).
    """
    if number not in option:
        return 0  # No potential if the number is not in the row/column
    
    marked_count = count_marked_in_option(option, results, options)
    
    # Full boing if this play would complete the row/column
    if marked_count == len(option) - 1:
        return 2
    
    # Partial boing if it brings the row/column closer to completion
    elif marked_count > 0:
        return 1
    
    return 0  # No boing potential if no marks and does not complete

def select_best_option(playable_options, options, results):
    """
    Selects the best number from playable_options to maximize boings across all rows/columns.
    
    Args:
        playable_options (list): List of numbers generated from the dice roll that can be played.
        options (list): List of rows and columns, each containing a list of numbers.
        results (list): List marking each row/column with 'O' for boings or None if unmarked.
        
    Returns:
        int: The best number to play to maximize boings.
    """
    best_option = None
    max_boings = 0

    # Evaluate each number in playable options
    for number in playable_options:
        total_boing_potential = 0

        # Calculate the boing potential of the number for each row/column
        for option in options:
            total_boing_potential += calculate_boing_potential(number, option, results, options)

        # Update the best option if the current number yields more boings
        if total_boing_potential > max_boings:
            max_boings = total_boing_potential
            best_option = number

    return best_option


print(get_all_distinct_numbers(options))