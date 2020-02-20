from abc import ABC, abstractmethod
import operator as op


class Function(ABC):
    @abstractmethod
    def evaluate(self, x):
        pass

    def __add__(self, other):
        return Expression(op.add, self, other)

    def __sub__(self, other):
        return Expression(op.sub, self, other)

    def __mul__(self, other):
        return Expression(op.mul, self, other)

    def __truediv__(self, other):
        return Expression(op.truediv, self, other)

    def __pow__(self, power, modulo=None):
        pass

    def __lt__(self, other):
        return Expression(op.lt, self, other)

    def __gt__(self, other):
        return Expression(op.gt, self, other)

    def __ge__(self, other):
        return Expression(op.ge, self, other)

    def __le__(self, other):
        return Expression(op.le, self, other)

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
    def __init__(self, op, left: Function, right: Function, power=1):
        self.op = op
        self.left = left
        self.right = right
        self.pow = power

    def evaluate(self, x):
        return self.op(self.left.evaluate(x), self.right.evaluate(x))

    def __eq__(self, other):
        return isinstance(other, Expression) and other.left == self.left \
                                             and other.right == self.right\
                                             and other.op == self.op

    def __ne__(self, other):
        return not isinstance(other, Expression) and other.left == self.left \
                                             and other.right == self.right\
                                             and other.op == self.op

    def derivative(self):
        pass

    def integral(self):
        pass


class Variable(Function):
    def __init__(self, name):
        self.name = name

    def evaluate(self, x):
        return x

    def __eq__(self, f) -> bool:
        return isinstance(f, Variable) and f.name == self.name

    def __ne__(self, other):
        return not isinstance(other, Variable) and other.name == self.name

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
