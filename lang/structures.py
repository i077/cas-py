import math
import numpy as np
import operator as op
from abc import ABC, abstractmethod
from State import State
from functools import reduce

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
    op_str = {
        op.mul: '*',
        op.truediv: '/',
        op.add: '+',
        op.sub: '-',
        op.pow: '^'
    }

    def __init__(self, op: callable, *terms: List[Function]):
        # how should we handle expressions taken to powers?
        # nvm we don't handle it here
        self.op = op
        self.terms = *terms

    def evaluate(self, state: State):

        # TODO: Fix this once we've implemented simplification of expressions with variables
        # TODO: WHY IS THIS HERE AND NOT IN REPR
        if any(isinstance(term, str) for term in self.terms):
            return Expression.op_str[self.op].join(str(term) for term in self.terms)
        else:
            return reduce(self.op, [term.evaluate(state) for term in self.terms])


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

    def __repr__(self):
        return Expression.op_str[self.op].join(str(term) for term in self.terms)



class Variable(Function):
    def __init__(self, state, base_var, subscript=None):
        self.base_var = base_var
        self.name = base_var
        self.subscript = subscript
        if subscript is not None:
            self.name += '_{' + str(subscript.evaluate(state)) + '}'

    def evaluate(self, state: State):
        #reevaluate subscript with current state
        if self.subscript is not None:
            new_name = self.base_var + '_{' + str(self.subscript.evaluate(state)) + '}'
        else:
            new_name = self.name

        if self.name in state or new_name in state:
            #replace this variable's key in state with new variable name
            if new_name != self.name and self.name in state:
                state.replace(self.name, new_name)
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

    def evaluate(self, state: State):
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
        #if it's an integer, print as an integer
        if self.value == float('inf'):
            return '\\infty'
        if self.value == float('-inf'):
            return '-\\infty'
        if int(self.value) == self.value:
            return str(int(self.value))
        return str(self.value)

class Cases(Function):
    def __init__(self, cases_list):
        self.cases_list = cases_list

    def evaluate(self, state: State):
        for row in self.cases_list:
            if not isinstance(row[1], Relation):
                raise Exception(f"Improper Cases: {row[1]} is not a relation")
            if row[1].evaluate(state):
                return row[0].evaluate(state)

        #no conditions were satisfied
        raise Exception("Improper Cases: No case satisfied!")

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def derivative(self):
        pass

    def integral(self):
        pass

    def __repr__(self):
        rep = '\\begin{cases}\n'
        for row in self.cases_list:
            rep += str(row[0]) + '&' + str(row[1]) + '\\\\'
        rep += '\n\\end{cases}'
        return rep


class Matrix(Function):
    def __init__(self, mat: list, type: str):
        self.mat = np.array(mat)
        self.type = type

    def evaluate(self, state: State):
        return np.vectorize(lambda entry: entry.evaluate(state))(
            self.mat
        )

    def __eq__(self, other):
        if not isinstance(other, Matrix) or self.mat.shape != other.mat.shape:
            return False
        return (self.mat == other.mat).all()

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        pass

    def integral(self):
        pass

    def __repr__(self):
        mat_string = ''
        for row in self.mat:
            for entry in row[:-1]:
                mat_string += str(entry) + '&'
            mat_string += str(row[-1]) + '\\\\'

        return f'\\begin{{{self.type}}}{mat_string}\\end{{{self.type}}}'


class Relation():
    def __init__(self, rel_chain):
        self.rel_chain = rel_chain

    def evaluate(self, state):
        for i in range(1,len(self.rel_chain)-1,2):
            rel = self.rel_chain[i]
            left = self.rel_chain[i-1].evaluate(state)
            right = self.rel_chain[i+1].evaluate(state)
            if isinstance(right, (float, int)) and isinstance(left, (float, int)):
                if not rel(left, right):
                    return False
            else:
                raise ValueError(f'Cannot compute relation {rel} on {left} and {right}')
        return True


class UserDefinedFunc():
    def __init__(self, args: list, func_body: Expression):
        self.args = args
        self.func_body = func_body

    def evaluate(self, state: State):
        return None

    def __repr__(self):
        return str(tuple(self.args)) + '\\to' + str(self.func_body)

