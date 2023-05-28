from typing import Any, Final
from util import Token
class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token: Final[Token] = token
        self.message = message

class BreakException(Exception):
    def __init__(self):
        pass

class ReturnException(Exception):
    def __init__(self, return_value: Any):
        self.value = return_value
        pass
