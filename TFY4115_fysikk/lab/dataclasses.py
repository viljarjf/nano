"""

Dataclasses

"""

from dataclasses import dataclass

@dataclass
class Ball:
    m: float
    c: float
    r: float

    @property
    def I(self):
        return self.c*self.m*self.r**2
    
    def __str__(self):
        return f"Ball:\n\tm: {self.m}\n\tc: {self.c}\n\tr: {self.r}"

@dataclass
class Force:
    x: float
    y: float

    @property
    def len(self) -> float:
        return (self.x**2 + self.y**2)**0.5

    def __truediv__(self, other):
        if isinstance(other, float):
            return Force(self.x / other, self.y / other)
        raise NotImplementedError
    
    def __itruediv__(self, other):
        if isinstance(other, float):
            self.x /= other
            self.y /= other
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, float):
            return Force(self.x * other, self.y * other)
        raise NotImplementedError
    
    def __imul__(self, other):
        if isinstance(other, float):
            self.x *= other
            self.y *= other
        raise NotImplementedError
    
    def __add__(self, other):
        if isinstance(other, Force):
            return Force(self.x + other.x, self.y + other.y)
        elif isinstance(other, float):
            return Force(self.x + other, self.y + other)
        raise NotImplementedError

class Point(Force):
    pass
