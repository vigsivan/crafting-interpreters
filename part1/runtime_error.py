from typing import Final
from util import Token
class RuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token: Final[Token] = token
        self.message = message

class BreakException(Exception):
    def __init__(self):
        ...
