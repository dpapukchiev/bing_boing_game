from tabulate import tabulate
from number_state import NumberState
from typing import Dict, List

class Tile:
    def __init__(self, x: int, y: int, number: int):
        self.x = x
        self.y = y
        self.number = number

    def __repr__(self):
        return f"Tile(x={self.x}, y={self.y}, number={self.number})"

class Map:
    def __init__(self, width: int, height: int, initial_state: dict = None):
        self.width = width
        self.height = height
        self.tiles = initial_state if initial_state else {}

    def get_tile(self, x: int, y: int):
        return self.tiles.get((x, y))

    def set_tile(self, x: int, y: int, number: int):
        self.tiles[(x, y)] = Tile(x, y, number)

    def display_map(self, game_state: Dict[str, NumberState]):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                tile = self.tiles.get((x, y))
                if tile:
                    num_str = str(tile.number)
                    state = game_state.get(num_str, NumberState.not_crossed)
                    if state == NumberState.bing:
                        row.append(f"X {num_str}".rjust(4, '.'))
                    elif state == NumberState.boing:
                        row.append(f"O {num_str}".rjust(4, '.'))
                    else:
                        row.append(num_str.rjust(4, '.'))
                else:
                    row.append(".....")
            grid.append(row)
        print(tabulate(grid, tablefmt="grid"))

    def find_consecutive_coordinates(self) -> List[List[int]]:
        consecutive_groups = []

        # Find consecutive numbers in rows based on grid coordinates
        for y in range(self.height):
            row_group = []
            for x in range(self.width):
                tile = self.tiles.get((x, y))
                if tile:
                    row_group.append(tile.number)
                elif row_group:
                    if len(row_group) > 1:
                        consecutive_groups.append(row_group)
                    row_group = []
            if len(row_group) > 1:
                consecutive_groups.append(row_group)

        # Find consecutive numbers in columns based on grid coordinates
        for x in range(self.width):
            col_group = []
            for y in range(self.height):
                tile = self.tiles.get((x, y))
                if tile:
                    col_group.append(tile.number)
                elif col_group:
                    if len(col_group) > 1:
                        consecutive_groups.append(col_group)
                    col_group = []
            if len(col_group) > 1:
                consecutive_groups.append(col_group)

        return consecutive_groups

class FileMap(Map):
    def __init__(self, file_path: str, width: int = None, height: int = None):
        initial_state, file_width, file_height = self._load_from_file(file_path)
        width = width if width is not None else file_width
        height = height if height is not None else file_height
        super().__init__(width, height, initial_state)

    def _load_from_file(self, file_path: str):
        initial_state = {}
        max_width = 0
        with open(file_path, 'r') as file:
            for y, line in enumerate(file):
                row = line.strip().split(',')
                for x, cell in enumerate(row):
                    if cell.isdigit():
                        initial_state[(x, y)] = Tile(x, y, int(cell))
                max_width = max(max_width, len(row))
        return initial_state, max_width, y + 1
