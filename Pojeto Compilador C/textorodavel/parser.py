from lexer import TokenType

# ===============================
# AST
# ===============================

class ASTNode:
    pass


class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class VarDecl(ASTNode):
    def __init__(self, var_type, name, initializer):
        self.var_type = var_type
        self.name = name
        self.initializer = initializer


class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Print(ASTNode):
    def __init__(self, expressions):
        self.expressions = expressions


class Read(ASTNode):
    def __init__(self, name):
        self.name = name


class If(ASTNode):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch


class While(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements


class BinaryExpr(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpr(ASTNode):
    def __init__(self, operator, expr):
        self.operator = operator
        self.expr = expr


class Literal(ASTNode):
    def __init__(self, value, literal_type):
        self.value = value
        self.literal_type = literal_type


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name


# ===============================
# PARSER
# ===============================

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._statement())
        return Program(statements)

    # ---------- Statements ----------

    def _statement(self):
        if self._match(TokenType.INT, TokenType.FLOAT, TokenType.STRING):
            return self._var_declaration()

        if self._match(TokenType.IDENTIFIER):
            return self._assignment()

        if self._match(TokenType.PRINT):
            return self._print_statement()

        if self._match(TokenType.READ):
            return self._read_statement()

        if self._match(TokenType.IF):
            return self._if_statement()

        if self._match(TokenType.WHILE):
            return self._while_statement()

        if self._match(TokenType.LBRACE):
            return self._block()

        if self._match(TokenType.SEMICOLON):
            return None

        raise SyntaxError("Comando inválido")

    def _var_declaration(self):
        var_type = self._previous().type
        name = self._consume(TokenType.IDENTIFIER, "Esperado identificador").lexeme

        initializer = None
        if self._match(TokenType.ASSIGN):
            initializer = self._expression()

        self._consume(TokenType.SEMICOLON, "Esperado ';'")
        return VarDecl(var_type, name, initializer)

    def _assignment(self):
        name = self._previous().lexeme
        self._consume(TokenType.ASSIGN, "Esperado '='")
        value = self._expression()
        self._consume(TokenType.SEMICOLON, "Esperado ';'")
        return Assignment(name, value)

    def _print_statement(self):
        self._consume(TokenType.LPAREN, "Esperado '('")
        exprs = [self._expression()]
        while self._match(TokenType.COMMA):
            exprs.append(self._expression())
        self._consume(TokenType.RPAREN, "Esperado ')'")
        self._consume(TokenType.SEMICOLON, "Esperado ';'")
        return Print(exprs)

    def _read_statement(self):
        self._consume(TokenType.LPAREN, "Esperado '('")
        name = self._consume(TokenType.IDENTIFIER, "Esperado identificador").lexeme
        self._consume(TokenType.RPAREN, "Esperado ')'")
        self._consume(TokenType.SEMICOLON, "Esperado ';'")
        return Read(name)

    def _if_statement(self):
        self._consume(TokenType.LPAREN, "Esperado '('")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Esperado ')'")
        then_branch = self._statement()
        else_branch = None
        if self._match(TokenType.ELSE):
            else_branch = self._statement()
        return If(condition, then_branch, else_branch)

    def _while_statement(self):
        self._consume(TokenType.LPAREN, "Esperado '('")
        condition = self._expression()
        self._consume(TokenType.RPAREN, "Esperado ')'")
        body = self._statement()
        return While(condition, body)

    def _block(self):
        statements = []
        while not self._check(TokenType.RBRACE):
            statements.append(self._statement())
        self._consume(TokenType.RBRACE, "Esperado '}'")
        return Block(statements)

    # ---------- Expressões ----------

    def _expression(self):
        return self._logic_or()

    def _logic_or(self):
        expr = self._logic_and()
        while self._match(TokenType.OR):
            expr = BinaryExpr(expr, self._previous(), self._logic_and())
        return expr

    def _logic_and(self):
        expr = self._equality()
        while self._match(TokenType.AND):
            expr = BinaryExpr(expr, self._previous(), self._equality())
        return expr

    def _equality(self):
        expr = self._relational()
        while self._match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            expr = BinaryExpr(expr, self._previous(), self._relational())
        return expr

    def _relational(self):
        expr = self._additive()
        while self._match(TokenType.LESS, TokenType.GREATER,
                          TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            expr = BinaryExpr(expr, self._previous(), self._additive())
        return expr

    def _additive(self):
        expr = self._multiplicative()
        while self._match(TokenType.PLUS, TokenType.MINUS):
            expr = BinaryExpr(expr, self._previous(), self._multiplicative())
        return expr

    def _multiplicative(self):
        expr = self._unary()
        while self._match(TokenType.MULT, TokenType.DIV):
            expr = BinaryExpr(expr, self._previous(), self._unary())
        return expr

    def _unary(self):
        if self._match(TokenType.NOT, TokenType.MINUS):
            return UnaryExpr(self._previous(), self._unary())
        return self._primary()

    def _primary(self):
        if self._match(TokenType.INT_CONST):
            return Literal(int(self._previous().lexeme), TokenType.INT)

        if self._match(TokenType.FLOAT_CONST):
            return Literal(float(self._previous().lexeme), TokenType.FLOAT)

        if self._match(TokenType.STRING_LITERAL):
            return Literal(self._previous().lexeme, TokenType.STRING)

        if self._match(TokenType.IDENTIFIER):
            return Variable(self._previous().lexeme)

        if self._match(TokenType.LPAREN):
            expr = self._expression()
            self._consume(TokenType.RPAREN, "Esperado ')'")
            return expr

        raise SyntaxError("Expressão inválida")

    # ---------- Utilitários ----------

    def _match(self, *types):
        for t in types:
            if self._check(t):
                self._advance()
                return True
        return False

    def _consume(self, token_type, message):
        if self._check(token_type):
            return self._advance()
        raise SyntaxError(message)

    def _check(self, token_type):
        return not self._is_at_end() and self._peek().type == token_type

    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _is_at_end(self):
        return self._peek().type == TokenType.EOF

