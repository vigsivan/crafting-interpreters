from abc import ABC
from Expr import Expr
from util import Token
from typing import List

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
	def __init__(self,  name: Token, initializer: Expr | None): 
		self. name: Token=  name
		self. initializer =  initializer
	def accept(self, visitor):
		return visitor.visit_var(self)

class Block(Stmt):
	def __init__(self, statements: List[Stmt] ): 
		self.statements = statements
	def accept(self, visitor):
		return visitor.visit_block(self)

class If(Stmt):
	def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Stmt | None):
		self.condition = condition
		self.then_branch = then_branch
		self.else_branch = else_branch

	def accept(self, visitor):
		return visitor.visit_if(self)

class While(Stmt):
	def __init__(self, condition: Expr | None, loop_body: Stmt):
		self.condition = condition
		self.loop_body = loop_body

	def accept(self, visitor):
		return visitor.visit_while(self)

class For(Stmt):
	def __init__(self, initialization: Stmt | None, condition: Expr | None, update: Expr | None, loop_body: Stmt):
		self.initialization = initialization
		self.condition = condition
		self.update = update
		self.body = loop_body

	def accept(self, visitor):
		return visitor.visit_for(self)

class Break(Stmt):
	def accept(self, visitor):
		return visitor.visit_break(self)
