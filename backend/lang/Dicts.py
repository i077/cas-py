import operator as op

import sympy
import math

from backend.lang.LaTeXParser import LaTeXParser as parse

builtin_func_dict = {
    parse.FUNC_SIN: math.sin,
    parse.FUNC_COS: math.cos,
    parse.FUNC_TAN: math.tan,
    parse.FUNC_SEC: sympy.sec,
    parse.FUNC_CSC: sympy.csc,
    parse.FUNC_COT: sympy.cot,
    parse.FUNC_ASIN: sympy.asin,
    parse.FUNC_ACOS: sympy.acos,
    parse.FUNC_ATAN: sympy.atan,
    parse.FUNC_ASEC: sympy.asec,
    parse.FUNC_ACSC: sympy.acsc,
    parse.FUNC_ACOT: sympy.acot,
    parse.FUNC_EXP: math.exp,
    parse.FUNC_LN: math.log,
    parse.FUNC_LOG: math.log,
}

rel_dict = {
    parse.LT: op.lt,
    parse.GT: op.gt,
    parse.LTE: op.le,
    parse.GTE: op.ge,
    parse.EQ: op.eq,
    parse.NEQ: op.ne,
}

inv_rel_dict = {val: key for key, val in rel_dict.items()}
# make \neq render properly in KaTeX
inv_rel_dict[op.ne] = "\\cancel{=}"

matrix_type_dict = {
    parse.MATRIX: "matrix",
    parse.P_MATRIX: "pmatrix",
    parse.B_MATRIX: "bmatrix",
    parse.V_MATRIX: "vmatrix",
}
