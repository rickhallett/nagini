from __future__ import annotations
from typing import Callable, Any
from dataclasses import dataclass

F = Callable[[int], int]
AndF = Callable[[F], int]

@dataclass
class Composable:
    function: F

    def __call__(self, value: int) -> int:
        return self.function(value)

    def and_then(self, other: AndF) -> Composable:
        function = lambda value: other(self.function)(value)
        function.__name__ = f"{self} and then {other.__name__}"
        return Composable(function)

    def __rshift__(self, other: AndF) -> Composable:
        return self.and_then(other)

    def __str__(self) -> str:
        return self.function.__name__

def double(parser):
    return lambda value: parser(value)*2
def square(parser):
    return lambda value: parser(value)**2
def constant(value):
    return value

simple = square(double(constant))
composed = Composable(constant) >> double >> square

print("simple:", simple(2))
print("composed:", composed(2))
print("composed arrangement:", composed)
