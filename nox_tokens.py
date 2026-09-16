class Tokentype:
    #END OF FILE AND ILLEGAL
    EOF = 'EOF'
    ILLEGAL = 'ILLEGAL'
    #KEYWORDS
    LET = 'LET'
    SAME = 'SAME'
    FUN = 'FUN'
    IF = 'IF'
    ELSE = 'ELSE'
    ELF = 'ELF'
    GIVE = 'GIVE'
    OUT = 'OUT'
    ASK = 'ASK'
    IN = 'IN'
    WHILE = 'WHILE'
    FROM = 'FROM'
    TO = 'TO'
    BY = 'BY'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    #IDENTIFIERS + LITERALS
    IDENTIFIER = 'IDENTIFIER'
    INT = 'INT'
    FLOAT = 'FLOAT'
    STR = 'STR'
    BOOL = 'BOOL'
    #OPERATORS
    ASSIGN = 'ASSIGN'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    STAR = 'STAR'
    SLASH = 'SLASH'
    PERCENT = 'PERCENT'
    EQ = 'EQ'
    NOT_EQ = 'NOT_EQ'
    LT = 'LT'
    GT = 'GT'
    GTE = 'GTE'
    LTE = 'LTE'
    #DELIMITERS
    COMMA = 'COMMA'
    COLON = 'COLON'
    SEMICOLON = 'SEMICOLON'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACE = 'LBRACE'
    RBRACE = 'RBRACE'
    #indentation
    INDENT = 'INDENT'
    DEDENT = 'DEDENT'
    NEWLINE = 'NEWLINE'
# a dictionary of keywords that maps strings to their corresponding token types
KEYWORDS = {
     'let'   : Tokentype.LET,
     "same"  : Tokentype.SAME,
     "fun"   : Tokentype.FUN,
     "give"  : Tokentype.GIVE,
     "out"   : Tokentype.OUT,
     "ask"   : Tokentype.ASK,
     "in"    : Tokentype.IN,
     "if"    : Tokentype.IF,
     "elf"   : Tokentype.ELF,
     "else"  : Tokentype.ELSE,
     "while" : Tokentype.WHILE,
     "from"  : Tokentype.FROM,
     "to"    : Tokentype.TO,
     "by"    : Tokentype.BY,
     "and"   : Tokentype.AND,
     "or"    : Tokentype.OR,
     "not"   : Tokentype.NOT,
     "true"  : Tokentype.TRUE,
     "false" : Tokentype.FALSE,
}

class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal

    def __repr__(self):
        return f'Token({self.type}, {self.literal})'