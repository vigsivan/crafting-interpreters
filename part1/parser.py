from typing import List, Final
from Expr import Binary, Grouping, Literal, Unary
from util import Token, TokenType

class ParserException(Exception):
    """Parser Exception"""

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: Final = tokens
        self.current: int = 0

    def expression(self):
        return self.equality()

    def parse(self):
        try:
            return self.expression()
        except ParserException:
            return None

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.BANG_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(
            TokenType.GREATER_EQUAL,
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def consume(self, ttype: TokenType, msg: str):
        if self.check(ttype): return self.advance()
        raise self.error(self.peek(), msg)

    def error(self, token: Token, msg: str):
        Lox.error(token, msg)
        return ParserException(msg)

    def synchronize(self):
        self.advance() 

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                case (TokenType.CLASS |
                      TokenType.FUN |
                      TokenType.VAR |
                      TokenType.FOR |
                      TokenType.IF |
                      TokenType.WHILE |
                      TokenType.PRINT |
                      TokenType.RETURN) :
                     return

            self.advance()

    def previous(self):
        return self.tokens[self.current - 1]

    def check(self, ttype: TokenType):
        if self.is_at_end():
            return False
        return self.peek().type == ttype

    def is_at_end(self) -> bool:
        return False

    def peek(self):
        return self.tokens[self.current]

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def match(self, *args: TokenType):
        for ttype in args:
            if self.check(ttype):
                self.advance()
                return True
        return False