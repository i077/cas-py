import math
import operator
from itertools import product, permutations
from abc import ABC, abstractmethod
from collections import Counter
from functools import reduce
from typing import List

import numpy as np
from scipy.special import comb

from State import State
from Dicts import builtin_func_dict, inv_rel_dict


class Function(ABC):
    @abstractmethod
    def evaluate(self, state):
        pass

    def __add__(self, other):
        return Expression(operator.add, self, other)

    def __sub__(self, other):
        return Expression(operator.sub, self, other)

    def __mul__(self, other):
        return Expression(operator.mul, self, other)

    def __truediv__(self, other):
        return Expression(operator.truediv, self, other)

    def __floordiv__(self, other):
        return Expression(operator.floordiv, self, other)

    def __pow__(self, power, modulo=None):
        return Expression(operator.pow, self, power)

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
        operator.mul: "*",
        operator.truediv: "/",
        operator.floordiv: "//",
        operator.add: "+",
        operator.sub: "-",
        operator.pow: "^",
    }

    def __init__(self, op: callable, *terms):
        # how should we handle expressions taken to powers?
        self.op = op
        self.terms = list(terms)
        assert (
            len(self.terms) == 2
            if self.op in [operator.truediv, operator.floordiv, operator.pow]
            else len(self.terms) >= 2
        )

    def evaluate(self, state: State):
        pass
        if self.op != operator.floordiv:
            return reduce(self.op, [term.evaluate(state) for term in self.terms])
        else:
            # floordiv indicates that this is a rational expression that should be stored as a fraction
            # if
            pass

    def __eq__(self, other):
        return (
            isinstance(other, Expression)
            and other.op == self.op
            and Counter(other.terms) == Counter(self.terms)
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        # if addition or subtraction then we just add or subtract the derivatives
        if self.op in [operator.add, operator.sub]:
            return Expression(self.op, *[term.derivative() for term in self.terms])
        # recursive product rule for n terms
        elif self.op == operator.mul:
            # base case for standard product rule
            if len(self.terms) == 2:
                return (
                    self.terms[1] * self.terms[0].derivative()
                    + self.terms[0] * self.terms[1].derivative()
                )
            else:
                remaining_terms = Expression(self.op, *self.terms[1:])
                return (
                    self.terms[0].derivative() * remaining_terms
                    + self.terms[0] * remaining_terms.derivative()
                )
        # quotient rule
        elif self.op in [operator.truediv, operator.floordiv]:
            left, right = self.terms[0], self.terms[1]
            return (left.derivative() * right - right.derivative() * left) / (
                right ** 2
            )
        else:
            raise ValueError

    # TODO: how tf do we do this
    def integral(self):
        pass

    def __repr__(self):
        if self.op == operator.mul:
            return "".join([f"({term})" for term in self.terms]) 
        return Expression.op_str[self.op].join([str(term) for term in self.terms])

    def factor(self):
        assert all(isinstance(x, (Monomial, Number)) for x in self.terms)
        factors = [
            Expression(operator.add, *factor) for factor in kronecker(self.terms)
        ]
        self.op = operator.mul
        self.terms = factors


class Variable(Function):
    def __init__(self, state, base_var, subscript=None):
        self.base_var = base_var
        self.name = base_var
        self.subscript = subscript
        if subscript is not None:
            self.name += "_{" + str(subscript.evaluate(state)) + "}"

    def evaluate(self, state: State):
        # reevaluate subscript with current state
        if self.subscript is not None:
            new_name = self.base_var + "_{" + str(self.subscript.evaluate(state)) + "}"
        else:
            new_name = self.name

        if self.name in state or new_name in state:
            # replace this variable's key in state with new variable name
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
        return Monomial(coeff=1, var=self, power=2) / 2

    def __repr__(self) -> str:
        return self.name


class Monomial(Function):
    def __init__(self, coeff, var: Variable, power):
        self.coeff = coeff
        self.var = var
        self.power = power

    def __add__(self, other):
        if (
            isinstance(other, Monomial)
            and other.var == self.var
            and other.power == self.power
        ):
            return Monomial(self.coeff + other.coeff, self.var, self.power)
        else:
            return super().__add__(other)

    def __sub__(self, other):
        if (
            isinstance(other, Monomial)
            and other.var == self.var
            and other.power == self.power
        ):
            return Monomial(self.coeff - other.coeff, self.var, self.power)
        else:
            return super().__sub__(other)

    def __mul__(self, other):
        if isinstance(other, Monomial) and other.var == self.var:
            return Monomial(
                self.coeff * other.coeff, self.var, other.power + self.power
            )
        else:
            return super().__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Monomial) and other.var == self.var:
            return (
                Monomial(self.coeff, self.var, self.power - other.power) / other.coeff
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
        return Monomial(
            coeff=self.coeff * self.power, var=self.var, power=self.power - 1
        )

    def integral(self):
        return Monomial(coeff=self.coeff, var=self.var, power=self.power + 1) / (
            self.power + 1
        )

    def __repr__(self):
        if self.power == 0:
            return f"{self.coeff}"
        elif self.power == 1:
            return f"{self.coeff if self.coeff != 1 else ''}{self.var}"
        else:
            return f"{self.coeff}{self.var}^{{{self.power}}}"


class Polynomial(Expression):
    def __init__(self, *terms):
        super().__init__(op=operator.add, *terms)


class Number(Function, ABC):
    @staticmethod
    def number_init(value):
        if isinstance(value, (RealNumber, float, int)):
            return RealNumber(value)
        return None

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
    def evaluate(self, state=None):
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
    def __repr__(self):
        pass


class RealNumber(Number):
    def __init__(self, value):
        if isinstance(value, RealNumber):
            self.value = value.value
        elif isinstance(value, (float, int)):
            self.value = value
        else:
            raise ValueError("Improper instantiation of real number")

    def __add__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value + other.value)
        elif isinstance(other, Fraction):
            # addition is commutative and we already implemented Fraction + RealNumber in Fraction
            return other + self
        else:
            return other.__add__(self)

    def __sub__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value - other.value)
        elif isinstance(other, Fraction):
            # subtraction is (almost) commutative and we already implemented Fraction + RealNumber in Fraction
            return RealNumber(-1) * other + self
        else:
            return other.__sub__(self)

    def __mul__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value * other.value)
        elif isinstance(other, Fraction):
            # multiplication is commutative and we already implemented Fraction * RealNumber in Fraction
            return other * self
        else:
            return other.__mul__(self)

    def __truediv__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value / other.value)
        elif isinstance(other, Fraction):
            # divide real number by fraction: a/(b/c) = (ac)/b
            return Fraction.create(self.value * other.den, other.num)
        else:
            return other.__truediv__(self)

    def evaluate(self, state=None):
        if int(self.value) == self.value:
            return int(self.value)
        return self.value

    def __eq__(self, other):
        if isinstance(other, RealNumber):
            return self.value == other.value
        else:
            return other.__eq__(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        return 0

    def integral(self):
        pass

    def __repr__(self):
        # if it's an integer, print as an integer
        if self.value == float("inf"):
            return "\\infty"
        if self.value == float("-inf"):
            return "-\\infty"
        if int(self.value) == self.value:
            return str(int(self.value))
        return str(self.value)


def Fraction(Number):
    """This class represents a numerical fraction at evaluation time, not a rational function, which would be stored
    as Expression with op.truediv/floordiv. For example, this class would hold \\frac{1}{2} but 
    \\frac{x}{2} is an Expression"""

    @staticmethod
    def create(num, den):
        """return a fraction if num and den are both integers and a RealNumber otherwise"""
        assert num is Number and den is Number
        if (isinstance(num, RealNumber) and isinstance(num.value, float)) or (
            isinstance(den, RealNumber) and isinstance(den.value, float)
        ):
            # don't make fractions from floats - just divide them
            return RealNumber(num / den)
        else:
            return Fraction(num, den)

    def __init__(self, top, bottom):
        """don't initialize with Fraction() - use Fraction.create() factory instead"""
        assert top is Number and bottom is Number
        if isinstance(top, RealNumber) and isinstance(bottom, RealNumber):
            self.top = top
            self.bottom = bottom
        else:
            # quotient will be a fraction since either top or bottom is a fraction
            quotient = top / bottom
            self.num = quotient.top
            self.den = quotient.den
        # else:
        #     raise ValueError("Improper instantiation of fraction")

    def __add__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value + other.value)
        else:
            return other.__add__(self)

    def __sub__(self, other):
        if isinstance(other, RealNumber):
            return RealNumber(self.value - other.value)
        else:
            return other.__sub__(self)

    def __mul__(self, other):
        if isinstance(other, RealNumber):
            # multiply fraction by real number: (a/b)*c = (ac)/b
            return Fraction.create(self.num * other, self.den)
        elif isinstance(other, Fraction):
            # multiply fraction by fraction: (a/b)(c/d) = (ac)/(bd)
            return Fraction.create(self.num * other.num, self.den * other.den)
        else:
            return other.__mul__(self)

    def __truediv__(self, other):
        if isinstance(other, RealNumber):
            # divide fraction by real number: (a/b)/c = a/(bc)
            return Fraction.create(self.num, other * self.den)
        if isinstance(other, Fraction):
            # divide fraction by fraction: (a/b)/(c/d) = (ad)/(bc)
            return Fraction.create(self.num * other.den, self.den * other.num)
        else:
            return other.__truediv__(self)

    def evaluate(self, state=None):
        if int(self.value) == self.value:
            return int(self.value)
        return self.value

    def __eq__(self, other):
        if isinstance(other, RealNumber):
            return self.value == other.value
        else:
            return other.__eq__(self)

    def __ne__(self, other):
        return not self.__eq__(other)

    def derivative(self):
        return 0

    def integral(self):
        pass

    def __repr__(self):
        # if it's an integer, print as an integer
        if self.value == float("inf"):
            return "\\infty"
        if self.value == float("-inf"):
            return "-\\infty"
        if int(self.value) == self.value:
            return str(int(self.value))
        return str(self.value)


