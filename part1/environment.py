from typing import Any, Dict
from runtime_error import RuntimeError
from util import Token

class Environment:
    def __init__(self):
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise RuntimeError(name, f"Undefined variable {name.lexeme}.")
