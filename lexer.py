from nox_tokens import Tokentype, KEYWORDS, Token
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.indent_stack = [0]  #stack to track indentation
    def current_char(self):
        if self.position >= len(self.code):
            return None
        return self.code[self.position]
    def advance(self):
        if self.current_char() == '\n':
            self.line += 1
            self.column = 0
        self.position += 1
        self.column += 1
    def peek(self):
        peek_pos = self.position + 1
        if peek_pos >= len(self.code):
            return None
        return self.code[peek_pos]
    def handle_newline(self):
        self.tokens.append(Token(Tokentype.NEWLINE, '\\n'))
        self.advance()
        #handle indentation
        indent_level = 0
        while self.current_char() == ' ':
            indent_level += 1
            self.advance()
        if indent_level > self.indent_stack[-1]:
            self.indent_stack.append(indent_level)
            self.tokens.append(Token(Tokentype.INDENT, indent_level))
        while indent_level < self.indent_stack[-1]:
            self.indent_stack.pop()
            self.tokens.append(Token(Tokentype.DEDENT, indent_level))
    def read_identifier(self):
        start_pos = self.position
        while self.current_char() is not None and (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()
        literal = self.code[start_pos : self.position]
        if literal in KEYWORDS:
            token_type = KEYWORDS[literal]
        else:
            token_type = Tokentype.IDENTIFIER
        self.tokens.append(Token(token_type, literal))
    def read_number(self):
        start_pos = self.position
        has_dot =False
        while self.current_char() is not None and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if has_dot:
                    break
                has_dot = True
            self.advance()
        literal = self.code[start_pos : self.position]
        if has_dot:
            self.tokens.append(Token(Tokentype.FLOAT, literal))
        else:
            self.tokens.append(Token(Tokentype.INT, literal))
    def read_string(self, quote_type):
        self.advance()
        start_pos = self.position
        while self.current_char() is not None and self.current_char() != quote_type:
            if self.current_char() == '\\' and self.peek() == quote_type:
                self.advance()
            self.advance()
        literal = self.code[start_pos : self.position]
        self.advance()  # skip closing quote
        self.tokens.append(Token(Tokentype.STR, literal))
    def tokenize(self):
        while self.current_char() is not None:
            if self.current_char() in (' ', '\t'):
                self.advance()
            elif self.current_char() == '\n':
                self.handle_newline()
            elif self.current_char().isalpha() or self.current_char() == '_':
                self.read_identifier()
            elif self.current_char().isdigit():
                self.read_number()
            elif self.current_char() in ('"', "'"):
                self.read_string(self.current_char())
            elif self.current_char() == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(Tokentype.EQ, '=='))
                else:
                    self.advance()
                    self.tokens.append(Token(Tokentype.ASSIGN, '='))
            elif self.current_char() == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(Tokentype.NOT_EQ, '!='))
                else:
                    self.advance()
                    self.tokens.append(Token(Tokentype.ILLEGAL, '!'))
            elif self.current_char() == '<':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(Tokentype.LTE, '<='))
                else:
                    self.advance()
                    self.tokens.append(Token(Tokentype.LT, '<'))
            elif self.current_char() == '>':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    self.tokens.append(Token(Tokentype.GTE, '>='))
                else:
                    self.advance()
                    self.tokens.append(Token(Tokentype.GT, '>'))
            elif self.current_char() == '+':
                self.advance()
                self.tokens.append(Token(Tokentype.PLUS, '+'))
            elif self.current_char() == '-':
                self.advance()
                self.tokens.append(Token(Tokentype.MINUS, '-'))
            elif self.current_char() == '*':
                self.advance()
                self.tokens.append(Token(Tokentype.STAR, '*'))
            elif self.current_char() == '/':
                self.advance()
                self.tokens.append(Token(Tokentype.SLASH, '/'))
            elif self.current_char() == '%':
                self.advance()
                self.tokens.append(Token(Tokentype.PERCENT, '%'))
            elif self.current_char() == ',':
                self.advance()
                self.tokens.append(Token(Tokentype.COMMA, ','))
            elif self.current_char() == ';':
                self.advance()
                self.tokens.append(Token(Tokentype.SEMICOLON, ';'))
            elif self.current_char() == ':':
                self.advance()
                self.tokens.append(Token(Tokentype.COLON, ':'))
            elif self.current_char() == '(':
                self.advance()
                self.tokens.append(Token(Tokentype.LPAREN, '('))
            elif self.current_char() == ')':
                self.advance()
                self.tokens.append(Token(Tokentype.RPAREN, ')'))
            elif self.current_char() == '{':
                self.advance()
                self.tokens.append(Token(Tokentype.LBRACE, '{'))
            elif self.current_char() == '}':
                self.advance()
                self.tokens.append(Token(Tokentype.RBRACE, '}'))
            else:
                self.tokens.append(Token(Tokentype.ILLEGAL, self.current_char()))
                self.advance()
        while len(self.indent_stack) > 1 :
            self.indent_stack.pop()
            self.tokens.append(Token(Tokentype.DEDENT, 0))
        self.tokens.append(Token(Tokentype.EOF, ''))
        return self.tokens