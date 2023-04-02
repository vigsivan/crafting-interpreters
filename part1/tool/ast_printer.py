from Expr import Binary, Expr, Grouping, Literal, Unary
from util import Token, TokenType

class AstPrinter:
    def print(self, expr: Expr):
        return expr.accept(self)

    def visit_binary(self, expr: Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visit_literal(self, expr: Literal):
        if expr.value == None: return "nil"
        return str(expr.value)

    def visit_unary(self, expr: Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name: str, *args: Expr):
        s = f"({name} "
        s = s + " ".join(expr.accept(self) for expr in args)
        s = s + ")"
        return s

if __name__ == "__main__":
    def main():
        expression = Binary(
            Unary(
                Token(TokenType.MINUS, "-",None, 1),
                Literal(123)),
            Token(TokenType.STAR, "*", None, 1),
            Grouping(Literal(45.67)))
        print(AstPrinter().print(expression))

    main()
