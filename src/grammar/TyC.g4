grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text);
    else:
        return super().emit();
}

options{
	language=Python3;
}

// ============================================================================
// PARSER RULES
// ============================================================================

// Program structure - allows empty programs
program : (structDecl | funcDecl)* EOF ;

// Struct declarations
structDecl : STRUCT IDENTIFIER LBRACE memberDecl* RBRACE SEMI ;

memberDecl : type IDENTIFIER SEMI ;

// Function declarations
funcDecl : returnType? IDENTIFIER LPAREN paramList? RPAREN blockStmt ;

returnType : type ;

paramList : param (COMMA param)* ;

param : type IDENTIFIER ;

// Types
type
    : INT
    | FLOAT
    | STRING
    | VOID
    | IDENTIFIER    // Struct type
    ;

// Statements
stmt
    : varDecl
    | blockStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | SEMI              // Empty statement
    ;

blockStmt : LBRACE stmt* RBRACE ;

varDecl
    : AUTO IDENTIFIER (ASSIGN expr)? SEMI
    | type IDENTIFIER (ASSIGN expr)? SEMI
    ;

ifStmt : IF LPAREN expr RPAREN stmt (ELSE stmt)? ;

whileStmt : WHILE LPAREN expr RPAREN stmt ;

forStmt : FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN stmt ;

forInit
    : AUTO IDENTIFIER (ASSIGN expr)?
    | type IDENTIFIER (ASSIGN expr)?
    | expr
    ;

forUpdate : expr ;

switchStmt : SWITCH LPAREN expr RPAREN LBRACE switchCase* RBRACE ;

switchCase
    : CASE expr COLON stmt*
    | DEFAULT COLON stmt*
    ;

breakStmt : BREAK SEMI ;

continueStmt : CONTINUE SEMI ;

returnStmt : RETURN expr? SEMI ;

exprStmt : expr SEMI ;

// Expressions with precedence (lowest to highest)

expr : assignExpr ;

// Level 11 (lowest): Assignment (right associative)
assignExpr : logicalOrExpr (ASSIGN assignExpr)? ;

// Level 10: Logical OR
logicalOrExpr : logicalAndExpr (OR logicalAndExpr)* ;

// Level 9: Logical AND
logicalAndExpr : equalityExpr (AND equalityExpr)* ;

// Level 8: Equality
equalityExpr : relationalExpr ((EQ | NE) relationalExpr)* ;

// Level 7: Relational
relationalExpr : additiveExpr ((LT | LE | GT | GE) additiveExpr)* ;

// Level 6: Additive
additiveExpr : multiplicativeExpr ((PLUS | MINUS) multiplicativeExpr)* ;

// Level 5: Multiplicative
multiplicativeExpr : unaryExpr ((STAR | DIV | MOD) unaryExpr)* ;

// Level 4: Unary prefix (right associative)
unaryExpr
    : (INC | DEC | NOT | MINUS | PLUS) unaryExpr
    | postfixExpr
    ;

// Level 2-3: Postfix and member access
postfixExpr : primaryExpr postfixSuffix* ;

postfixSuffix
    : INC
    | DEC
    | DOT IDENTIFIER
    | LPAREN argList? RPAREN
    ;

// Level 1 (highest): Primary expressions
primaryExpr
    : INTLIT
    | FLOATLIT
    | STRING_LIT
    | IDENTIFIER
    | LPAREN expr RPAREN
    | LBRACE argList? RBRACE    // Struct literal
    ;

argList : expr (COMMA expr)* ;

// ============================================================================
// LEXER RULES
// ============================================================================

// Keywords (must come before IDENTIFIER)
AUTO : 'auto' ;
BREAK : 'break' ;
CASE : 'case' ;
CONTINUE : 'continue' ;
DEFAULT : 'default' ;
ELSE : 'else' ;
FLOAT : 'float' ;
FOR : 'for' ;
IF : 'if' ;
INT : 'int' ;
RETURN : 'return' ;
STRING : 'string' ;
STRUCT : 'struct' ;
SWITCH : 'switch' ;
VOID : 'void' ;
WHILE : 'while' ;

// Two-character operators (must come before single-character)
LE : '<=' ;
GE : '>=' ;
EQ : '==' ;
NE : '!=' ;
AND : '&&' ;
OR : '||' ;
INC : '++' ;
DEC : '--' ;

// Single-character operators
PLUS : '+' ;
MINUS : '-' ;
STAR : '*' ;
DIV : '/' ;
MOD : '%' ;
LT : '<' ;
GT : '>' ;
NOT : '!' ;
ASSIGN : '=' ;
DOT : '.' ;

// Separators
LBRACE : '{' ;
RBRACE : '}' ;
LPAREN : '(' ;
RPAREN : ')' ;
LBRACK : '[' ;
RBRACK : ']' ;
SEMI : ';' ;
COMMA : ',' ;
COLON : ':' ;

// Float literals (must come before INTLIT to match properly)
FLOATLIT
    : MINUS? [0-9]+ '.' [0-9]* EXPONENT?     // 3.14, 1., 1.e5, -3.14
    | MINUS? '.' [0-9]+ EXPONENT?            // .5, .5e-2
    | MINUS? [0-9]+ EXPONENT                 // 1e4, 2E-3
    ;

fragment EXPONENT : [eE] [+-]? [0-9]+ ;

// Integer literals (spec allows negative: -45 is ONE token)
INTLIT : MINUS? [0-9]+ ;

// String literals and errors (errors must come before valid STRING_LIT)
ILLEGAL_ESCAPE : '"' STRING_CHAR* '\\' ~[bfrnt"\\] {self.text = self.text[1:]} ;

UNCLOSE_STRING : '"' STRING_CHAR* ([\r\n] | EOF) {self.text = self.text[1:]} ;

STRING_LIT : '"' STRING_CHAR* '"' {self.text = self.text[1:-1]} ;

fragment STRING_CHAR
    : ESC_SEQ
    | ~["\\\r\n]      // Any char except ", \, \r, \n
    ;

fragment ESC_SEQ : '\\' [bfrnt"\\] ;

// Identifiers (must come after keywords)
IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;

// Comments
BLOCK_COMMENT : '/*' .*? '*/' -> skip ;
LINE_COMMENT : '//' ~[\r\n]* -> skip ;

// Whitespace
WS : [ \t\f\r\n]+ -> skip ;

// Error catch-all (must be last)
ERROR_CHAR : . ;
