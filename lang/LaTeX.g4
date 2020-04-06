grammar LaTeX;

options {
    language=Python3;
}

WS
    : [ \r\n\t]+ -> channel (HIDDEN)
    ;

// Literal tokens

BS      : '\\';

BACKTICK: '`';

LPAREN  : '(';
RPAREN  : ')';
LCURLY  : '{';
RCURLY  : '}';
LBRACK  : '[';
RBRACK  : ']';

PLUS        : '+';
MINUS       : '-';
MULT        : '*';
DIV         : '/';
CARET       : '^';
AMPERSAND   : '&';

POINT   : '.';

EQ      : '=';
NEQ     : '\\neq';
LT      : '<' | '\\lt';
LTE     : '\\leq';
GT      : '>' | '\\gt';
GTE     : '\\geq';
ASSIGN  : ':=';

CASES   : 'cases';
MATRIX  : 'matrix';
P_MATRIX: 'pmatrix';
B_MATRIX: 'bmatrix';
V_MATRIX: 'vmatrix';

UNDERSCORE : '_';
COMMA      : ',';

PI : '\\pi';
E  : 'e';

NON_E_LETTER  : [a-df-zA-Z];
DIGIT   : [0-9];

CMD_CDOT        : '\\cdot';
CMD_TIMES       : '\\times';
CMD_DIV         : '\\div';
CMD_FRAC        : '\\frac';
CMD_BEGIN       : '\\begin';
CMD_END         : '\\end';
CMD_TO          : '\\to';
CMD_RIGHTARROW  : '\\rightarrow';
CMD_DD          : '\\dd';

FUNC_LIM        : '\\lim';
FUNC_INT        : '\\int';
FUNC_SUM        : '\\sum';
FUNC_PROD       : '\\prod';
FUNC_DV         : '\\dv';
FUNC_PDV        : '\\pdv';
FUNC_SQRT       : '\\sqrt';
FUNC_CHOOSE     : '\\binom';

FUNC_LOG        : '\\log';
FUNC_LN         : '\\ln';
FUNC_EXP        : '\\exp';
FUNC_SIN        : '\\sin';
FUNC_COS        : '\\cos';
FUNC_TAN        : '\\tan';
FUNC_SEC        : '\\sec';
FUNC_CSC        : '\\csc';
FUNC_COT        : '\\cot';
FUNC_ASIN       : '\\arcsin' | '\\asin' | '\\sin^{-1}';
FUNC_ACOS       : '\\arccos' | '\\acos' | '\\cos^{-1}';
FUNC_ATAN       : '\\arctan' | '\\atan' | '\\tan^{-1}';
FUNC_ASEC       : '\\arcsec' | '\\asec' | '\\sec^{-1}';
FUNC_ACSC       : '\\arccsc' | '\\acsc' | '\\csc^{-1}';
FUNC_ACOT       : '\\arccot' | '\\acot' | '\\cot^{-1}';

CMD_LFLOOR      : '\\lfloor';
CMD_RFLOOR      : '\\rfloor';
CMD_LCEIL       : '\\lceil';
CMD_RCEIL       : '\\rceil';

INFINITY        : '\\infty';
NEG_INFINITY    : '-\\infty';

// History tokens
DOLLAR          : '$';
hist_entry
    : DOLLAR nnint  #hist_index
    | DOLLAR 'ans'  #hist_ans
    ;

// Compound literals

number  : MINUS? DIGIT+ (POINT DIGIT*)?;
nnint   : DIGIT+;

multichar_var : (NON_E_LETTER | E | DIGIT)+;

// Variable names
var_name
    : NON_E_LETTER                               #var_name_letter
    | BACKTICK name=multichar_var BACKTICK #var_name_multichar
    ;

var
    : var_name (UNDERSCORE tex_symb)?;

tex_symb
    : (NON_E_LETTER | E | DIGIT)   #tex_symb_single
    | LCURLY expr RCURLY #tex_symb_multi
    | LCURLY var RCURLY  #tex_symb_recurse
    ;

// Function names can either be builtin LaTeX commands or var names
func_name
    : func_builtin #func_name_builtin
    | var          #func_name_var
    ;

func_builtin
    : name=(FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_SEC | FUNC_CSC | FUNC_COT
    | FUNC_EXP | FUNC_LN | FUNC_LOG
    | FUNC_ASIN | FUNC_ACOS | FUNC_ATAN
    | FUNC_ASEC | FUNC_ACSC | FUNC_ACOT)
    ;

