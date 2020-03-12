import sys
from antlr4 import FileStream, InputStream, CommonTokenStream
from LaTeXVisitor import LaTeXVisitor
from LaTeXParser import LaTeXParser as parse
from LaTeXLexer import LaTeXLexer
from structures import Number, Polynomial, Variable, Expression, Cases, Relation
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


    # def visitFraction(self, ctx:parse.FractionContext):
    #     return Fraction(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

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
        self.state.set(self.visit(ctx.var_def()), expr)
        return expr

    def visitFunc_assign(self, ctx: parse.Func_assignContext):
        """func_assign
        assign_var ASSIGN func_def 
        assign a value to a function in the state"""
        func_def = self.visit(ctx.func_def())
        self.state.set(self.visit(ctx.var_def()), func_def)
        return func_def

    # Function definitions ======================================================

    # Relations =================================================================
    def visitRelop(self, ctx:parse.RelopContext):
        return ctx.op.type

    def visitRelation(self, ctx: parse.RelationContext):
        rep = []
        rel_dict = {
            parse.LT: op.lt,
            parse.GT: op.gt,
            parse.LTE: op.le,
            parse.GTE: op.ge,
            parse.EQ: op.eq,
            parse.NEQ: op.ne
        }
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

    def visitCases_exp(self, ctx:parse.Cases_expContext):
        return Cases(
            [self.visit(row) for row in ctx.cases_row()] +
            [self.visit(ctx.cases_last_row())]
        )


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