"""
Scanner implementation in Python
"""

# TODO: test the implementation

from typing import Any, List, Optional
from util import Token, TokenType


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

        self.reserved_keywords_map = {
            # Keywords,
            "and": TokenType.AND ,
            "class": TokenType.CLASS ,
            "else": TokenType.ELSE ,
            "false": TokenType.FALSE ,
            "fun": TokenType.FUN ,
            "if": TokenType.IF ,
            "nil": TokenType.NIL ,
            "or": TokenType.OR ,
            "print": TokenType.PRINT ,
            "return": TokenType.RETURN ,
            "super": TokenType.SUPER ,
            "this": TokenType.THIS ,
            "true": TokenType.TRUE ,
            "var": TokenType.VAR ,
            "while": TokenType.WHILE ,
        }

    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            start = None  # current
            self.scan_token()
            if start is None:
                break

        self.tokens.append(Token(TokenType.EOF, "", None, self.line + 1))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        if c == ")":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == "(":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == "*":
            self.add_token(TokenType.STAR)
        elif c == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG)
        elif c == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
            )
        elif c == ">":
            self.add_token(
                TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
            )
        elif c == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS)
        elif c in [" ", "\r", "\t"]:
            return
        elif c == "\n":
            self.line += 1
        elif c == '"':
            self.string()
        else:
            if self.is_digit(c):
                self.number()
            elif self.is_alpha(c):
                self.identifier()
            else:
                # FIXME make this more like the Java implementation
                raise ValueError(f"Character {c} on line {self.line}")

    def is_alpha(self, c) -> bool:
        return (c >= 'a' and c <= 'z' or
                c >= 'A' and c <= 'Z' or
                c == '_')

    def is_alphanumeric(self, c):
        return (self.is_alpha(c) or self.is_digit(c))

    def identifier(self):
        while self.is_alphanumeric(self.peek()): self.advance()
        text = self.source[self.start:self.current]
        if text in self.reserved_keywords_map:
            self.add_token(self.reserved_keywords_map[text])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            # FIXME: make this more like the Java implementation
            raise ValueError("Unterminated string")

        # move past the closing "
        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, c) -> bool:
        return c >= '0' and c <= '9'

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()
        
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

        while self.is_digit(self.peek()):
            self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def advance(self) -> str:
        ...

    def add_token(self, ttype: TokenType, literal: Optional[Any] = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(ttype, text, literal, self.line))

    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current+1]


