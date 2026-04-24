from __future__ import annotations

import math
from typing import Protocol

from .Tag import Tag


class _PixelConverter(Protocol):
    """Minimal interface Point needs from its parent — both Gradeable and
    Function expose these pixel <-> coordinate conversion methods.
    """

    def _px_to_xval(self, px: float) -> float: ...
    def _px_to_yval(self, px: float) -> float: ...
    def _xval_to_px(self, xval: float) -> float: ...
    def _yval_to_px(self, yval: float) -> float: ...


class Point(Tag):
    x: float
    y: float
    px: float
    py: float

    def __init__(
        self, parent_function: _PixelConverter, x: float, y: float, pixel: bool = True
    ) -> None:
        super().__init__()
        if pixel:
            self.px = x
            self.py = y
            self.x = parent_function._px_to_xval(x)
            self.y = parent_function._px_to_yval(y)
        else:
            self.x = x
            self.y = y
            self.px = parent_function._xval_to_px(x)
            self.py = parent_function._yval_to_px(y)

    def get_px_distance_squared(self, point: Point) -> float:
        dx = point.px - self.px
        dy = point.py - self.py
        return dx**2 + dy**2

    def get_euclidean_distance(self, point: Point) -> float:
        return math.sqrt(self.get_px_distance_squared(point))

    def get_x_distance(self, x: float) -> float:
        return abs(x - self.x)

    def get_y_distance(self, y: float) -> float:
        return abs(y - self.y)
