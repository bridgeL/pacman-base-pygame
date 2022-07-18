import json
from pathlib import Path


class Map:
    def __init__(self) -> None:
        with Path("res", "map.json").open("r", encoding="utf8") as f:
            lines: list[str] = json.load(f)

        self._map = [line.split() for line in lines]
        self.gap = 20

    def is_item(self, i: int, j: int, item: str):
        try:
            return self._map[i][j] == item
        except:
            raise Exception("地图寻址错误", i, j)

    def is_wall(self, i: int, j: int):
        return self.is_item(i, j, "#")

    def is_bean(self, i: int, j: int):
        return self.is_item(i, j, "-")

    def is_power(self, i: int, j: int):
        return self.is_item(i, j, "@")

    def clear(self, i: int, j: int):
        self._map[i][j] = "."
