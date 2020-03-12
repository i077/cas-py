import math
import operator as op
from abc import ABC, abstractmethod


class Function(ABC):
    @abstractmethod
    def evaluate(self, state):
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
        return Expression(op.pow, self, power)

    # we can't do this unless we specify function domains -- probably too much complexity?
    #     def __lt__(self, other):
    #         return Expression(op.lt, self, other)

    #     def __gt__(self, other):
    #         return Expression(op.gt, self, other)

    #     def __ge__(self, other):
    #         return Expression(op.ge, self, other)

    #     def __le__(self, other):
    #         return Expression(op.le, self, other)

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
    def __init__(self, op: callable, left: Function, right: Function, power=1):
        # how should we handle expressions taken to powers?
        self.op = op
        self.left = left
        self.right = right
        self.pow = power

    def evaluate(self, state: dict):
        l_val = self.left.evaluate(state)
        r_val = self.right.evaluate(state)

        #TODO: Fix this once we've implemented simplification of expressions with variables
        if isinstance(l_val, str) or isinstance(r_val, str):
            op_str = {
                op.mul: '*',
                op.truediv: '/',
                op.add: '+',
                op.sub: '-',
                op.pow: '^'
            }
            return str(l_val) + op_str[self.op] + str(r_val)

        if self.op == op.pow:
            power = r_val
            if isinstance(power, Number):
                if power == 1:
                    return self
                    # why this?
                    # else:
                    #     return self * Expression(op.mul, self, r - 1)
                if power == 0:
                    return Number(1)
                if power < 0:
                    return Number(1) / Expression(op.pow, l_val, abs(power))

            return self.op(l_val, power)

        return self.op(l_val, r_val)

    def __eq__(self, other):
        return (
            isinstance(other, Expression)
            and other.left == self.left
            and other.right == self.right
            and other.op == self.op
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        # if addition or subtraction then we just add or subtract the derivatives
        if self.op in [op.add, op.sub]:
            return self.op(self.left.derivative(), self.right.derivative())
        # product rule
        elif self.op == op.mul:
            return (
                self.left.derivative() * self.right
                + self.left * self.right.derivative()
            )
        # quotient rule
        elif self.op == op.truediv:
            return (
                self.left.derivative() * self.right
                - self.right.derivative() * self.left
            ) / (self.right ** 2)
        else:
            raise ValueError

    # TODO: how tf do we do this
    def integral(self):
        pass


class Variable(Function):
    def __init__(self, state, base_var, subscript=None):
        self.base_var = base_var
        self.name = base_var
        self.subscript = subscript
        if subscript is not None:
            self.name += '_{' + str(subscript.evaluate(state)) + '}'

    def evaluate(self, state: dict):
        #reevaluate subscript with current state
        if self.subscript is not None:
            new_name = self.base_var + '_{' + str(self.subscript.evaluate(state)) + '}'
        else:
            new_name = self.name

        if self.name in state or new_name in state:
            #replace this variable's key in state with new variable name
            if new_name != self.name and self.name in state:
                state[new_name] = state[self.name]
                del state[self.name]
                self.name = new_name
            return state[new_name].evaluate(state)

        self.name = new_name
        return self.name

    def __eq__(self, f) -> bool:
        return isinstance(f, Variable) and f.name == self.name

    def __ne__(self, other):
        return not (isinstance(other, Variable) and other.name == self.name)

    def derivative(self):
        return 1

    def integral(self):
        return Polynomial(coeff=1, var=self, power=2) / 2

    def __repr__(self) -> str:
        return self.name


class Polynomial(Function):
    def __init__(self, coeff, var: Variable, power):
        self.coeff = coeff
        self.var = var
        self.power = power

    def __add__(self, other):
        if (
            isinstance(other, Polynomial)
            and other.var == self.var
            and other.power == self.power
        ):
            return Polynomial(self.coeff + other.coeff, self.var, self.power)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if (
            isinstance(other, Polynomial)
            and other.var == self.var
            and other.power == self.power
        ):
            return Polynomial(self.coeff - other.coeff, self.var, self.power)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Polynomial) and other.var == self.var:
            return Polynomial(
                self.coeff * other.coeff, self.var, other.power + self.power
            )
        else:
            return super().__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Polynomial) and other.var == self.var:
            return (
                Polynomial(self.coeff, self.var, self.power - other.power) / other.coeff
            )
        else:
            return super().__truediv__(other)

    def evaluate(self, state: dict):
        return self.coeff * (state[self.var.name] ** self.power)

    def __eq__(self, other):
        return (
            self.coeff == other.coeff
            and self.var == other.var
            and self.power == other.power
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        return Polynomial(
            coeff=self.coeff * self.power, var=self.var, power=self.power - 1
        )

    def integral(self):
        return Polynomial(coeff=self.coeff, var=self.var, power=self.power + 1) / (
            self.power + 1
        )


class Number(Function):
    def __init__(self, value):
        if isinstance(value, Number):
            self.value = value.value
        else:
            self.value = value

    def __add__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
        else:
            super().__add__(other)

    def __sub__(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)

    def evaluate(self, state=None):
        if int(self.value) == self.value:
            return int(self.value)
        return self.value

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        return 0

    def integral(self):
        pass

    def __repr__(self):
        return str(self.value)
