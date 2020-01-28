from abc import ABC, abstractmethod
from typing import Union


class Function:
    def __init__(self, name):
        super().__init__()
        self.name = name

    @abstractmethod
    def evaluate(self, x):
        pass


class Variable(Function):
    def __init__(self, name):
        super().__init__()

    def evaluate(self, x: Number):
        return x


class Number(Function):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Rational(Number):
    def __init__(self):
        super().__init__()