func_call
    // Function calls with normal syntax
    : func_name (LPAREN (expr ((COMMA expr)+)*)? RPAREN | 
                 LCURLY LPAREN (expr ((COMMA expr)+)*)? RPAREN RCURLY |
                 LCURLY (expr ((COMMA expr)+)*)? RCURLY) #func_call_var
    // Sums
    | FUNC_SUM UNDERSCORE (LCURLY relation RCURLY CARET tex_symb | CARET tex_symb LCURLY relation RCURLY)
                          (expr | LCURLY expr RCURLY)                                                          #func_sum
    // Products
    | FUNC_PROD UNDERSCORE (LCURLY relation RCURLY CARET tex_symb | CARET tex_symb LCURLY relation RCURLY)
                           (expr | LCURLY expr RCURLY)                                                         #func_prod
    // Limits
    | FUNC_LIM UNDERSCORE LCURLY var (CMD_TO | CMD_RIGHTARROW) expr RCURLY LCURLY expr RCURLY                  #func_lim
    // Integrals
    | FUNC_INT (UNDERSCORE tex_symb CARET tex_symb)? LCURLY expr CMD_DD var RCURLY                             #func_int
    // Floor/ceilings
    | lop=(CMD_LFLOOR | CMD_LCEIL) expr rop=(CMD_RFLOOR | CMD_RCEIL)                                           #func_floorceil
    // (Partial) derivatives
    | op=(FUNC_DV | FUNC_PDV) (LBRACK nnint RBRACK)? LCURLY expr RCURLY LCURLY var RCURLY                      #func_deriv
    // n-th rootssqrt
    | FUNC_SQRT (LBRACK expr RBRACK)? LCURLY expr RCURLY                                                       #func_root
    // choose function
    | FUNC_CHOOSE LCURLY expr RCURLY LCURLY expr RCURLY                                                        #func_choose
    ;

// Rules
entry: castle_input EOF;

castle_input
    : expr       #castle_input_expr
    | relation   #castle_input_relation
    | assignment #castle_input_assignment
    ;

relation
    : (expr relop)+ expr
    ;

relop: op=(EQ | NEQ | LT | LTE | GT | GTE);

expr: add_expr;

add_expr
    : add_expr op=(PLUS | MINUS) add_expr #add_expr_recurse
    | mult_expr                           #add_expr_mult
    ;

mult_expr
    : mult_expr op=(MULT | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV) mult_expr #mult_expr_recurse
    | pow_expr                                                             #mult_expr_pow
    ;

pow_expr
    : pow_expr CARET tex_symb #pow_expr_recurse
    | unit                    #pow_expr_unit
    ;

unit
    : sign=(PLUS | MINUS) unit      #unit_recurse      // Signed unit expressions
    | MINUS? LPAREN expr RPAREN     #unit_paren        // Parentheticals, optionally signed
    | PI                            #unit_pi           // 3.14159...
    | E                             #unit_e            // 2.71828...
    | func_call                     #unit_func         // Function calls
    | var                           #unit_var          // Variable identifiers
    | number                        #unit_number       // Number literals
    | inf=(INFINITY | NEG_INFINITY) #unit_infinity     // Infinity
    | fraction                      #unit_fraction     // Fraction expressions
    | matrix_env                    #unit_matrix       // Matrices
    | cases_env                     #unit_cases        // Branching (cases)
    | hist_entry                    #unit_hist         // History reference
    ;

var_def
    : var_name (UNDERSCORE tex_symb)?;

arg_list
    : LPAREN (var_def (COMMA var_def)*)? RPAREN
    ;

func_def
    : arg_list (CMD_TO | CMD_RIGHTARROW) expr
    ;

assignment
    : var_def ASSIGN expr     #var_assign
    | var_def ASSIGN func_def #func_assign
    ;

fraction
    : CMD_FRAC LCURLY expr RCURLY LCURLY expr RCURLY
    ;

cases_last_row
    : expr AMPERSAND relation (BS BS)?
    ;

cases_row
    : expr AMPERSAND relation BS BS
    ;

cases_exp
    : cases_row* cases_last_row
    ;

cases_env
    : CMD_BEGIN LCURLY CASES RCURLY
      cases_exp
      CMD_END LCURLY CASES RCURLY
    ;

matrix_last_row
    : (expr AMPERSAND)* expr (BS BS)?
    ;

matrix_row
    : (expr AMPERSAND)* expr BS BS
    ;

matrix_exp
    : matrix_row* matrix_last_row
    ;

matrix_env
    : CMD_BEGIN LCURLY open_mat_type=(MATRIX | V_MATRIX | B_MATRIX | P_MATRIX) RCURLY
      matrix_exp
      CMD_END LCURLY close_mat_type=(MATRIX | V_MATRIX | B_MATRIX | P_MATRIX) RCURLY
    ;
