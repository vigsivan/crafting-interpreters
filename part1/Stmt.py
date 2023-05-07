from abc import ABC
from Expr import Expr
from util import Token
from typing import Optional

class Stmt(ABC):
	def accept(self, visitor):
		return visitor(self)


class Expression(Stmt):
	def __init__(self,  expression: Expr): 
		self. expression: Expr=  expression
	def accept(self, visitor):
		return visitor.visit_expression(self)

class Print(Stmt):
	def __init__(self,  expression: Expr): 
		self. expression: Expr=  expression
	def accept(self, visitor):
		return visitor.visit_print(self)

class Var(Stmt):
	def __init__(self,  name: Token, initializer: Optional[Expr]): 
		self. name: Token=  name
		self. initializer =  initializer
	def accept(self, visitor):
		return visitor.visit_var(self)
