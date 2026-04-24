from __future__ import annotations


class Axis:
    domain: list[float]
    pixels: int

    def __init__(self, domain: list[float], pixels: int) -> None:
        # TODO: support non-linear axis types
        self.domain = domain
        self.pixels = pixels

    def pixel_to_coord(self, value: float) -> float:
        return self.domain[0] + (value / self.pixels) * (self.domain[1] - self.domain[0])

    def coord_to_pixel(self, value: float) -> float:
        return self.pixels * (value - self.domain[0]) / (self.domain[1] - self.domain[0])
