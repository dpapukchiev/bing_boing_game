from enum import Enum

class NumberState(Enum):
    not_crossed = 0
    bing = 1
    boing = 2
    def __str__(self):
        return self.name