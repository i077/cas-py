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
LBRACE  : '{';
RBRACE  : '}';
LBRACK  : '[';
RBRACK  : ']';

PLUS    : '+';
MINUS   : '-';
MULT    : '*';
DIV     : '/';
CARET   : '^';

POINT   : '.';

EQUAL   : '=';
ASSIGN  : ':=';

fragment LETTER  : [a-zA-Z];
fragment DIGIT   : [0-9];

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

start
    : SYMBOL
    | NUMBER
    ;
