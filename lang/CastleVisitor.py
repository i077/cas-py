import sys
from antlr4 import FileStream, InputStream, Lexer, Parser, CommonTokenStream
from LaTeXVisitor import LaTeXVisitor
from LaTeXParser import LaTeXParser as parse
from LaTeXLexer import LaTeXLexer

class CastleVisitor(LaTeXVisitor):
    def CastleVisitor(self, state: dict):
        self.state = state

    def visitAdd_expr_recurse(self, ctx:parse.Add_expr_recurseContext):
        if ctx.op.type == parse.PLUS:
            return self.visit(ctx.add_expr(0)) + self.visit(ctx.add_expr(1))
        else:
            return self.visit(ctx.add_expr(0)) - self.visit(ctx.add_expr(1))

    def visitMult_expr_recurse(self, ctx:parse.Mult_expr_recurseContext):
        if ctx.op.type in {parse.DIV, parse.CMD_DIV}:
            return self.visit(ctx.mult_expr(0)) // self.visit(ctx.mult_exp)
        else:
            return self.visit(ctx.mult_expr(0)) * self.visit(ctx.mult_expr(1))

    def visitPow_expr_recurse(self, ctx:parse.Pow_expr_recurseContext):
        return self.visit(ctx.pow_expr) ** self.visit(ctx.tex_symb)

    def visitUnit_recurse(self, ctx:parse.Unit_recurseContext):
        if ctx.sign.type == parse.MINUS:
            return -1*self.visit(ctx.unit)
        else:
            return self.visit(ctx.unit)

    def visitUnit_paren(self, ctx:parse.Unit_parenContext):
        return (-1 if ctx.MINUS() else 1) * self.visit(ctx.expr)

    def visitNumber(self, ctx:parse.NumberContext):
        return float(ctx.getText())

    def visitEntry(self, ctx:parse.EntryContext):
        return self.visit(ctx.castle_input())


def main(argv):
    stream = InputStream('5+6')
    lexer = LaTeXLexer(stream)
    tokens = CommonTokenStream(lexer)
    print(tokens.getText())
    parser = parse(tokens)
    tree = parser.entry()

    visitor = CastleVisitor()
    print(visitor.visit(tree))

if __name__ == '__main__':
    main(sys.argv)