def numberGCD(a: int, b: int) -> int:
    if b == 0:
        return a
    else:
        return numberGCD(b, a % b)


def listGCD(values, gcd=numberGCD):
    """
    recursively apply a GCD function to a list of values

    Parameters:
    ----------
        values: the list of items over which we want to find the gcd
        gcd: the gcd function

    Returns:
    -------
        the gcd of all values in "values"
    """
    result = values.pop()
    while values:
        result = gcd(result, values.pop())
        # raise ValueError("Improper instantiation of fraction")
    return result


def monomialGCD(a, b) -> Function:
    if isinstance(a, Monomial) and isinstance(b, Monomial) and a.var != b.var:
        return 1
    if isinstance(a, (Number, int)) or isinstance(b, (Number, int)):
        get_value = (
            lambda v: v.coeff
            if isinstance(v, Monomial)
            else (v.value if isinstance(v, Number) else v)
        )
        a = get_value(a)
        b = get_value(b)
        return numberGCD(a, b)

    return Monomial(
        coeff=numberGCD(a.coeff, b.coeff), var=a.var, power=min(a.power, b.power)
    )


class Cases(Function):
    def __init__(self, cases_list):
        self.cases_list = cases_list

    def evaluate(self, state: State):
        for row in self.cases_list:
            if not isinstance(row[1], Relation):
                raise Exception(f"Improper Cases: {row[1]} is not a relation")
            if row[1].evaluate(state):
                return row[0].evaluate(state)

        # no conditions were satisfied
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
        rep = "\\begin{cases}\n"
        for row in self.cases_list:
            rep += str(row[0]) + "&" + str(row[1]) + "\\\\"
        rep += "\n\\end{cases}"
        return rep


