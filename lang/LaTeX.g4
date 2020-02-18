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
LT      : '<';
LTE     : '\\leq';
GT      : '>';
GTE     : '\\geq';
ASSIGN  : ':=';

MATRIX  : 'matrix';
P_MATRIX: 'pmatrix';
B_MATRIX: 'bmatrix';
V_MATRIX: 'vmatrix';

UNDERSCORE : '_';
COMMA      : ',';

LETTER  : [a-zA-Z];
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

FUNC_LOG        : '\\log';
FUNC_LN         : '\\ln';
FUNC_EXP        : '\\exp';
FUNC_SIN        : '\\sin';
FUNC_COS        : '\\cos';
FUNC_TAN        : '\\tan';
FUNC_SEC        : '\\sec';
FUNC_CSC        : '\\csc';
FUNC_COT        : '\\cot';

CMD_LFLOOR      : '\\lfloor';
CMD_RFLOOR      : '\\rfloor';
CMD_LCEIL       : '\\lceil';

// Compound literals

number  : MINUS? DIGIT+ (POINT DIGIT*)?;

multichar_var : (LETTER | DIGIT)+;

// Variable names
var_name
    : LETTER
    | BACKTICK name=multichar_var BACKTICK
    ;

var
    : var_name (UNDERSCORE tex_symb)?;
tex_symb
    : (LETTER | DIGIT)
    | LCURLY expr RCURLY
    ;

// Function names can either be builtin LaTeX commands or var names
func_name
    : func_builtin
    | var
    ;

func_builtin
    : FUNC_SIN | FUNC_COS | FUNC_TAN
    | FUNC_SEC | FUNC_CSC | FUNC_COT
    | FUNC_EXP | FUNC_LN | FUNC_LOG
    ;

func
    // Function calls with normal syntax
    : func_name LPAREN (expr ((COMMA expr)+)*) RPAREN
    // Limits
    | FUNC_LIM UNDERSCORE LCURLY limitvar=var (CMD_TO | CMD_RIGHTARROW) limitto=expr RCURLY LCURLY expr RCURLY
    // Integrals
    | FUNC_INT (UNDERSCORE tex_symb CARET tex_symb)? LCURLY expr CMD_DD var RCURLY
    // Floor/ceilings
    ;

// Rules

start
    : relation EOF
    ;

relation
    : relation relop=(EQ | LT | LTE | GT | GTE) relation
    | expr
    ;

expr: add_expr;

add_expr
    : add_expr op=(PLUS | MINUS) add_expr
    | mult_expr
    ;

mult_expr
    : mult_expr op=(MULT | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV) mult_expr
    | pow_expr
    ;

pow_expr
    : pow_expr CARET tex_symb
    | unit
    ;

unit
    : sign=(PLUS | MINUS) unit      // Signed unit expressions
    | MINUS? LPAREN expr RPAREN     // Parentheticals, optionally signed
    | func                          // Function calls
    | var                           // Variable identifiers
    | number                        // Number literals
    | fraction                      // Fraction expressions
    | matrix_env                    // Matrices
    ;

fraction
    : CMD_FRAC LCURLY expr RCURLY LCURLY expr RCURLY
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
