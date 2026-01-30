from enum import Enum
from parser import ASTNode

class ASTPrinter:
    def print(self, node, indent=0):
        prefix = "  " * indent

        # Caso base
        if node is None:
            print(f"{prefix}None")
            return

        # ENUM → folha (nunca explorar)
        if isinstance(node, Enum):
            print(f"{prefix}{node.name}")
            return

        # Tipos primitivos → folha
        if isinstance(node, (str, int, float, bool)):
            print(f"{prefix}{node}")
            return

        # Lista → iterar
        if isinstance(node, list):
            for item in node:
                self.print(item, indent)
            return

        # AST Node → explorar
        if isinstance(node, ASTNode):
            print(f"{prefix}{type(node).__name__}")

            for attr, value in vars(node).items():
                print(f"{prefix}  {attr}:")
                self.print(value, indent + 2)
            return

        # Qualquer outro caso (segurança)
        print(f"{prefix}{node}")