class Matrix(Function):
    def __init__(self, mat: list, type: str):
        self.mat = np.array(mat)
        self.type = type

    def evaluate(self, state: State):
        return np.vectorize(lambda entry: entry.evaluate(state))(self.mat)

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
        mat_string = ""
        for row in self.mat:
            for entry in row[:-1]:
                mat_string += str(entry) + "&"
            mat_string += str(row[-1]) + "\\\\"

        return f"\\begin{{{self.type}}}{mat_string}\\end{{{self.type}}}"


class Relation:
    def __init__(self, rel_chain):
        self.rel_chain = rel_chain

    def evaluate(self, state):
        for i in range(1, len(self.rel_chain) - 1, 2):
            rel = self.rel_chain[i]
            left = self.rel_chain[i - 1].evaluate(state)
            right = self.rel_chain[i + 1].evaluate(state)
            if isinstance(right, (float, int)) and isinstance(left, (float, int)):
                if not rel(left, right):
                    return False
            else:
                raise ValueError(f"Cannot compute relation {rel} on {left} and {right}")
        return True

    def __repr__(self):
        output = ""
        for ex in self.rel_chain:
            output += str(inv_rel_dict.get(ex, ex))
        return output


class UserDefinedFunc:
    def __init__(self, args: list, func_body: Expression):
        self.args = args
        self.func_body = func_body

    def evaluate(self, state: State):
        return None

    def __repr__(self):
        return str(tuple(self.args)) + "\\to" + str(self.func_body)


