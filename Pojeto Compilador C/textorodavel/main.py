from lexer import Lexer
from parser import Parser
from ast_printer import ASTPrinter
from semantic import SemanticAnalyzer


code = open("program.mc").read()

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
printer = ASTPrinter()
printer.print(ast)

semantic = SemanticAnalyzer()
semantic.analyze(ast)


print("Programa válido!")
