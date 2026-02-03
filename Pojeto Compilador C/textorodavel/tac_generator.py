from parser import *

class TACGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        method = f"gen_{type(node).__name__}"
        return getattr(self, method)(node)

    # =========================
    # Program & Statements
    # =========================

    def gen_Program(self, node):
        for stmt in node.statements:
            self.generate(stmt)
        return self.code

    def gen_Block(self, node):
        for stmt in node.statements:
            self.generate(stmt)

    def gen_VarDecl(self, node):
        if node.initializer:
            value = self.generate(node.initializer)
            self.code.append(f"{node.name} = {value}")

    def gen_Assignment(self, node):
        value = self.generate(node.value)
        self.code.append(f"{node.name} = {value}")

    def gen_Print(self, node):
        for expr in node.expressions:
            value = self.generate(expr)
            self.code.append(f"print {value}")

    def gen_Read(self, node):
        self.code.append(f"read {node.name}")

    # =========================
    # Control Flow
    # =========================

    def gen_If(self, node):
        cond = self.generate(node.condition)
        label_else = self.new_temp()
        label_end = self.new_temp()

        self.code.append(f"ifFalse {cond} goto {label_else}")
        self.generate(node.then_branch)
        self.code.append(f"goto {label_end}")
        self.code.append(f"{label_else}:")
        if node.else_branch:
            self.generate(node.else_branch)
        self.code.append(f"{label_end}:")

    def gen_While(self, node):
        label_start = self.new_temp()
        label_end = self.new_temp()

        self.code.append(f"{label_start}:")
        cond = self.generate(node.condition)
        self.code.append(f"ifFalse {cond} goto {label_end}")
        self.generate(node.body)
        self.code.append(f"goto {label_start}")
        self.code.append(f"{label_end}:")

    # =========================
    # Expressions
    # =========================

    def gen_BinaryExpr(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {node.operator.lexeme} {right}")
        return temp

    def gen_UnaryExpr(self, node):
        expr = self.generate(node.expr)
        temp = self.new_temp()
        self.code.append(f"{temp} = {node.operator.lexeme}{expr}")
        return temp

    def gen_Literal(self, node):
        return str(node.value)

    def gen_Variable(self, node):
        return node.name