class FunctionCall:
    def __init__(self, function_name, passed_args: list):
        self.function_name = function_name
        self.passed_args = passed_args

    def evaluate(self, state: State):
        if self.function_name in builtin_func_dict:
            eval_args = [float(arg.evaluate(state)) for arg in self.passed_args]
            return builtin_func_dict[self.function_name](*eval_args)
        else:
            function = state[self.function_name]
            if self.passed_args:
                state.push_layer()
                for arg, value in zip(function.args, self.passed_args):
                    # evaluate args here to avoid bugs where passed variable has same name as function arg
                    value = Number.number_init(value.evaluate(state))
                    state[arg.name] = value
                result = function.func_body.evaluate(state)
                state.pop_layer()
            else:
                result = function.func_body.evaluate(state)
            return result


class SumFunc:
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
        if upper_bound == float("inf"):
            # TODO
            pass
        if not isinstance(upper_bound, int):
            raise Exception("Sum upper bound must evaluate to integer")

        state.push_layer()
        max_bound = max(upper_bound, lower_bound)
        min_bound = min(upper_bound, lower_bound)
        sum_val = 0
        for i in range(min_bound, max_bound + 1):
            state[self.var.name] = RealNumber(i)
            sum_val += float(self.sum_expr.evaluate(state))
        state.pop_layer()
        return sum_val

    def __repr__(self):
        return f"\\sum_{{{self.var.name} = {self.lower_bound_expr}}}^{{{self.upper_bound_expr}}}{{{self.sum_expr}}}"


class ProdFunc:
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
        if upper_bound == float("inf"):
            # TODO
            pass
        if not isinstance(upper_bound, int):
            raise Exception("Prod upper bound must evaluate to integer")

        state.push_layer()
        max_bound = max(upper_bound, lower_bound)
        min_bound = min(upper_bound, lower_bound)
        prod_val = 1
        for i in range(min_bound, max_bound + 1):
            state[self.var.name] = RealNumber(i)
            prod_val *= float(self.prod_expr.evaluate(state))
        state.pop_layer()
        return prod_val

    def __repr__(self):
        return f"\\prod_{{{self.var.name} = {self.lower_bound_expr}}}^{{{self.upper_bound_expr}}}{{{self.prod_expr}}}"


class Limit:
    def __init__(self, var: Variable, lim_to, expr):
        self.var = var
        self.lim_to = lim_to
        self.expr = expr

    def evaluate(self, state: State):
        # TODO
        pass

    def __repr__(self):
        return f"\\lim_{{{self.var} \\to {self.lim_to}}}{{{self.expr}}}"


class Integral:
    def __init__(self, lower, upper, expr, var):
        self.lower = lower
        self.upper = upper
        self.expr = expr
        self.var = var

    def evaluate(self, state: State):
        # TODO
        pass

    def __repr__(self):
        return f"\\int_{{{self.lower}}}^{{{self.upper}}}{{{self.expr}\\dd {self.var}}}"


class Floor:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, state: State):
        return math.floor(self.expr.evaluate(state))

    def __repr__(self):
        return f"\\lfloor {self.expr} \\rfloor"


class Ceiling:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, state: State):
        return math.ceil(self.expr.evaluate(state))

    def __repr__(self):
        return f"\\lceil {self.expr} \\rceil"


