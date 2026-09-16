from nox_ast import *
from nox_tokens import Tokentype, Token, KEYWORDS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def current_token(self):
        if self.pos >= len(self.tokens):
            return None
        return self.tokens[self.pos]
    def advance(self):
        self.pos +=1
    def peek_token(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.tokens):
            return None
        return self.tokens[peek_pos]
    def expect(self, token_type):
        if self.current_token() is not None and self.current_token().type == token_type:
            token = self.current_token()
            self.advance()
            return token
        else:
            raise Exception(f"Expected token type {token_type} but got {self.current_token().type if self.current_token() is not None else 'None'}")
    def parse(self):
        statements = []
        while self.current_token().type != Tokentype.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return Program(statements)
    def parse_statement(self):
        token = self.current_token()
        if token.type == Tokentype.LET:
            return self.parse_Vardecl()
        elif token.type == Tokentype.SAME:
            return self.parse_Constdecl()
        elif token.type == Tokentype.FUN:
            return self.parse_Funcdecl()
        elif token.type == Tokentype.GIVE:
            return self.parse_Returnstmt()
        elif token.type == Tokentype.OUT:
            return self.parse_Outstmt()
        elif token.type == Tokentype.IF:
            return self.parse_Ifstmt()
        elif token.type == Tokentype.WHILE:
            return self.parse_Whilestmt()
        elif token.type == Tokentype.ASK:
            return self.parse_Askexpr()
        elif token.type == Tokentype.NEWLINE:
            self.advance()
            return None
        elif token.type == Tokentype.IDENTIFIER:
            if self.peek_token().type == Tokentype.FROM:
                return self.parse_Rangeloop()
            elif self.peek_token().type == Tokentype.IN:
                return self.parse_Listloop()
            else :
                return self.parse_identifier_stmt()
        else:
            raise Exception(f"unexpected token {token.type}")
    def parse_Vardecl(self):
        self.expect(Tokentype.LET)
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.ASSIGN)
        value = self.parse_expression()
        return Vardecl(name,value)
    def parse_Constdecl(self):
        self.expect(Tokentype.SAME)
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.ASSIGN)
        value = self.parse_expression()
        return Constdecl(name,value) 
    def parse_params(self):
        params = []
        while self.current_token().type != Tokentype.RPAREN:
            param = self.expect(Tokentype.IDENTIFIER).literal
            params.append(param)
            if self.current_token().type == Tokentype.COMMA:
                self.advance()
        return params
    def parse_Funcdecl(self):
        self.expect(Tokentype.FUN)
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.LPAREN)
        params = self.parse_params()
        self.expect(Tokentype.RPAREN)
        self.expect(Tokentype.COLON)
        body = self.parse_block()
        return Funcdecl(name, params, body)
    def parse_block(self):
        if self.current_token().type == Tokentype.NEWLINE :
            self.advance()
        self.expect(Tokentype.INDENT)
        statements = []
        while self.current_token().type not in  (Tokentype.DEDENT, Tokentype.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        self.expect(Tokentype.DEDENT)
        return statements
    def parse_Ifstmt(self):
        self.expect(Tokentype.IF)
        condition = self.parse_expression()
        self.expect(Tokentype.COLON)
        then_block = self.parse_block()
        elf_clauses = []
        while self.current_token().type == Tokentype.ELF:
            self.expect(Tokentype.ELF)
            elf_condition = self.parse_expression()
            self.expect(Tokentype.COLON)
            elf_block = self.parse_block()
            elf_clauses.append((elf_condition, elf_block))
        else_block = None
        if self.current_token().type == Tokentype.ELSE:
            self.expect(Tokentype.ELSE)
            self.expect(Tokentype.COLON)
            else_block = self.parse_block()
        return Ifstmt(condition, then_block, elf_clauses, else_block)
    def parse_Whilestmt(self):
        self.expect(Tokentype.WHILE)
        condition = self.parse_expression()
        self.expect(Tokentype.COLON)
        body = self.parse_block()
        return Whilestmt(condition, body)
    def parse_Rangeloop(self):
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.FROM)
        start = self.parse_expression()
        self.expect(Tokentype.TO)
        end = self.parse_expression()
        step = None
        if self.current_token().type == Tokentype.BY:
            self.expect(Tokentype.BY)
            step = self.parse_expression()
        self.expect(Tokentype.COLON)
        body = self.parse_block()
        return Rangeloop(name, start, end, step, body)
    def parse_Listloop(self):
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.IN)
        iterable = self.parse_expression()
        self.expect(Tokentype.COLON)
        body = self.parse_block()
        return Listloop(name, iterable, body)
    def parse_Outstmt(self):
        self.expect(Tokentype.OUT)
        self.expect(Tokentype.LPAREN)
        value = self.parse_expression()
        self.expect(Tokentype.RPAREN)
        return Outstmt(value)
    def parse_Returnstmt(self):
        self.expect(Tokentype.GIVE)
        value = self.parse_expression()
        return Returnstmt(value)
    def parse_identifier_stmt(self):
        if self.peek_token().type == Tokentype.ASSIGN:
            return self.parse_Assignment()
        elif self.peek_token().type == Tokentype.LPAREN:
            return self.parse_Functioncall()
        else:
            raise Exception(f"unexpected token {self.current_token().type}")
    def parse_Assignment(self):
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.ASSIGN)
        value = self.parse_expression()
        return Assignment(name, value)
    def parse_Askexpr(self):
            self.expect(Tokentype.ASK)
            self.expect(Tokentype.LPAREN)
            prompt = None
            if self.current_token().type != Tokentype.RPAREN:
                prompt = self.parse_expression()
            self.expect(Tokentype.RPAREN)
            return Askexpr(prompt)
    def parse_Functioncall(self):
        name = self.expect(Tokentype.IDENTIFIER).literal
        self.expect(Tokentype.LPAREN)
        args = []
        while self.current_token().type != Tokentype.RPAREN:
            arg = self.parse_expression()
            args.append(arg)
            if self.current_token().type == Tokentype.COMMA:
                self.advance()
        self.expect(Tokentype.RPAREN)
        return Functioncall(name, args)
    def parse_expression(self):
        left = self.parse_comparision()
        while self.current_token().type in (Tokentype.AND, Tokentype.OR):
            op = self.current_token().literal
            self.advance()
            right = self.parse_comparision()
            left = Binaryop(left, op, right)
        return left
    def parse_comparision(self):
        left = self.parse_term()
        while self.current_token().type in (Tokentype.EQ, Tokentype.NOT_EQ, Tokentype.GT, Tokentype.GTE, Tokentype.LT, Tokentype.LTE):
            op = self.current_token().literal
            self.advance()
            right = self.parse_term()
            left = Binaryop(left, op, right)
        return left
    def parse_term(self):
        left = self.parse_factor()
        while self.current_token().type in (Tokentype.PLUS, Tokentype.MINUS):
            op = self.current_token().literal
            self.advance()
            right = self.parse_factor()
            left = Binaryop(left, op, right)
        return left
    def parse_factor(self):
        left = self.parse_unary()
        while self.current_token().type in (Tokentype.STAR, Tokentype.SLASH, Tokentype.PERCENT):
            op = self.current_token().literal
            self.advance()
            right = self.parse_unary()
            left = Binaryop(left, op, right)
        return left
    def parse_unary(self):
        if self.current_token().type in (Tokentype.NOT, Tokentype.MINUS):
            op = self.current_token().literal
            self.advance()
            right = self.parse_unary()
            return  Unaryop(op, right)
        return self.parse_primary()
    def parse_primary(self):
        token = self.current_token()
        if token.type == Tokentype.INT:
            self.advance()
            return Intliteral(token.literal)
        elif token.type == Tokentype.FLOAT:
            self.advance()
            return Floatliteral(token.literal)
        elif token.type == Tokentype.STR:
            self.advance()
            return Stringliteral(token.literal)
        elif token.type == Tokentype.TRUE:
            self.advance()
            return Booleanliteral(True)
        elif token.type == Tokentype.FALSE:
            self.advance()
            return Booleanliteral(False)
        elif token.type == Tokentype.ASK:
            return self.parse_Askexpr()
        elif token.type == Tokentype.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(Tokentype.RPAREN)
            return expr
        elif token.type == Tokentype.IDENTIFIER:
            if self.peek_token().type == Tokentype.LPAREN :
                return self.parse_Functioncall()
            self.advance()
            return Identifier(token.literal)
        else :
            raise Exception(f"unexpected Token {token.type}")