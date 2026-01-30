import re
from enum import Enum, auto
from dataclasses import dataclass

# ===============================
# Token Types
# ===============================

class TokenType(Enum):
    # Keywords
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    PRINT = auto()
    READ = auto()

    # Identifiers & literals
    IDENTIFIER = auto()
    INT_CONST = auto()
    FLOAT_CONST = auto()
    STRING_LITERAL = auto()

    # Operators (ordem importa!)
    EQUAL = auto()           # ==
    NOT_EQUAL = auto()       # !=
    GREATER_EQUAL = auto()   # >=
    LESS_EQUAL = auto()      # <=
    GREATER = auto()         # >
    LESS = auto()            # <
    ASSIGN = auto()          # =
    PLUS = auto()            # +
    MINUS = auto()           # -
    MULT = auto()            # *
    DIV = auto()             # /
    AND = auto()             # &&
    OR = auto()              # ||
    NOT = auto()             # !

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()

    EOF = auto()


# ===============================
# Token
# ===============================

@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int


# ===============================
# Lexer
# ===============================

class Lexer:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0

        self.keywords = {
            "int": TokenType.INT,
            "float": TokenType.FLOAT,
            "string": TokenType.STRING,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "print": TokenType.PRINT,
            "read": TokenType.READ,
        }

        # Ordem das regex prioritárias.
        self.token_specs = [
            (r'==', TokenType.EQUAL),
            (r'!=', TokenType.NOT_EQUAL),
            (r'>=', TokenType.GREATER_EQUAL),
            (r'<=', TokenType.LESS_EQUAL),
            (r'&&', TokenType.AND),
            (r'\|\|', TokenType.OR),

            (r'>', TokenType.GREATER),
            (r'<', TokenType.LESS),
            (r'=', TokenType.ASSIGN),
            (r'\+', TokenType.PLUS),
            (r'-', TokenType.MINUS),
            (r'\*', TokenType.MULT),
            (r'/', TokenType.DIV),
            (r'!', TokenType.NOT),

            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\{', TokenType.LBRACE),
            (r'\}', TokenType.RBRACE),
            (r',', TokenType.COMMA),
            (r';', TokenType.SEMICOLON),

            (r'"[^"]*"', TokenType.STRING_LITERAL),
            (r'\d+\.\d+', TokenType.FLOAT_CONST),
            (r'\d+', TokenType.INT_CONST),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),

            (r'[ \t]+', None),
            (r'\n', None),
            (r'//.*', None),
        ]

    def tokenize(self):
        while self.pos < len(self.source):
            match = None

            for pattern, token_type in self.token_specs:
                regex = re.compile(pattern)
                match = regex.match(self.source, self.pos)

                if match:
                    lexeme = match.group(0)

                    if token_type:
                        if token_type == TokenType.IDENTIFIER and lexeme in self.keywords:
                            token_type = self.keywords[lexeme]

                        self.tokens.append(
                            Token(token_type, lexeme, self.line, self.column)
                        )

                    self._advance(lexeme)
                    break

            if not match:
                raise SyntaxError(
                    f"Caractere inesperado '{self.source[self.pos]}' "
                    f"na linha {self.line}, coluna {self.column}"
                )

        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

    def _advance(self, lexeme):
        for char in lexeme:
            if char == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        self.pos += len(lexeme)
# ===============================

# End of lexer.py