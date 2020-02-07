from abc import ABC, abstractmethod
from operator import add, sub, mul, truediv, lt, gt, le, ge, eq, ne, pow


class Function(ABC):
    @abstractmethod
    def evaluate(self, x):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def __pow__(self, power, modulo=None):
        pass

    @abstractmethod
    def __lt__(self, other):
        pass

    @abstractmethod
    def __gt__(self, other):
        pass

    @abstractmethod
    def __ge__(self, other):
        pass

    @abstractmethod
    def __le__(self, other):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def derivative(self):
        pass

    @abstractmethod
    def integral(self):
        pass


class Expression(Function):
    def __init__(self, op, left: Function, right: Function):
        self.op = op
        self.left = left
        self.right = right

    def evaluate(self, x):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def derivative(self):
        pass

    def integral(self):
        pass


class Variable(Function):
    def __init__(self, name):
        self.name = name

    def evaluate(self, x):
        return x

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, f) -> bool:
        return isinstance(f, Variable) and f.name == self.name

    def __ne__(self, other):
        pass

    def derivative(self):
        return 1

    def integral(self):
        pass

    def __repr__(self) -> str:
        return self.name


class Polynomial(Function):
    def __init__(self, coeff, var: Variable, power):
        self.coeff = coeff
        self.var = var
        self.power = power

    def evaluate(self, x):
        val = x.value if isinstance(x, Number) else x
        return self.coeff * (val ** self.power)

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def derivative(self):
        return Polynomial(
            coeff=self.coeff * self.power, var=self.var, power=self.power - 1
        )

    def integral(self):
        pass


class Number(Function):
    def __init__(self, value):
        self.value = value

    def evaluate(self, x=None):
        return self.value

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def derivative(self):
        return 0

    def integral(self):
        pass

    def __repr__(self):
        return self.value


class Fraction(Function):
    def __init__(self, numerator: Function, denominator: Function):
        self.numerator = numerator
        self.denominator = denominator

    def evaluate(self, x):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def __pow__(self, power, modulo=None):
        pass

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __ge__(self, other):
        pass

    def __le__(self, other):
        pass

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def derivative(self):
        return (
            self.numerator.derivative() * self.denominator
            - self.denominator.derivative() * self.numerator
        ) / (self.denominator * self.denominator)

    def integral(self):
        pass
