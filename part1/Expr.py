from abc import ABC
from typing import Any, Callable, Optional
from util import Token

class Expr(ABC):
    def accept(self, visitor):
        return visitor(self)


class Binary(Expr):
    def __init__(self,  left: Expr, operator: Token, right: Expr): 
        self. left: Expr=  left
        self. operator: Token=  operator
        self. right: Expr=  right
    def accept(self, visitor):
        return visitor.visit_binary(self)

class Grouping(Expr):
    def __init__(self,  expression: Expr): 
        self. expression: Expr=  expression
    def accept(self, visitor):
        return visitor.visit_grouping(self)

class Literal(Expr):
    def __init__(self,  value): 
        self. value=  value
    def accept(self, visitor):
        return visitor.visit_literal(self)

class Unary(Expr):
    def __init__(self,  operator: Token, right: Expr): 
        self. operator: Token=  operator
        self. right: Expr=  right
    def accept(self, visitor):
        return visitor.visit_unary(self)

class Variable(Expr):
    def __init__(self, name: Token):
        self.name = name
    
    def accept(self, visitor):
        return visitor.visit_variable(self)

class Assign(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value
    
    def accept(self, visitor):
        return visitor.visit_assign(self)

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self. left: Expr=  left
        self. operator: Token=  operator
        self. right: Expr=  right
    def accept(self, visitor):
        return visitor.visit_logical(self)

