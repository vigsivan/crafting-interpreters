from typing import Any, List
from Stmt import Block, Print, Expression, Stmt, Var
from Expr import Assign, Binary, Expr, Grouping, Literal, Unary, Variable
from util import Token, TokenType
from runtime_error import RuntimeError
from environment import Environment

class Interpreter:
    def __init__(self):
        self.environment = Environment()

    def interpret(self, statements: List[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            raise e

    def execute(self, statement: Stmt):
        statement.accept(self)

    def visit_var(self, statement: Var):
        value = None
        if statement.initializer is not None:
            value = self.evaluate(statement.initializer)
        self.environment.define(statement.name.lexeme, value)

    def visit_variable(self, expression: Variable):
        return self.environment.get(expression.name)

    def visit_expression(self, stmt: Expression):
        self.evaluate(stmt.expression)

    def visit_block(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(self.environment))

    def visit_print(self, stmt: Print):
        value = stmt.expression.accept(self)
        print(self.stringify(value))

    def visit_literal(self, expr: Literal):
        return expr.value

    def visit_grouping(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visit_unary(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return -float(right)

        # should be unreachable
        return None

    def visit_assign(self, expr: Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visit_binary(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.check_number_operand(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operand(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                elif isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeError(expr.operator,
                                   "Operands must be two numbers or two strings")
            case TokenType.GREATER:
                self.check_number_operand(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operand(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operand(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

    # also does check_number_operands
    def check_number_operand(self, operator: Token, *operands: Any):
        if all(isinstance(operand, float) for operand in operands):
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def is_equal(self, a: Any, b: Any) -> bool:
        if a is None and b is None: return True
        if a is None:
            return False
        return a == b

    def is_truthy(self, object: Any) -> bool:
        if object is None: return False
        if isinstance(object, bool): return bool(object)
        return True

    def stringify(self, object: Any):
        if object is None: return "nil"
        return str(object)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def execute_block(self, statements: List[Stmt], environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
