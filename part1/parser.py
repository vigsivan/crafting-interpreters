from typing import List, Final
from Expr import Assign, Binary, Call, Grouping, Literal, Unary, Variable, Logical
from Stmt import Block, Break, If, FunctionStatement, Print, Expression, Var, For, While, Stmt, Return
from util import Token, TokenType

MAX_ARGUMENTS = 255

class ParserException(Exception):
    """Parser Exception"""
    def __init__(self, token: Token, message: str):
        self.token: Final[Token] = token
        self.message = message

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens: Final = tokens
        self.current: int = 0

    def parse(self):
        statements = []
        while not self.is_at_end():
            declaration = self.declaration()
            if declaration is not None:
                statements.append(declaration)
        return statements

    def expression(self):
        return self.assignment()

    def function(self):
        if self.match(TokenType.FUN):
            expr = self.parse_function()
        else:
            expr = self.logical_or()
        return expr

    def assignment(self):
        expr = self.function()

        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()

            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)

            raise ParserException(equals, "Invalid assignment target.")
        return expr

    def logical_or(self):
        expr = self.logical_and()
        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.logical_and()
            expr = Logical(expr, operator, right)
        return expr

    def logical_and(self):
        expr = self.equality()
        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            else:
                return self.statement()
        except ParserException as e:
            self.synchronize()
            raise e

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name")

        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Var(name, initializer)

    def statement(self):
        # if self.match(TokenType.FUN):
        #     return self.function_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        if self.match(TokenType.EOF):
            return
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.RETURN):
            return self.return_statement()

        return self.expression_statement()

    def parse_function(self):
        if not self.check(TokenType.LEFT_PAREN):
            name = self.consume(TokenType.IDENTIFIER, "Expect function name")
        else:
            name = None
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after fun name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
                if not self.match(TokenType.COMMA):
                    break
                if len(parameters) >= MAX_ARGUMENTS:
                    raise ParserException(self.peek(), f"Can't have more than {MAX_ARGUMENTS} parameters")
        self.consume(TokenType.RIGHT_PAREN , "Expect ')' after function parameters.")
        implementation = self.statement()
        return FunctionStatement(name, parameters, implementation)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition of 'while'.")
        loop_body = self.statement()
        # FIXME:
        assert loop_body is not None
        return While(condition, loop_body)

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
        if self.match(TokenType.SEMICOLON):
            initialization = None
        elif self.match(TokenType.VAR):
            initialization = self.var_declaration()
        else:
            initialization = self.expression_statement()
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        else:
            condition = None
        self.consume(TokenType.SEMICOLON, "Expect ';' after condition in 'for'.")

        if not self.check(TokenType.RIGHT_PAREN):
            update = self.expression()
        else:
            update = None
        self.consume(TokenType.RIGHT_PAREN, "Expect ) after for-loop update")
        loop_body = self.statement()
        return For(initialization, condition, update, loop_body)

    def return_statement(self):
        token = self.previous()
        return_value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value")
        return Return(token, return_value)

    def break_statement(self):
        break_token = self.previous()
        self.consume(TokenType.SEMICOLON, "Expect ';' after break")
        return Break(break_token)

    def block(self):
        statements = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            try:
                statements.append(self.declaration())
            except ParserException as pe:
                raise pe
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        expr = self.expression()
        if isinstance(expr, FunctionStatement):
            return Expression(expr)
        self.consume(TokenType.SEMICOLON, "Expect ';' after value in expression statement.")
        return Expression(expr)

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
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
        return self.call()
    
    def call(self):
        # think of this primary expression as being the left
        # operand to the '(' operator
        expr = self.primary()
        while True:
            if self.match(TokenType.LEFT_PAREN):
                arguments = self.parse_args()
                paren = self.consume(TokenType.RIGHT_PAREN
                                     , "Expect ')' after function arguments.")
                expr = Call(expr, paren, arguments)
            else:
                break

        return expr

    def parse_args(self):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
                if len(arguments) >= MAX_ARGUMENTS:
                    raise ParserException(self.peek(), f"Can't have more than {MAX_ARGUMENTS} arguments")
        return arguments
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise ParserException(self.peek(), "Expect expression.")

    def consume(self, ttype: TokenType, msg: str):
        if self.check(ttype): return self.advance()
        raise ParserException(self.peek(), msg)

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
        return self.current >= len(self.tokens)
        # return False

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
