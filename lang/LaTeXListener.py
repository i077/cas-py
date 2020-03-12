# Generated from LaTeX.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .LaTeXParser import LaTeXParser
else:
    from LaTeXParser import LaTeXParser

# This class defines a complete listener for a parse tree produced by LaTeXParser.
class LaTeXListener(ParseTreeListener):

    # Enter a parse tree produced by LaTeXParser#hist_index.
    def enterHist_index(self, ctx:LaTeXParser.Hist_indexContext):
        pass

    # Exit a parse tree produced by LaTeXParser#hist_index.
    def exitHist_index(self, ctx:LaTeXParser.Hist_indexContext):
        pass


    # Enter a parse tree produced by LaTeXParser#hist_ans.
    def enterHist_ans(self, ctx:LaTeXParser.Hist_ansContext):
        pass

    # Exit a parse tree produced by LaTeXParser#hist_ans.
    def exitHist_ans(self, ctx:LaTeXParser.Hist_ansContext):
        pass


    # Enter a parse tree produced by LaTeXParser#number.
    def enterNumber(self, ctx:LaTeXParser.NumberContext):
        pass

    # Exit a parse tree produced by LaTeXParser#number.
    def exitNumber(self, ctx:LaTeXParser.NumberContext):
        pass


    # Enter a parse tree produced by LaTeXParser#nnint.
    def enterNnint(self, ctx:LaTeXParser.NnintContext):
        pass

    # Exit a parse tree produced by LaTeXParser#nnint.
    def exitNnint(self, ctx:LaTeXParser.NnintContext):
        pass


    # Enter a parse tree produced by LaTeXParser#multichar_var.
    def enterMultichar_var(self, ctx:LaTeXParser.Multichar_varContext):
        pass

    # Exit a parse tree produced by LaTeXParser#multichar_var.
    def exitMultichar_var(self, ctx:LaTeXParser.Multichar_varContext):
        pass


    # Enter a parse tree produced by LaTeXParser#var_name_letter.
    def enterVar_name_letter(self, ctx:LaTeXParser.Var_name_letterContext):
        pass

    # Exit a parse tree produced by LaTeXParser#var_name_letter.
    def exitVar_name_letter(self, ctx:LaTeXParser.Var_name_letterContext):
        pass


    # Enter a parse tree produced by LaTeXParser#var_name_multichar.
    def enterVar_name_multichar(self, ctx:LaTeXParser.Var_name_multicharContext):
        pass

    # Exit a parse tree produced by LaTeXParser#var_name_multichar.
    def exitVar_name_multichar(self, ctx:LaTeXParser.Var_name_multicharContext):
        pass


    # Enter a parse tree produced by LaTeXParser#var.
    def enterVar(self, ctx:LaTeXParser.VarContext):
        pass

    # Exit a parse tree produced by LaTeXParser#var.
    def exitVar(self, ctx:LaTeXParser.VarContext):
        pass


    # Enter a parse tree produced by LaTeXParser#tex_symb_single.
    def enterTex_symb_single(self, ctx:LaTeXParser.Tex_symb_singleContext):
        pass

    # Exit a parse tree produced by LaTeXParser#tex_symb_single.
    def exitTex_symb_single(self, ctx:LaTeXParser.Tex_symb_singleContext):
        pass


    # Enter a parse tree produced by LaTeXParser#tex_symb_multi.
    def enterTex_symb_multi(self, ctx:LaTeXParser.Tex_symb_multiContext):
        pass

    # Exit a parse tree produced by LaTeXParser#tex_symb_multi.
    def exitTex_symb_multi(self, ctx:LaTeXParser.Tex_symb_multiContext):
        pass


    # Enter a parse tree produced by LaTeXParser#tex_symb_recurse.
    def enterTex_symb_recurse(self, ctx:LaTeXParser.Tex_symb_recurseContext):
        pass

    # Exit a parse tree produced by LaTeXParser#tex_symb_recurse.
    def exitTex_symb_recurse(self, ctx:LaTeXParser.Tex_symb_recurseContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_name_builtin.
    def enterFunc_name_builtin(self, ctx:LaTeXParser.Func_name_builtinContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_name_builtin.
    def exitFunc_name_builtin(self, ctx:LaTeXParser.Func_name_builtinContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_name_var.
    def enterFunc_name_var(self, ctx:LaTeXParser.Func_name_varContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_name_var.
    def exitFunc_name_var(self, ctx:LaTeXParser.Func_name_varContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_builtin.
    def enterFunc_builtin(self, ctx:LaTeXParser.Func_builtinContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_builtin.
    def exitFunc_builtin(self, ctx:LaTeXParser.Func_builtinContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_call_var.
    def enterFunc_call_var(self, ctx:LaTeXParser.Func_call_varContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_call_var.
    def exitFunc_call_var(self, ctx:LaTeXParser.Func_call_varContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_lim.
    def enterFunc_lim(self, ctx:LaTeXParser.Func_limContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_lim.
    def exitFunc_lim(self, ctx:LaTeXParser.Func_limContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_int.
    def enterFunc_int(self, ctx:LaTeXParser.Func_intContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_int.
    def exitFunc_int(self, ctx:LaTeXParser.Func_intContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_floorceil.
    def enterFunc_floorceil(self, ctx:LaTeXParser.Func_floorceilContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_floorceil.
    def exitFunc_floorceil(self, ctx:LaTeXParser.Func_floorceilContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_deriv.
    def enterFunc_deriv(self, ctx:LaTeXParser.Func_derivContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_deriv.
    def exitFunc_deriv(self, ctx:LaTeXParser.Func_derivContext):
        pass


    # Enter a parse tree produced by LaTeXParser#entry.
    def enterEntry(self, ctx:LaTeXParser.EntryContext):
        pass

    # Exit a parse tree produced by LaTeXParser#entry.
    def exitEntry(self, ctx:LaTeXParser.EntryContext):
        pass


    # Enter a parse tree produced by LaTeXParser#castle_input_expr.
    def enterCastle_input_expr(self, ctx:LaTeXParser.Castle_input_exprContext):
        pass

    # Exit a parse tree produced by LaTeXParser#castle_input_expr.
    def exitCastle_input_expr(self, ctx:LaTeXParser.Castle_input_exprContext):
        pass


    # Enter a parse tree produced by LaTeXParser#castle_input_relation.
    def enterCastle_input_relation(self, ctx:LaTeXParser.Castle_input_relationContext):
        pass

    # Exit a parse tree produced by LaTeXParser#castle_input_relation.
    def exitCastle_input_relation(self, ctx:LaTeXParser.Castle_input_relationContext):
        pass


    # Enter a parse tree produced by LaTeXParser#castle_input_assignment.
    def enterCastle_input_assignment(self, ctx:LaTeXParser.Castle_input_assignmentContext):
        pass

    # Exit a parse tree produced by LaTeXParser#castle_input_assignment.
    def exitCastle_input_assignment(self, ctx:LaTeXParser.Castle_input_assignmentContext):
        pass


    # Enter a parse tree produced by LaTeXParser#relation.
    def enterRelation(self, ctx:LaTeXParser.RelationContext):
        pass

    # Exit a parse tree produced by LaTeXParser#relation.
    def exitRelation(self, ctx:LaTeXParser.RelationContext):
        pass


    # Enter a parse tree produced by LaTeXParser#relop.
    def enterRelop(self, ctx:LaTeXParser.RelopContext):
        pass

    # Exit a parse tree produced by LaTeXParser#relop.
    def exitRelop(self, ctx:LaTeXParser.RelopContext):
        pass


    # Enter a parse tree produced by LaTeXParser#expr.
    def enterExpr(self, ctx:LaTeXParser.ExprContext):
        pass

    # Exit a parse tree produced by LaTeXParser#expr.
    def exitExpr(self, ctx:LaTeXParser.ExprContext):
        pass


    # Enter a parse tree produced by LaTeXParser#add_expr_mult.
    def enterAdd_expr_mult(self, ctx:LaTeXParser.Add_expr_multContext):
        pass

    # Exit a parse tree produced by LaTeXParser#add_expr_mult.
    def exitAdd_expr_mult(self, ctx:LaTeXParser.Add_expr_multContext):
        pass


    # Enter a parse tree produced by LaTeXParser#add_expr_recurse.
    def enterAdd_expr_recurse(self, ctx:LaTeXParser.Add_expr_recurseContext):
        pass

    # Exit a parse tree produced by LaTeXParser#add_expr_recurse.
    def exitAdd_expr_recurse(self, ctx:LaTeXParser.Add_expr_recurseContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mult_expr_pow.
    def enterMult_expr_pow(self, ctx:LaTeXParser.Mult_expr_powContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mult_expr_pow.
    def exitMult_expr_pow(self, ctx:LaTeXParser.Mult_expr_powContext):
        pass


    # Enter a parse tree produced by LaTeXParser#mult_expr_recurse.
    def enterMult_expr_recurse(self, ctx:LaTeXParser.Mult_expr_recurseContext):
        pass

    # Exit a parse tree produced by LaTeXParser#mult_expr_recurse.
    def exitMult_expr_recurse(self, ctx:LaTeXParser.Mult_expr_recurseContext):
        pass


    # Enter a parse tree produced by LaTeXParser#pow_expr_recurse.
    def enterPow_expr_recurse(self, ctx:LaTeXParser.Pow_expr_recurseContext):
        pass

    # Exit a parse tree produced by LaTeXParser#pow_expr_recurse.
    def exitPow_expr_recurse(self, ctx:LaTeXParser.Pow_expr_recurseContext):
        pass


    # Enter a parse tree produced by LaTeXParser#pow_expr_unit.
    def enterPow_expr_unit(self, ctx:LaTeXParser.Pow_expr_unitContext):
        pass

    # Exit a parse tree produced by LaTeXParser#pow_expr_unit.
    def exitPow_expr_unit(self, ctx:LaTeXParser.Pow_expr_unitContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_recurse.
    def enterUnit_recurse(self, ctx:LaTeXParser.Unit_recurseContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_recurse.
    def exitUnit_recurse(self, ctx:LaTeXParser.Unit_recurseContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_paren.
    def enterUnit_paren(self, ctx:LaTeXParser.Unit_parenContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_paren.
    def exitUnit_paren(self, ctx:LaTeXParser.Unit_parenContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_func.
    def enterUnit_func(self, ctx:LaTeXParser.Unit_funcContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_func.
    def exitUnit_func(self, ctx:LaTeXParser.Unit_funcContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_var.
    def enterUnit_var(self, ctx:LaTeXParser.Unit_varContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_var.
    def exitUnit_var(self, ctx:LaTeXParser.Unit_varContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_number.
    def enterUnit_number(self, ctx:LaTeXParser.Unit_numberContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_number.
    def exitUnit_number(self, ctx:LaTeXParser.Unit_numberContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_fraction.
    def enterUnit_fraction(self, ctx:LaTeXParser.Unit_fractionContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_fraction.
    def exitUnit_fraction(self, ctx:LaTeXParser.Unit_fractionContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_matrix.
    def enterUnit_matrix(self, ctx:LaTeXParser.Unit_matrixContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_matrix.
    def exitUnit_matrix(self, ctx:LaTeXParser.Unit_matrixContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_cases.
    def enterUnit_cases(self, ctx:LaTeXParser.Unit_casesContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_cases.
    def exitUnit_cases(self, ctx:LaTeXParser.Unit_casesContext):
        pass


    # Enter a parse tree produced by LaTeXParser#unit_hist.
    def enterUnit_hist(self, ctx:LaTeXParser.Unit_histContext):
        pass

    # Exit a parse tree produced by LaTeXParser#unit_hist.
    def exitUnit_hist(self, ctx:LaTeXParser.Unit_histContext):
        pass


    # Enter a parse tree produced by LaTeXParser#var_def.
    def enterVar_def(self, ctx:LaTeXParser.Var_defContext):
        pass

    # Exit a parse tree produced by LaTeXParser#var_def.
    def exitVar_def(self, ctx:LaTeXParser.Var_defContext):
        pass


    # Enter a parse tree produced by LaTeXParser#arg_list_single.
    def enterArg_list_single(self, ctx:LaTeXParser.Arg_list_singleContext):
        pass

    # Exit a parse tree produced by LaTeXParser#arg_list_single.
    def exitArg_list_single(self, ctx:LaTeXParser.Arg_list_singleContext):
        pass


    # Enter a parse tree produced by LaTeXParser#arg_list_multi.
    def enterArg_list_multi(self, ctx:LaTeXParser.Arg_list_multiContext):
        pass

    # Exit a parse tree produced by LaTeXParser#arg_list_multi.
    def exitArg_list_multi(self, ctx:LaTeXParser.Arg_list_multiContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_def.
    def enterFunc_def(self, ctx:LaTeXParser.Func_defContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_def.
    def exitFunc_def(self, ctx:LaTeXParser.Func_defContext):
        pass


    # Enter a parse tree produced by LaTeXParser#var_assign.
    def enterVar_assign(self, ctx:LaTeXParser.Var_assignContext):
        pass

    # Exit a parse tree produced by LaTeXParser#var_assign.
    def exitVar_assign(self, ctx:LaTeXParser.Var_assignContext):
        pass


    # Enter a parse tree produced by LaTeXParser#func_assign.
    def enterFunc_assign(self, ctx:LaTeXParser.Func_assignContext):
        pass

    # Exit a parse tree produced by LaTeXParser#func_assign.
    def exitFunc_assign(self, ctx:LaTeXParser.Func_assignContext):
        pass


    # Enter a parse tree produced by LaTeXParser#fraction.
    def enterFraction(self, ctx:LaTeXParser.FractionContext):
        pass

    # Exit a parse tree produced by LaTeXParser#fraction.
    def exitFraction(self, ctx:LaTeXParser.FractionContext):
        pass


    # Enter a parse tree produced by LaTeXParser#cases_last_row.
    def enterCases_last_row(self, ctx:LaTeXParser.Cases_last_rowContext):
        pass

    # Exit a parse tree produced by LaTeXParser#cases_last_row.
    def exitCases_last_row(self, ctx:LaTeXParser.Cases_last_rowContext):
        pass


    # Enter a parse tree produced by LaTeXParser#cases_row.
    def enterCases_row(self, ctx:LaTeXParser.Cases_rowContext):
        pass

    # Exit a parse tree produced by LaTeXParser#cases_row.
    def exitCases_row(self, ctx:LaTeXParser.Cases_rowContext):
        pass


    # Enter a parse tree produced by LaTeXParser#cases_exp.
    def enterCases_exp(self, ctx:LaTeXParser.Cases_expContext):
        pass

    # Exit a parse tree produced by LaTeXParser#cases_exp.
    def exitCases_exp(self, ctx:LaTeXParser.Cases_expContext):
        pass


    # Enter a parse tree produced by LaTeXParser#cases_env.
    def enterCases_env(self, ctx:LaTeXParser.Cases_envContext):
        pass

    # Exit a parse tree produced by LaTeXParser#cases_env.
    def exitCases_env(self, ctx:LaTeXParser.Cases_envContext):
        pass


    # Enter a parse tree produced by LaTeXParser#matrix_last_row.
    def enterMatrix_last_row(self, ctx:LaTeXParser.Matrix_last_rowContext):
        pass

    # Exit a parse tree produced by LaTeXParser#matrix_last_row.
    def exitMatrix_last_row(self, ctx:LaTeXParser.Matrix_last_rowContext):
        pass


    # Enter a parse tree produced by LaTeXParser#matrix_row.
    def enterMatrix_row(self, ctx:LaTeXParser.Matrix_rowContext):
        pass

    # Exit a parse tree produced by LaTeXParser#matrix_row.
    def exitMatrix_row(self, ctx:LaTeXParser.Matrix_rowContext):
        pass


    # Enter a parse tree produced by LaTeXParser#matrix_exp.
    def enterMatrix_exp(self, ctx:LaTeXParser.Matrix_expContext):
        pass

    # Exit a parse tree produced by LaTeXParser#matrix_exp.
    def exitMatrix_exp(self, ctx:LaTeXParser.Matrix_expContext):
        pass


    # Enter a parse tree produced by LaTeXParser#matrix_env.
    def enterMatrix_env(self, ctx:LaTeXParser.Matrix_envContext):
        pass

    # Exit a parse tree produced by LaTeXParser#matrix_env.
    def exitMatrix_env(self, ctx:LaTeXParser.Matrix_envContext):
        pass



del LaTeXParser