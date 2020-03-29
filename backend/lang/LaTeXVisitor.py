# Generated from LaTeX.g4 by ANTLR 4.8
from antlr4 import *
from backend.lang.LaTeXParser import LaTeXParser

# This class defines a complete generic visitor for a parse tree produced by LaTeXParser.


class LaTeXVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LaTeXParser#hist_index.
    def visitHist_index(self, ctx: LaTeXParser.Hist_indexContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#hist_ans.
    def visitHist_ans(self, ctx: LaTeXParser.Hist_ansContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#number.
    def visitNumber(self, ctx: LaTeXParser.NumberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#nnint.
    def visitNnint(self, ctx: LaTeXParser.NnintContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#multichar_var.
    def visitMultichar_var(self, ctx: LaTeXParser.Multichar_varContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#var_name_letter.
    def visitVar_name_letter(self, ctx: LaTeXParser.Var_name_letterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#var_name_multichar.
    def visitVar_name_multichar(self, ctx: LaTeXParser.Var_name_multicharContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#var.
    def visitVar(self, ctx: LaTeXParser.VarContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#tex_symb_single.
    def visitTex_symb_single(self, ctx: LaTeXParser.Tex_symb_singleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#tex_symb_multi.
    def visitTex_symb_multi(self, ctx: LaTeXParser.Tex_symb_multiContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#tex_symb_recurse.
    def visitTex_symb_recurse(self, ctx: LaTeXParser.Tex_symb_recurseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_name_builtin.
    def visitFunc_name_builtin(self, ctx: LaTeXParser.Func_name_builtinContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_name_var.
    def visitFunc_name_var(self, ctx: LaTeXParser.Func_name_varContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_builtin.
    def visitFunc_builtin(self, ctx: LaTeXParser.Func_builtinContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_call_var.
    def visitFunc_call_var(self, ctx: LaTeXParser.Func_call_varContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_sum.
    def visitFunc_sum(self, ctx: LaTeXParser.Func_sumContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_prod.
    def visitFunc_prod(self, ctx: LaTeXParser.Func_prodContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_lim.
    def visitFunc_lim(self, ctx: LaTeXParser.Func_limContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_int.
    def visitFunc_int(self, ctx: LaTeXParser.Func_intContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_floorceil.
    def visitFunc_floorceil(self, ctx: LaTeXParser.Func_floorceilContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_deriv.
    def visitFunc_deriv(self, ctx: LaTeXParser.Func_derivContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#entry.
    def visitEntry(self, ctx: LaTeXParser.EntryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#castle_input_expr.
    def visitCastle_input_expr(self, ctx: LaTeXParser.Castle_input_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#castle_input_relation.
    def visitCastle_input_relation(self, ctx: LaTeXParser.Castle_input_relationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#castle_input_assignment.
    def visitCastle_input_assignment(
        self, ctx: LaTeXParser.Castle_input_assignmentContext
    ):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#relation.
    def visitRelation(self, ctx: LaTeXParser.RelationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#relop.
    def visitRelop(self, ctx: LaTeXParser.RelopContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#expr.
    def visitExpr(self, ctx: LaTeXParser.ExprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#add_expr_mult.
    def visitAdd_expr_mult(self, ctx: LaTeXParser.Add_expr_multContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#add_expr_recurse.
    def visitAdd_expr_recurse(self, ctx: LaTeXParser.Add_expr_recurseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#mult_expr_pow.
    def visitMult_expr_pow(self, ctx: LaTeXParser.Mult_expr_powContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#mult_expr_recurse.
    def visitMult_expr_recurse(self, ctx: LaTeXParser.Mult_expr_recurseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#pow_expr_recurse.
    def visitPow_expr_recurse(self, ctx: LaTeXParser.Pow_expr_recurseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#pow_expr_unit.
    def visitPow_expr_unit(self, ctx: LaTeXParser.Pow_expr_unitContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_recurse.
    def visitUnit_recurse(self, ctx: LaTeXParser.Unit_recurseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_paren.
    def visitUnit_paren(self, ctx: LaTeXParser.Unit_parenContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_func.
    def visitUnit_func(self, ctx: LaTeXParser.Unit_funcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_var.
    def visitUnit_var(self, ctx: LaTeXParser.Unit_varContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_number.
    def visitUnit_number(self, ctx: LaTeXParser.Unit_numberContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_infinity.
    def visitUnit_infinity(self, ctx: LaTeXParser.Unit_infinityContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_fraction.
    def visitUnit_fraction(self, ctx: LaTeXParser.Unit_fractionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_matrix.
    def visitUnit_matrix(self, ctx: LaTeXParser.Unit_matrixContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_cases.
    def visitUnit_cases(self, ctx: LaTeXParser.Unit_casesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#unit_hist.
    def visitUnit_hist(self, ctx: LaTeXParser.Unit_histContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#var_def.
    def visitVar_def(self, ctx: LaTeXParser.Var_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#arg_list.
    def visitArg_list(self, ctx: LaTeXParser.Arg_listContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_def.
    def visitFunc_def(self, ctx: LaTeXParser.Func_defContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#var_assign.
    def visitVar_assign(self, ctx: LaTeXParser.Var_assignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#func_assign.
    def visitFunc_assign(self, ctx: LaTeXParser.Func_assignContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#fraction.
    def visitFraction(self, ctx: LaTeXParser.FractionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#cases_last_row.
    def visitCases_last_row(self, ctx: LaTeXParser.Cases_last_rowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#cases_row.
    def visitCases_row(self, ctx: LaTeXParser.Cases_rowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#cases_exp.
    def visitCases_exp(self, ctx: LaTeXParser.Cases_expContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#cases_env.
    def visitCases_env(self, ctx: LaTeXParser.Cases_envContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#matrix_last_row.
    def visitMatrix_last_row(self, ctx: LaTeXParser.Matrix_last_rowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#matrix_row.
    def visitMatrix_row(self, ctx: LaTeXParser.Matrix_rowContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#matrix_exp.
    def visitMatrix_exp(self, ctx: LaTeXParser.Matrix_expContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by LaTeXParser#matrix_env.
    def visitMatrix_env(self, ctx: LaTeXParser.Matrix_envContext):
        return self.visitChildren(ctx)


del LaTeXParser
