import math
import operator as op
import sys

import numpy as np
import sympy
from antlr4 import CommonTokenStream, FileStream, InputStream

from Dicts import matrix_type_dict, rel_dict
from LaTeXLexer import LaTeXLexer
from LaTeXParser import LaTeXParser as parse
from LaTeXVisitor import LaTeXVisitor
from State import State
from structures import (
    Cases,
    CastleException,
    Ceiling,
    Choose,
    ComplexNumber,
    Derivative,
    Determinant,
    Expression,
    Floor,
    FunctionCall,
    Integral,
    Limit,
    Matrix,
    Monomial,
    Number,
    RealNumber,
    Root,
    ProdFunc,
    Relation,
    SumFunc,
    UserDefinedFunc,
    Variable,
)


class CastleVisitor(LaTeXVisitor):
    def __init__(self, state: State):
        self.state = state

    def visitEntry(self, ctx: parse.EntryContext):
        """entry
        castle_input EOF """
        return str(self.visit(ctx.castle_input()).evaluate(self.state))

    # 5-function Arithmetic ====================================================
    def visitAdd_expr_recurse(self, ctx: parse.Add_expr_recurseContext):
        """add_expr_recurse
        add_expr op=(PLUS | MINUS) add_expr"""
        return Expression(
            op.add if ctx.op.type == parse.PLUS else op.sub,
            self.visit(ctx.add_expr(0)),
            self.visit(ctx.add_expr(1)),
        )

    def visitIme_mult(self, ctx: parse.Ime_multContext):
        """implicit_mult_expr_mult
        implicit_mult_expr implicit_mult_expr"""
        return Expression(
            op.mul,
            self.visit(ctx.implicit_mult_expr(0)),
            self.visit(ctx.implicit_mult_expr(1)),
        )

    def visitIme_left(self, ctx: parse.Ime_leftContext):
        """implicit_mult_expr_left
        left_implicit_pow_expr (implicit_mult_expr | var_pow_expr | paren_pow_expr)?"""
        if ctx.implicit_mult_expr():
            return Expression(
                op.mul,
                self.visit(ctx.left_implicit_pow_expr()),
                self.visit(ctx.implicit_mult_expr()),
            )
        if ctx.var_pow_expr():
            return Expression(
                op.mul,
                self.visit(ctx.left_implicit_pow_expr()),
                self.visit(ctx.var_pow_expr()),
            )
        if ctx.paren_pow_expr():
            return Expression(
                op.mul,
                self.visit(ctx.left_implicit_pow_expr()),
                self.visit(ctx.paren_pow_expr()),
            )
        else:
            return self.visit(ctx.left_implicit_pow_expr())

    def visitIme_var_unit_paren_left(self, ctx: parse.Ime_var_unit_paren_leftContext):
        """ime_var_unit_paren_left
        (var_pow_expr | paren_pow_expr) implicit_mult_expr"""
        if ctx.var_pow_expr():
            left_expr = self.visit(ctx.var_pow_expr())
        elif ctx.paren_pow_expr():
            left_expr = self.visit(ctx.paren_pow_expr())
        return Expression(op.mul, left_expr, self.visit(ctx.implicit_mult_expr()))

    def visitIme_var_unit_paren_right(self, ctx: parse.Ime_var_unit_paren_rightContext):
        """ime_var_unit_paren_right
        implicit_mult_expr (var_pow_expr | paren_pow_expr)"""
        if ctx.var_pow_expr():
            right_expr = self.visit(ctx.var_pow_expr())
        elif ctx.paren_pow_expr():
            right_expr = self.visit(ctx.paren_pow_expr())
        return Expression(op.mul, self.visit(ctx.implicit_mult_expr()), right_expr)

    def visitIme_paren_var(self, ctx: parse.Ime_paren_varContext):
        """ime_paren_var
        paren_pow_expr var_pow_expr"""
        return Expression(
            op.mul, self.visit(ctx.paren_pow_expr()), self.visit(ctx.var_pow_expr())
        )

    def visitIme_var_var(self, ctx: parse.Ime_var_varContext):
        """ime_var_var
        var_pow_expr var_pow_expr"""
        return Expression(
            op.mul, self.visit(ctx.var_pow_expr(0)), self.visit(ctx.var_pow_expr(1))
        )

    def visitIme_paren_paren(self, ctx: parse.Ime_paren_parenContext):
        """ime_paren_paren
        paren_pow_expr paren_pow_expr"""
        return Expression(
            op.mul, self.visit(ctx.paren_pow_expr(0)), self.visit(ctx.paren_pow_expr(1))
        )

    def visitVar_pow_expr(self, ctx: parse.Var_pow_exprContext):
        """var_pow_expr
        var (CARET tex_symb)?"""
        exponent = ctx.tex_symb()
        if exponent is None:
            return self.visit(ctx.var())
        return Expression(op.pow, self.visit(ctx.var()), self.visit(exponent))

    def visitParen_pow_expr(self, ctx: parse.Paren_pow_exprContext):
        """paren_pow_expr
        paren (CARET tex_symb)?"""
        exponent = ctx.tex_symb()
        if exponent is None:
            return self.visit(ctx.unit_paren())
        return Expression(op.pow, self.visit(ctx.unit_paren()), self.visit(exponent))

    def visitMult_expr_recurse(self, ctx: parse.Mult_expr_recurseContext):
        """mult_expr_recurse
        mult_expr op=(MULT | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV) mult_expr """
        return Expression(
            op.truediv if ctx.op.type in {parse.DIV, parse.CMD_DIV} else op.mul,
            self.visit(ctx.mult_expr(0)),
            self.visit(ctx.mult_expr(1)),
        )

    def visitMult_sign(self, ctx: parse.Mult_signContext):
        """mult_sign
        sign=(PLUS | MINUS) mult_expr """
        if ctx.sign.type == parse.MINUS:
            return Expression(op.mul, RealNumber(-1), self.visit(ctx.mult_expr()))
        else:
            return self.visit(ctx.mult_expr())

    def visitImplicit_pow_expr_recurse(
        self, ctx: parse.Implicit_pow_expr_recurseContext
    ):
        """implicit_pow_expr_recurse
        implicit_pow_expr CARET tex_symb """
        return Expression(
            op.pow, self.visit(ctx.implicit_pow_expr()), self.visit(ctx.tex_symb())
        )

    def visitLeft_implicit_pow_expr_recurse(
        self, ctx: parse.Left_implicit_pow_expr_recurseContext
    ):
        """left_implicit_pow_expr_recurse
        left_implicit_pow_expr CARET tex_symb """
        return Expression(
            op.pow, self.visit(ctx.left_implicit_pow_expr()), self.visit(ctx.tex_symb())
        )

    def visitPow_expr_recurse(self, ctx: parse.Pow_expr_recurseContext):
        """pow_expr_recurse
        pow_expr CARET tex_symb """
        return Expression(
            op.pow, self.visit(ctx.pow_expr()), self.visit(ctx.tex_symb())
        )

    # Units =====================================================================
    def visitUnit_paren(self, ctx: parse.Unit_parenContext):
        """unit_paren
        LPAREN expr RPAREN """
        return self.visit(ctx.expr())

    def visitUnit_infinity(self, ctx: parse.Unit_infinityContext):
        """unit_infinity
        inf=(INFINITY | NEG_INFINITY)"""
        if ctx.inf.type == parse.INFINITY:
            return RealNumber(float("inf"))
        else:
            return RealNumber(float("-inf"))

    def visitUnit_pi(self, ctx: parse.Unit_piContext):
        return RealNumber(math.pi)

    def visitUnit_e(self, ctx: parse.Unit_eContext):
        return RealNumber(math.e)

    def visitUnit_i(self, ctx: parse.Unit_iContext):
        # i = 0 + 1i
        return ComplexNumber.create(RealNumber(0), RealNumber(1))

    def visitNumber(self, ctx: parse.NumberContext):
        """number
        MINUS? DIGIT+ (POINT DIGIT*)? """
        return RealNumber(float(ctx.getText()))

    def visitNnint(self, ctx: parse.NnintContext):
        """nnint
        DIGIT+ """
        return RealNumber(int(ctx.getText()))

    def visitFraction(self, ctx: parse.FractionContext):
        """fraction
        CMD_FRAC LCURLY expr RCURLY LCURLY expr RCURLY"""
        # use the floordiv // operator to represent a fraction
        return Expression(op.floordiv, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Variable names and TeX symbols ===============================================
    def visitVar_name_letter(self, ctx: parse.Var_name_letterContext):
        """var_name_letter
           LETTER """
        return ctx.getText()

    def visitMultichar_var(self, ctx: parse.Multichar_varContext):
        """multichar_var
        (LETTER | DIGIT)+ """
        return ctx.getText()

    def visitVar_name_multichar(self, ctx: parse.Var_name_multicharContext):
        """var_name_multichar
        BACKTICK name=multichar_var BACKTICK """
        return self.visit(ctx.name)

    def visitTex_symb_single(self, ctx: parse.Tex_symb_singleContext):
        """tex_symb_single
        (NON_EI_LETTER | E | I | DIGIT) """
        if ctx.E():
            return RealNumber(np.e)
        if ctx.I():
            return ComplexNumber.create(RealNumber(0), RealNumber(1))
        text = ctx.getText()
        if ctx.DIGIT():
            return RealNumber(int(text))
        else:
            return Variable(self.state, text)

    def visitTex_symb_multi(self, ctx: parse.Tex_symb_multiContext):
        """tex_symb_multi
        LCURLY expr RCURLY """
        return self.visit(ctx.expr())

    def visitTex_symb_recurse(self, ctx: parse.Tex_symb_recurseContext):
        """tex_symb_recurse
        LCURLY var RCURLY """
        return self.visit(ctx.var())

    def visitVar(self, ctx: parse.VarContext):
        """var
        var_name (UNDERSCORE tex_symb)?
        var used to reference variable's value in an expression"""
        var = self.visit(ctx.var_name())
        subscript = self.visit(ctx.tex_symb()) if ctx.tex_symb() else None
        return Variable(self.state, var, subscript)

    # Variable and function assignments ========================================
    def visitVar_def(self, ctx: parse.Var_defContext):
        """var_def
        var_name (UNDERSCORE tex_symb)?
        variable name used in assignment (as opposed to var)"""
        var = self.visit(ctx.var_name())
        subscript = self.visit(ctx.tex_symb()) if ctx.tex_symb() else None
        return Variable(self.state, var, subscript)

    def visitVar_assign(self, ctx: parse.Var_assignContext):
        """var_assign
        assign_var ASSIGN expr
        assign a value to a variable in the state"""
        expr = self.visit(ctx.expr())
        self.state[self.visit(ctx.var_def()).name] = expr
        return expr

    def visitFunc_assign(self, ctx: parse.Func_assignContext):
        """func_assign
        assign_var ASSIGN func_def
        assign a value to a function in the state"""
        func_def = self.visit(ctx.func_def())
        self.state[self.visit(ctx.var_def()).name] = func_def
        return func_def

    # Function definitions ======================================================
    def visitArg_list(self, ctx: parse.Arg_listContext):
        args = ctx.var_def()
        if not args:
            return None
        if not isinstance(args, (list, tuple)):
            return [self.visit(args)]
        return [self.visit(arg) for arg in args]

    def visitFunc_def(self, ctx: parse.Func_defContext):
        args = self.visit(ctx.arg_list())
        func_body = self.visit(ctx.expr())
        return UserDefinedFunc(args, func_body)

    # Function calls ============================================================
    def visitFunc_custom(self, ctx: parse.Func_customContext):
        """func_custom (user-defined function call)
        var LPAREN (expr (COMMA expr)+)? RPAREN"""
        function_name = self.visit(ctx.var()).name
        args = ctx.expr()
        if not args:
            args = []
        elif not isinstance(args, (list, tuple)):
            args = [self.visit(args)]
        else:
            args = [self.visit(arg) for arg in args]

        return FunctionCall(function_name, args)

    def visitFunc_call_builtin(self, ctx: parse.Func_call_builtinContext):
        """func_call_builtin
        func_builtin (LCURLY and/or LPAREN) expr ((COMMA expr)+)*)? (RCURLY and/or RPAREN)"""
        function_name = self.visit(ctx.func_builtin())
        args = ctx.expr()
        if not args:
            args = []
        elif not isinstance(args, (list, tuple)):
            args = [self.visit(args)]
        else:
            args = [self.visit(arg) for arg in args]

        return FunctionCall(function_name, args)

    def visitFunc_sum(self, ctx: parse.Func_sumContext):
        lower = self.visit(ctx.relation())
        upper_bound = self.visit(ctx.tex_symb())
        sum_expr = self.visit(ctx.expr())

        if not (
            isinstance(lower, Relation)
            and len(lower.rel_chain) == 3
            and lower.rel_chain[1] == rel_dict[parse.EQ]
            and isinstance(lower.rel_chain[0], Variable)
        ):
            raise CastleException("Lower sum term should be var = expr")

        return SumFunc(lower.rel_chain[0], lower.rel_chain[2], upper_bound, sum_expr)

    def visitFunc_prod(self, ctx: parse.Func_prodContext):
        lower = self.visit(ctx.relation())
        upper_bound = self.visit(ctx.tex_symb())
        prod_expr = self.visit(ctx.expr())

        if not (
            isinstance(lower, Relation)
            and len(lower.rel_chain) == 3
            and lower.rel_chain[1] == rel_dict[parse.EQ]
            and isinstance(lower.rel_chain[0], Variable)
        ):
            raise CastleException("Lower product term should be var = expr")

        return ProdFunc(lower.rel_chain[0], lower.rel_chain[2], upper_bound, prod_expr)

    def visitFunc_lim(self, ctx: parse.Func_limContext):
        return Limit(
            self.visit(ctx.var()), self.visit(ctx.expr(0)), self.visit(ctx.expr(1))
        )

    def visitFunc_int(self, ctx: parse.Func_intContext):
        return Integral(
            self.visit(ctx.tex_symb(0)),
            self.visit(ctx.tex_symb(1)),
            self.visit(ctx.expr()),
            self.visit(ctx.var()),
        )

    def visitFunc_floorceil(self, ctx: parse.Func_floorceilContext):
        left, right = ctx.lop.type, ctx.rop.type
        if left == parse.CMD_LFLOOR:
            if right != parse.CMD_RFLOOR:
                raise CastleException("Unmatched left floor operator")
            return Floor(self.visit(ctx.expr()))

        if left == parse.CMD_LCEIL:
            if right != parse.CMD_RCEIL:
                raise CastleException("Unmatched left ceiling operator")
            return Ceiling(self.visit(ctx.expr()))

    def visitFunc_deriv(self, ctx: parse.Func_derivContext):
        order = ctx.nnint()
        return Derivative(
            "\\dv" if ctx.op.type == parse.FUNC_DV else "\\pdv",
            self.visit(order) if order else None,
            self.visit(ctx.expr()),
            self.visit(ctx.var()),
        )

    def visitFunc_root(self, ctx: parse.Func_rootContext):
        exprs = ctx.expr()
        if len(exprs) > 1:
            # n-th root instead of default square root
            return Root(self.visit(exprs[1]), n=self.visit(exprs[0]))
        return Root(self.visit(exprs[0]))

    def visitFunc_choose(self, ctx: parse.Func_chooseContext):
        return Choose(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitFunc_builtin(self, ctx: parse.Func_builtinContext):
        return ctx.name.type

    def visitVar_parens(self, ctx: parse.Var_parensContext):
        """var_parens (the ambiguous y(x+1) structure)
        var LPAREN expr RPAREN (CARET tex_symb)?"""
        # tex_symb is present if the var_parens structure is raised to a power:
        # for example y(x+1)^2
        var = self.visit(ctx.var())
        var_val = self.state.get(var.name)
        expr = self.visit(ctx.expr())
        exponent = ctx.tex_symb()
        if var_val is None:
            raise Exception(f"Variable {var.name} not found")
        if isinstance(var_val, UserDefinedFunc):
            # the variable is a function, so call it
            if exponent is not None:
                return Expression(
                    op.pow, FunctionCall(var.name, [expr]), self.visit(exponent)
                )
            else:
                return FunctionCall(var.name, [expr])

        else:  # otherwise this is a multiplication
            if exponent is not None:
                # x((y+1)^z)
                return Expression(
                    op.mul, var, Expression(op.pow, expr, self.visit(exponent))
                )
            else:
                return Expression(op.mul, var, expr)

    # Relations =================================================================
    def visitRelop(self, ctx: parse.RelopContext):
        return ctx.op.type

    def visitRelation(self, ctx: parse.RelationContext):
        rep = []
        ops = [self.visit(op) for op in ctx.relop()]
        exprs = [self.visit(expr) for expr in ctx.expr()]
        for i in range(len(ctx.relop())):
            rep.append(exprs[i])
            rep.append(rel_dict[ops[i]])
        rep.append(exprs[-1])
        return Relation(rep)

    # Cases =====================================================================
    def visitCases_env(self, ctx: parse.Cases_envContext):
        return self.visit(ctx.cases_exp())

    def visitCases_last_row(self, ctx: parse.Cases_last_rowContext):
        return (self.visit(ctx.expr()), self.visit(ctx.relation()))

    def visitCases_row(self, ctx: parse.Cases_rowContext):
        return (self.visit(ctx.expr()), self.visit(ctx.relation()))

    def visitCases_exp(self, ctx: parse.Cases_expContext):
        return Cases(
            [self.visit(row) for row in ctx.cases_row()]
            + [self.visit(ctx.cases_last_row())]
        )

    # Matrices ===================================================================
    def visitMatrix_env(self, ctx: parse.Matrix_envContext):
        begin_type = ctx.open_mat_type.type
        end_type = ctx.close_mat_type.type
        if begin_type != end_type:
            raise CastleException("Mismatched matrix environments")

        # 'vmatrix' type signifies a determinant
        if begin_type == parse.V_MATRIX:
            return Determinant(self.visit(ctx.matrix_exp()))
        else:
            return Matrix(self.visit(ctx.matrix_exp()), matrix_type_dict[begin_type])

    def visitMatrix_exp(self, ctx: parse.Matrix_expContext):
        return [self.visit(row) for row in ctx.matrix_row()] + [
            self.visit(ctx.matrix_last_row())
        ]

    def visitMatrix_row(self, ctx: parse.Matrix_rowContext):
        entries = ctx.expr()
        if not isinstance(entries, list):
            return self.visit(entries)
        return [self.visit(entry) for entry in entries]

    def visitMatrix_last_row(self, ctx: parse.Matrix_last_rowContext):
        entries = ctx.expr()
        if not isinstance(entries, list):
            return self.visit(entries)
        return [self.visit(entry) for entry in entries]


def evaluate_expression(state: State, expr: str):
    stream = InputStream(expr)
    lexer = LaTeXLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = parse(tokens)
    tree = parser.entry()
    visitor = CastleVisitor(state)
    return (visitor.visit(tree), visitor.state)


def main(argv):
    state = State()
    FILEPATH = "input.txt"
    for line in open(FILEPATH, "r").readlines():
        print(evaluate_expression(state, line)[0])


if __name__ == "__main__":
    main(sys.argv)
