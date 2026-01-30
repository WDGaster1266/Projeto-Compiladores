from lexer import TokenType
from parser import *

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Variável '{name}' já declarada")
        self.symbols[name] = var_type

    def get(self, name):
        if name not in self.symbols:
            raise Exception(f"Variável '{name}' não declarada")
        return self.symbols[name]


class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()

    def analyze(self, node):
        if node is None:
            return None
        method = f"visit_{type(node).__name__}"
        return getattr(self, method)(node)

    def visit_Program(self, node):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_Block(self, node):
        for stmt in node.statements:
            self.analyze(stmt)

    def visit_VarDecl(self, node):
        self.table.declare(node.name, node.var_type)
        if node.initializer:
            init_type = self.analyze(node.initializer)
            if init_type != node.var_type:
                raise Exception("Tipos incompatíveis na inicialização")

    def visit_Assignment(self, node):
        var_type = self.table.get(node.name)
        value_type = self.analyze(node.value)
        if var_type != value_type:
            raise Exception("Tipos incompatíveis na atribuição")

    def visit_Print(self, node):
        for expr in node.expressions:
            self.analyze(expr)

    def visit_Read(self, node):
        self.table.get(node.name)

    def visit_If(self, node):
        self.analyze(node.condition)
        self.analyze(node.then_branch)
        if node.else_branch:
            self.analyze(node.else_branch)

    def visit_While(self, node):
        self.analyze(node.condition)
        self.analyze(node.body)

    def visit_BinaryExpr(self, node):
        left = self.analyze(node.left)
        right = self.analyze(node.right)
        if left != right:
            raise Exception("Operação entre tipos incompatíveis")
        return left

    def visit_UnaryExpr(self, node):
        return self.analyze(node.expr)

    def visit_Literal(self, node):
        return node.literal_type

    def visit_Variable(self, node):
        return self.table.get(node.name)
    