from typing import Any, Dict, Final, Optional, Self
from runtime_error import RuntimeError
from util import Token


class Environment:
    def __init__(self, enclosing: Optional[Self] = None):
        self.values: Dict[str, Any] = {}
        self.enclosing: Final[Optional[Self]] = enclosing

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        if self.enclosing:
            return self.enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")

    def assign(self, name: Token, value: Any):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        if self.enclosing:
            self.enclosing.assign(name, value)
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
