from typing import Any, Dict, Final, Optional, Self
from runtime_error import RuntimeError
from util import Token


class Environment:
    def __init__(self, enclosing: Optional[Self] = None, inside_loop: bool=False):
        self.values: Dict[str, Any] = {}
        self.enclosing: Final[Optional[Self]] = enclosing
        self.inside_loop = inside_loop

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
        elif self.enclosing:
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
