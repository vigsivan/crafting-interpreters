"""
Scanner implementation in Python

Things we haven't implemented yet:
    * Number Literals
"""

import sys
from typing import Any, List, Optional
from util import Token, TokenType

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1


    def scan_tokens(self) -> List[Token]:
        while not self.is_at_end():
            start = None # current
            self.scan_token()
            if start is None:
                break

        self.tokens.append(Token(TokenType.EOF, "", None, self.line+1))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        if c == ')':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == '(':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        elif c == '*':
            self.add_token(TokenType.STAR)
        elif c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c in [' ', '\r', '\t']:
            return
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        else:
            # FIXME make this more like the Java implementation
            raise ValueError(f"Character {c} on line {self.line}")

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            # FIXME: make this more like the Java implementation
            raise ValueError("Unterminated string")

        # move past the closing "
        self.advance()

        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, c):
        ...

    def number(self, c):
        ...

    def advance(self) -> str:
        ...

    def add_token(self, ttype: TokenType, literal: Optional[Any]=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(ttype, text, literal, self.line))

    def match(self, expected: str):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end(): return '\0'
        return self.source[self.current]
