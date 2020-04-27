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
I  : 'i';

NON_EI_LETTER  : [a-df-hj-zA-Z];
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

FUNC_RREF       : '\\rref';
FUNC_GCD        : '\\gcd';
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

multichar_var : (NON_EI_LETTER | E | I | DIGIT)+;

// Variable names
var_name
    : NON_EI_LETTER                               #var_name_letter
    | BACKTICK name=multichar_var BACKTICK #var_name_multichar
    ;

var
    : var_name (UNDERSCORE tex_symb)?;

tex_symb
    : (NON_EI_LETTER | E | I | DIGIT)   #tex_symb_single
    | LCURLY expr RCURLY #tex_symb_multi
    | LCURLY var RCURLY  #tex_symb_recurse
    ;

func_builtin
    : name=(FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_SEC | FUNC_CSC | FUNC_COT
    | FUNC_EXP | FUNC_LN | FUNC_GCD
    | FUNC_RREF | FUNC_LOG
    | FUNC_ASIN | FUNC_ACOS | FUNC_ATAN
    | FUNC_ASEC | FUNC_ACSC | FUNC_ACOT)
    ;

func_call
    // Custom function call with a number of arguments other than 1
    : var LPAREN (expr (COMMA expr)+)? RPAREN                                                                  #func_custom
    // Function builtin function call
    | func_builtin (LPAREN (expr ((COMMA expr)+)*)? RPAREN |
                    LCURLY LPAREN (expr ((COMMA expr)+)*)? RPAREN RCURLY |
                    LCURLY (expr ((COMMA expr)+)*)? RCURLY)                                                    #func_call_builtin
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
    | implicit_mult_expr                                                   #mult_implicit
    | sign=(PLUS | MINUS) mult_expr                                        #mult_sign
    | pow_expr                                                             #mult_expr_pow
    ;

implicit_mult_expr
    : implicit_mult_expr implicit_mult_expr                   #ime_mult
    | left_implicit_pow_expr (implicit_mult_expr)?            #ime_left
    | implicit_pow_expr                                       #ime_pow
    | var_parens                                              #ime_var_parens
    //basically everything that isn't 'var unit_paren' because we want that to be only handled by var_parens
    | (var_pow_expr | paren_pow_expr) implicit_mult_expr      #ime_var_unit_paren_left
    | implicit_mult_expr (var_pow_expr | paren_pow_expr)      #ime_var_unit_paren_right
    | paren_pow_expr var_pow_expr                             #ime_paren_var
    | var_pow_expr var_pow_expr                               #ime_var_var
    | paren_pow_expr paren_pow_expr                           #ime_paren_paren
    ;

var_pow_expr
    : var (CARET tex_symb)?
    ;

paren_pow_expr
    : unit_paren (CARET tex_symb)?
    ;

implicit_pow_expr
    : implicit_pow_expr CARET tex_symb  #implicit_pow_expr_recurse
    | implicit_mult_unit                #implicit_pow_expr_unit
    ;

left_implicit_pow_expr
    : left_implicit_pow_expr CARET tex_symb  #left_implicit_pow_expr_recurse
    | left_implicit_mult_unit                #left_implicit_pow_expr_unit
    ;

pow_expr
    : pow_expr CARET tex_symb #pow_expr_recurse
    | unit                    #pow_expr_unit
    ;

// this structure (for example y(x+1)) is completely ambiguous between a multiplication
// and a function call. So we need to use state context to figure out what it is
// we also have to consider exponentiation here because y(x+1)^z is interpreted
// as (y(x+1))^z if y is a function and y((x+1)^z) if y is a number
var_parens
    : var LPAREN expr RPAREN (CARET tex_symb)?
    ;

unit
    : inf=(INFINITY | NEG_INFINITY) #unit_infinity     // Infinity
    | implicit_mult_unit            #unit_implicit
    | left_implicit_mult_unit       #unit_left_implicit
    //these two are really implicit_mult_units but they need to be
    //considered separately because of the var_parens ambiguity
    | var                           #unit_var          // Variable identifiers
    | unit_paren                    #unit_unit_paren
    ;

unit_paren
    : LPAREN expr RPAREN
    ;

//units that can be multiplied together without * or \cdot on both sides:
//for example x\sqrt{x}
implicit_mult_unit
    : func_call                     #unit_func         // Function calls
    | fraction                      #unit_fraction     // Fraction expressions
    | matrix_env                    #unit_matrix       // Matrices
    | cases_env                     #unit_cases        // Branching (cases)
    | hist_entry                    #unit_hist         // History reference
    | PI                            #unit_pi           // 3.14159...
    | E                             #unit_e            // 2.71828...
    | I                             #unit_i            // \sqrt{-1}
    ;

//units that can only be explicitly multiplied on the left
left_implicit_mult_unit
    : number                        #unit_number       // Number literals
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
