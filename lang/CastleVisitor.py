import sys
import sympy
import math
from antlr4 import FileStream, InputStream, CommonTokenStream
from LaTeXVisitor import LaTeXVisitor
from LaTeXParser import LaTeXParser as parse
from LaTeXLexer import LaTeXLexer
from structures import Number, Polynomial, Variable, Expression, Cases, Relation, UserDefinedFunc, FunctionCall
from State import State
import operator as op

class CastleVisitor(LaTeXVisitor):
    def __init__(self, state: State):
        self.state = state

    def visitEntry(self, ctx:parse.EntryContext):
        """entry
        castle_input EOF """
        return self.visit(ctx.castle_input()).evaluate(self.state)

    # Basic arithmetic and expr ===================================================
    def visitAdd_expr_recurse(self, ctx:parse.Add_expr_recurseContext):
        """add_expr_recurse
        add_expr op=(PLUS | MINUS) add_expr"""
        return Expression(
            op.add if ctx.op.type == parse.PLUS else op.sub,
            self.visit(ctx.add_expr(0)),
            self.visit(ctx.add_expr(1)),
        )

    def visitMult_expr_recurse(self, ctx:parse.Mult_expr_recurseContext):
        """mult_expr_recurse
        mult_expr op=(MULT | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV) mult_expr """
        return Expression(
            op.truediv if ctx.op.type in {parse.DIV, parse.CMD_DIV} else op.mul,
            self.visit(ctx.mult_expr(0)),
            self.visit(ctx.mult_expr(1)),
        )

    def visitPow_expr_recurse(self, ctx:parse.Pow_expr_recurseContext):
        """pow_expr_recurse
        pow_expr CARET tex_symb """
        return Expression(
            op.pow,
            self.visit(ctx.pow_expr()),
            self.visit(ctx.tex_symb()),
        )

    def visitUnit_recurse(self, ctx:parse.Unit_recurseContext):
        """unit_recurse
        sign=(PLUS | MINUS) unit """
        if ctx.sign.type == parse.MINUS:
            return Expression(op.mul, Number(-1), self.visit(ctx.unit()))
        else:
            return self.visit(ctx.unit())

    def visitUnit_paren(self, ctx:parse.Unit_parenContext):
        """unit_paren
        MINUS? LPAREN expr RPAREN """
        if ctx.MINUS():
            return Expression(op.mul, Number(-1), self.visit(ctx.expr()))
        else:
            return self.visit(ctx.expr())

    def visitNumber(self, ctx:parse.NumberContext):
        """number
        MINUS? DIGIT+ (POINT DIGIT*)? """
        return Number(float(ctx.getText()))


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
        return self.visit(ctx.name())

    def visitTex_symb_single(self, ctx: parse.Tex_symb_singleContext):
        """tex_symb_single
        (LETTER | DIGIT) """
        text = ctx.getText()
        if ctx.DIGIT():
            return Number(int(text))
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
        self.state[self.visit(ctx.var_def())] = expr
        return expr

    def visitFunc_assign(self, ctx: parse.Func_assignContext):
        """func_assign
        assign_var ASSIGN func_def 
        assign a value to a function in the state"""
        func_def = self.visit(ctx.func_def())
        self.state[self.visit(ctx.var_def())] = func_def
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

    def visitFunc_builtin(self, ctx: parse.Func_builtinContext):
        return CastleVisitor.builtin_func_dict[ctx.name.type]


    # Function calls ============================================================
    def visitFunc_call_var(self, ctx: parse.Func_call_varContext):
        function = self.visit(ctx.func_name())
        args = ctx.expr()
        if not args:
            args = ()
        elif not isinstance(args, (list, tuple)):
            args = (self.visit(args))
        else:
            args = (self.visit(arg) for arg in args)
        if isinstance(function, Variable):
            return FunctionCall(self.state[function.name], args)
        return FunctionCall(function, args)


    # Relations =================================================================
    def visitRelop(self, ctx:parse.RelopContext):
        return ctx.op.type

    def visitRelation(self, ctx: parse.RelationContext):
        rep = []
        ops = [self.visit(op) for op in ctx.relop()]
        exprs = [self.visit(expr) for expr in ctx.expr()]
        for i in range(len(ctx.relop())):
            rep.append(exprs[i])
            rep.append(CastleVisitor.rel_dict[ops[i]])
        rep.append(exprs[-1])
        return Relation(rep)


    # Cases =====================================================================
    def visitCases_env(self, ctx: parse.Cases_envContext):
        return self.visit(ctx.cases_exp())

    def visitCases_last_row(self, ctx: parse.Cases_last_rowContext):
        return (self.visit(ctx.expr()), self.visit(ctx.relation()))

    def visitCases_row(self, ctx: parse.Cases_rowContext):
        return (self.visit(ctx.expr()), self.visit(ctx.relation()))

    def visitCases_exp(self, ctx:parse.Cases_expContext):
        return Cases(
            [self.visit(row) for row in ctx.cases_row()] +
            [self.visit(ctx.cases_last_row())]
        )

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
        parse.FUNC_LOG: math.log
    }

    rel_dict = {
        parse.LT: op.lt,
        parse.GT: op.gt,
        parse.LTE: op.le,
        parse.GTE: op.ge,
        parse.EQ: op.eq,
        parse.NEQ: op.ne
    }

def evaluate_expression(state: State, expr: str):
    stream = InputStream(expr)
    lexer = LaTeXLexer(stream)
    tokens = CommonTokenStream(lexer)
    parser = parse(tokens)
    tree = parser.entry()
    visitor = CastleVisitor(state)
    print(visitor.visit(tree))


def main(argv):
    state = State()
    FILEPATH = 'lang/input.txt'
    for line in open(FILEPATH, 'r').readlines():
        evaluate_expression(state, line)

if __name__ == '__main__':
    main(sys.argv)