class FunctionCall():
    def __init__(self, function, passed_args: list):
        self.function = function
        self.passed_args = passed_args

    def evaluate(self, state: State):
        if isinstance(self.function, UserDefinedFunc):
            if self.passed_args:
                state.push_layer()
                for arg, value in zip(self.function.args, self.passed_args):
                    state[arg.name] = value
                result = self.function.func_body.evaluate(state)
                state.pop_layer()
            else:
                result = self.function.func_body.evaluate(state)
            return result
        else:
            eval_args = [float(arg.evaluate(state)) for arg in self.passed_args]
            return self.function(*eval_args)

class SumFunc():
    def __init__(self, var: Variable, lower_bound_expr, upper_bound_expr, sum_expr):
        self.var = var
        self.sum_expr = sum_expr
        self.upper_bound_expr = upper_bound_expr
        self.lower_bound_expr = lower_bound_expr

    def evaluate(self, state: State):
        lower_bound = self.lower_bound_expr.evaluate(state)
        if not isinstance(lower_bound, int):
            raise Exception("Sum lower bound must evaluate to integer")
        upper_bound = self.upper_bound_expr.evaluate(state)
        if upper_bound == float('inf'):
            #TODO
            pass
        if not isinstance(upper_bound, int):
            raise Exception("Sum upper bound must evaluate to integer")

        state.push_layer()
        max_bound = max(upper_bound, lower_bound)
        min_bound = min(upper_bound, lower_bound)
        sum_val = 0
        for i in range(min_bound, max_bound+1):
            state[self.var.name] = Number(i)
            sum_val += float(self.sum_expr.evaluate(state))
        state.pop_layer()
        return sum_val

    def __repr__(self):
        return f'\\sum_{{{self.var.name} = {self.lower_bound_expr}}}^{{{self.upper_bound_expr}}}{{{self.sum_expr}}}'

class ProdFunc():
    def __init__(self, var: Variable, lower_bound_expr, upper_bound_expr, prod_expr):
        self.var = var
        self.prod_expr = prod_expr
        self.upper_bound_expr = upper_bound_expr
        self.lower_bound_expr = lower_bound_expr

    def evaluate(self, state: State):
        lower_bound = self.lower_bound_expr.evaluate(state)
        if not isinstance(lower_bound, int):
            raise Exception("Prod lower bound must evaluate to integer")
        upper_bound = self.upper_bound_expr.evaluate(state)
        if upper_bound == float('inf'):
            #TODO
            pass
        if not isinstance(upper_bound, int):
            raise Exception("Prod upper bound must evaluate to integer")

        state.push_layer()
        max_bound = max(upper_bound, lower_bound)
        min_bound = min(upper_bound, lower_bound)
        prod_val = 1
        for i in range(min_bound, max_bound+1):
            state[self.var.name] = Number(i)
            prod_val *= float(self.prod_expr.evaluate(state))
        state.pop_layer()
        return prod_val

    def __repr__(self):
        return f'\\prod_{{{self.var.name} = {self.lower_bound_expr}}}^{{{self.upper_bound_expr}}}{{{self.prod_expr}}}'

class Limit():
    def __init__(self, var: Variable, lim_to, expr):
        self.var = var
        self.lim_to = lim_to
        self.expr = expr

    def evaluate(self, state: State):
        #TODO
        pass

    def __repr__(self):
        return f'\\lim_{{{self.var} \\to {self.lim_to}}}{{{self.expr}}}'

class Integral():
    def __init__(self, lower, upper, expr, var):
        self.lower = lower
        self.upper = upper
        self.expr = expr
        self.var = var

    def evaluate(self, state: State):
        #TODO
        pass

    def __repr__(self):
        return f'\\int_{{{self.lower}}}^{{{self.upper}}}{{{self.expr}\\dd {self.var}}}'

class Floor():
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, state: State):
        return math.floor(self.expr.evaluate(state))

    def __repr__(self):
        return f'\\lfloor {self.expr} \\rfloor'

class Ceiling():
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, state: State):
        return math.ceil(self.expr.evaluate(state))

    def __repr__(self):
        return f'\\lceil {self.expr} \\rceil'

class Derivative():
    def __init__(self, cmd: str, order: Number, expr, var):
        self.cmd = cmd
        self.order = order
        self.expr = expr
        self.var = var

    def evaluate(self, state: State):
        #TODO
        pass

    def __repr__(self):
        if self.order:
            return f'{self.cmd}[{self.order}]{{{self.expr}}}{{{self.var}}}'
        else:
            return f'{self.cmd}{{{self.expr}}}{{{self.var}}}'