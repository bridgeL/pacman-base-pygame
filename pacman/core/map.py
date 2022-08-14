lines = [
    "# # # # # # # # # # # # # # # # # # # # # # # # # # # #",
    "# - - - - - - - - - - - - # # - - - - - - - - - - - - #",
    "# - # # # # - # # # # # - # # - # # # # # - # # # # - #",
    "# @ # . . # - # . . . # - # # - # . . . # - # . . # @ #",
    "# - # # # # - # # # # # - # # - # # # # # - # # # # - #",
    "# - - - - - - - - - - - - - - - - - - - - - - - - - - #",
    "# - # # # # - # # - # # # # # # # # - # # - # # # # - #",
    "# - # # # # - # # - # # # # # # # # - # # - # # # # - #",
    "# - - - - - - # # - - - - # # - - - - # # - - - - - - #",
    "# # # # # # - # # # # # . # # . # # # # # - # # # # # #",
    "# # # # # # - # # # # # . # # . # # # # # - # # # # # #",
    ". . . . # # - # # . . . . . . . . . . # # - # # . . . .",
    "# # # # # # - # # . # # # . . # # # . # # - # # # # # #",
    "# # # # # # - # # . # . . . . . . # . # # - # # # # # #",
    ". . . . . . - . . . # . . . . . . # . . . - . . . . . .",
    "# # # # # # - # # . # . . . . . . # . # # - # # # # # #",
    "# # # # # # - # # . # # # # # # # # . # # - # # # # # #",
    ". . . . # # - # # . . . . . . . . . . # # - # # . . . .",
    "# # # # # # - # # . # # # # # # # # . # # - # # # # # #",
    "# # # # # # - # # . # # # # # # # # . # # - # # # # # #",
    "# - - - - - - - - - - - - # # - - - - - - - - - - - - #",
    "# - # # # # - # # # # # - # # - # # # # # - # # # # - #",
    "# - # # # # - # # # # # - # # - # # # # # - # # # # - #",
    "# @ - - # # - - - - - - - . . - - - - - - - # # - - @ #",
    "# # # - # # - # # - # # # # # # # # - # # - # # - # # #",
    "# # # - # # - # # - # # # # # # # # - # # - # # - # # #",
    "# - - - - - - # # - - - - # # - - - - # # - - - - - - #",
    "# - # # # # # # # # # # - # # - # # # # # # # # # # - #",
    "# - # # # # # # # # # # - # # - # # # # # # # # # # - #",
    "# - - - - - - - - - - - - - - - - - - - - - - - - - - #",
    "# # # # # # # # # # # # # # # # # # # # # # # # # # # #"
]


class Map:
    def __init__(self) -> None:
        self.map = [line.split() for line in lines]
        self.gap = 20
        self.row = len(self.map)
        self.col = len(self.map[0])

    def is_item(self, i: int, j: int, item: str):
        if i < 0 or i >= self.row or j < 0 or j >= self.col:
            print("error", "寻址错误", i, j)
            return None
        return self.map[i][j] == item

    def is_wall(self, i: int, j: int):
        return self.is_item(i, j, "#")

    def is_bean(self, i: int, j: int):
        return self.is_item(i, j, "-")

    def is_power(self, i: int, j: int):
        return self.is_item(i, j, "@")

    def clear(self, i: int, j: int):
        self.map[i][j] = "."

    def pos2coord(self, pos: tuple, be_int = True):
        if be_int:
            coord = [int(x / self.gap) for x in pos]
        else:
            coord = [x / self.gap for x in pos]
        return coord

    def coord2pos(self, coord: tuple):
        pos = [i*self.gap for i in coord]
        return pos
