import sys
from typing import Final, List
from scanner import Scanner
from util import Token, TokenType
# from parser import Parser
from Expr import Binary, Grouping, Literal, Unary
from tool.ast_printer import AstPrinter

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

class Lox:
    had_error: bool = False

    @classmethod
    def main(cls, *args):
        if len(args) > 1:
            print(f"Usage: {sys.argv[0]} [script]")
            sys.exit(64)
        elif len(args) == 1:
            cls.run_file(args[0])
        else:
            print("Running REPL")
            cls.run_prompt()

    @classmethod
    def run_file(cls, arg: str):
        with open(arg, "rb") as f:
            bytes = f.read()

        cls.run(bytes.decode("utf-8"))
        if cls.had_error:
            sys.exit(65)

    @classmethod
    def run_prompt(cls):
        while True:
            line = input("> ")
            if len(line.strip()) == 0:
                break
            cls.run(line)

    @classmethod
    def run(cls, source: str):
        scanner = Scanner(source, cls.error)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if cls.had_error or expression is None:
            return
        
        print(AstPrinter().print(expression))


    @classmethod
    def error(cls, line: int | Token, message: str):
        if isinstance(line, int):
            cls.report(line, "", message)
        else:
            if line.type == TokenType.EOF:
                cls.report(line.line, " at end", message)
            else:
                cls.report(line.line, f" at '{line.lexeme}'", message)


    @classmethod
    def report(cls, line: int, where: str, message: str):
        s = f"[line {line}] Error {where}: {message}"
        print(s)
        cls.had_error = True
        return s
