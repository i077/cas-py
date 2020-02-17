grammar LaTeX;

options {
    language=Python3;
}

WS
    : [ \r\n\t]+ -> channel (HIDDEN)
    ;

// Literal tokens

BS      : '\\';

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

fragment LETTER  : [a-zA-Z];
fragment DIGIT   : [0-9];

CMD_CDOT        : '\\cdot';
CMD_TIMES       : '\\times';
CMD_DIV         : '\\div';
CMD_FRAC        : '\\frac';
CMD_BEGIN       : '\\begin';
CMD_END         : '\\end';

FUNC_LIM        : '\\lim';
FUNC_INT        : '\\int';

FUNC_LOG        : '\\log';
FUNC_LN         : '\\ln';
FUNC_EXP        : '\\exp';
FUNC_SIN        : '\\sin';
FUNC_COS        : '\\cos';
FUNC_TAN        : '\\tan';
FUNC_SEC        : '\\sec';

// Compound literals

NUMBER  : MINUS? DIGIT+ (POINT DIGIT*)?;

SYMBOL  : BS [a-zA-Z]+;

// Rules

start: relation;

relation
    : relation (EQ | LT | LTE | GT | GTE) relation
    | expr
    ;

expr: add_expr;

add_expr
    : add_expr (PLUS | MINUS) add_expr
    | mult_expr
    ;

mult_expr
    : mult_expr (MULT | CMD_TIMES | CMD_CDOT | DIV | CMD_DIV) mult_expr
    | unit
    ;

unit
    : (PLUS | MINUS) unit
    | pow_expr
    | fraction
    ;

pow_expr
    : pow_expr CARET (NUMBER | LCURLY expr RCURLY)
    | NUMBER
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