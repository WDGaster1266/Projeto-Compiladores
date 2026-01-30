from lexer import Lexer

'''
code = """
int x;
x = 10;
if (x >= 5) {
    print(x);
}
"""
'''
'''
code = 
int a;
int b;
a = 10;

if (a > 5) {
    b = a + 1;
}
'''

# ===============================
# Teste básico de erro
code = "int x @ 10;"
#Lexer(code).tokenize()

lexer = Lexer(code)
tokens = lexer.tokenize()

for t in tokens:
    print(t)


# ===============================
# Teste de erro simples