class Derivative:
    def __init__(self, cmd: str, order: RealNumber, expr, var):
        self.cmd = cmd
        self.order = order
        self.expr = expr
        self.var = var

    def evaluate(self, state: State):
        # TODO
        pass

    def __repr__(self):
        if self.order:
            return f"{self.cmd}[{self.order}]{{{self.expr}}}{{{self.var}}}"
        else:
            return f"{self.cmd}{{{self.expr}}}{{{self.var}}}"


class Root:
    def __init__(self, expr, n=None):
        self.expr = expr
        self.n = n

    def evaluate(self, state: State):
        if self.n is None:
            return math.sqrt(self.expr.evaluate(state))
        n = self.n.evaluate()
        if n == 0:
            raise ValueError(f"Can't take 0th root of {self.expr}")
        return math.pow(self.expr.evaluate(state), 1 / n)

    def __repr__(self):
        if self.n is None:
            return f"\\sqrt{{{self.expr}}}"
        return f"\\sqrt[{self.n}]{{{self.expr}}}"


class Choose:
    def __init__(self, n, k):
        self.n = n
        self.k = k

    def evaluate(self, state: State):
        n = self.n.evaluate(state)
        k = self.k.evaluate(state)
        return comb(n, k)

    def __repr__(self):
        return f"\\binom{{{self.n}}}{{{self.k}}}"


# get all the degrees of the current polynomial
def get_degrees(poly):
    degrees = []
    for mon in poly:
        if isinstance(mon, Monomial):
            degrees.append(mon.power)
        else:
            degrees.append(0)
    return degrees


# find the index of a monomial with a given power
def power_poly_index(poly, power):
    for x in range(len(poly)):
        if isinstance(poly[x], Monomial) and power == poly[x].power:
            return x
    return -1


# find the highest power of a polynomial
def get_highest_pow(poly):
    if isinstance(poly, RealNumber):
        return 0
    for mon in poly:
        if isinstance(mon, RealNumber):
            return 0
        elif mon.coeff != 0:
            return mon.power
    return 0


# find the largest power with a nonzero coefficient in a polynomial
def get_highest_coeff(poly):
    for mon in poly:
        if mon.coeff != 0:
            return mon.coeff


# add intermediate monomials that are missing from a polynomial
def add_missing_degrees(poly, numerator_high_pow):
    num_degrees = get_degrees(poly)
    pot_missing = list(np.arange(0, numerator_high_pow + 1)[::-1])
    upd_poly = []

    poly = [
        poly[power_poly_index(poly, x)]
        if x in num_degrees and x != 0
        else Monomial(0, poly[0].var, x)
        if x not in num_degrees and x != 0
        else poly[power_poly_index(poly, x)]
        if x in num_degrees
        else RealNumber(0)
        for x in pot_missing
    ]

    if isinstance(poly[-1], Monomial) and poly[-1].power == 0:
        poly[-1] = RealNumber(poly[-1].coeff)
    return poly


# remove monomials that have a zero coefficient until you have a monomial with a nonzero
# coefficient (in order of descending powers)
def remove_leading_zeros(poly):
    for x in range(len(poly)):
        if isinstance(poly[x], RealNumber):
            return poly[x]
        if poly[x].coeff != 0:
            return poly[x:]


# polynomial division with a numerator and denominator
def poly_div(num_poly, den_poly):
    high_num_poly_deg = num_poly[0].power
    quotient = [0] * high_num_poly_deg

    # add the missing degrees for the numerator polynomial and denominator polynomial
    num_poly = add_missing_degrees(num_poly, high_num_poly_deg)
    den_poly = add_missing_degrees(den_poly, high_num_poly_deg)

    remainder = num_poly
    i = 0

    remain_high_deg = get_highest_pow(remainder)
    deg_den = get_highest_pow(den_poly)

    # while the power of the remainder is higher than that of the denominator,
    # divide the numerator by the denominator
    while remain_high_deg >= deg_den:
        quotient[i], remainder = poly_divide_one_iter(remainder, den_poly)
        remain_high_deg = get_highest_pow(remainder)
        i += 1
    quotient = list(filter((0).__ne__, quotient))
    return (quotient, remainder)


# run one iteration of polynomial division
def poly_divide_one_iter(num_poly, den_poly):
    deg_num = get_highest_pow(num_poly)
    deg_den = get_highest_pow(den_poly)
    quotient = Monomial(
        get_highest_coeff(num_poly) / get_highest_coeff(den_poly),
        num_poly[0].var,
        deg_num - deg_den,
    )
    mult = [
        quotient * mon
        if isinstance(mon, Monomial)
        else Monomial(
            (RealNumber(quotient.coeff) * mon).value, quotient.var, quotient.power
        )
        for mon in den_poly
    ]
    mult = remove_leading_zeros(mult)

    eq_length_mult = add_missing_degrees(mult, deg_num)
    eq_length_rem = add_missing_degrees(num_poly, deg_num)

    subtract_from_rem = [
        eq_length_rem[x] - eq_length_mult[x]
        if type(eq_length_rem[x]) is type(eq_length_mult[x])
        else RealNumber(eq_length_rem[x]) - eq_length_mult[x]
        if isinstance(eq_length_mult[x], RealNumber)
        else eq_length_rem[x] - RealNumber(eq_length_mult[x])
        for x in range(len(eq_length_mult))
    ]

    remainder = subtract_from_rem
    remain_high_deg = get_highest_pow(remainder)
    remainder = remove_leading_zeros(remainder)

    if deg_num == deg_den:
        quotient = RealNumber(quotient.coeff)
    return quotient, remainder


# find the greatest common divisor between a and b
# highest degree of a must be higher than that of b
def polynomialGCD(a, b):
    while b != 0:
        quotient, remainder = poly_divide_one_iter(a, b)
        a = b
        b = remainder
    if a == 0 or isinstance(a, RealNumber):
        return a
    leading_coeff = a[0].coeff
    for index in range(len(a)):
        if isinstance(a[index], Monomial):
            a[index].coeff /= leading_coeff
        else:
            a[index] /= RealNumber(leading_coeff)
    return a


# plug in number for variable in the polynomial and evaluate
def eval_poly(poly, value):
    sum = 0
    for mon in poly:
        if isinstance(mon, Monomial):
            sum += mon.coeff * value ** mon.power
        elif isinstance(mon, RealNumber):
            sum += mon.value
        else:
            sum += mon
    return sum


# factor a polynomial
def kronecker(poly):
    variable = poly[0].var
    f_pow = get_highest_pow(poly)
    g_pow = f_pow // 2
    h_pow = f_pow - g_pow

    last_mon = poly[len(poly) - 1]

    if isinstance(last_mon, Monomial):
        divisor = [Monomial(1, last_mon.var, last_mon.power)]
        q, r = poly_div(poly, divisor)
        return list(kronecker(q), divisor)

    f = [eval_poly(poly, 0), eval_poly(poly, 1), eval_poly(poly, 2)]

    d = []

    for num in f:
        abs_num = abs(num)
        divisor_of_num = []
        for i in range(1, int(abs_num) + 1):
            if abs_num % i == 0:
                divisor_of_num.append(i)
                divisor_of_num.append(-i)
        d.append(divisor_of_num)

    a = list(product(*d))

    b = a[: len(a) // 2]

    for poss_coeff in b:
        all_perm = list(permutations(poss_coeff))
        for perm in set(all_perm):

            poss_poly = []
            coeff = len(perm) - 1
            power = len(perm) - 1
            while power > 0:
                poss_poly.append(Monomial(perm[coeff - power], variable, power))
                power -= 1
            poss_poly.append(RealNumber(perm[coeff]))
            q, r = poly_div(poly, poss_poly)
            if isinstance(r, RealNumber) and r.value == 0:
                return list((kronecker(q), poss_poly))
    return poly


start = State()
x = Variable(start, "x")
first_num = Monomial(1, x, 5)
second_num = Monomial(-1, x, 4)
third_num = Monomial(8, x, 3)
fourth_num = Monomial(-2, x, 2)
fifth_num = Monomial(14, x, 1)
sixth_num = RealNumber(5)
poly = [first_num, second_num, third_num, fourth_num, fifth_num, sixth_num]
ex = Expression(operator.add, *poly)
ex.factor()
print(ex)
