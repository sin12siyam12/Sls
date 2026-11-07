from tokens import TokenType
from ast_nodes import (
    VariableDeclarationNode,
    BinaryOperationNode,
    NumberNode,
    PrintNode,
    IdentifierNode,
    StringNode,
    IfNode,
    BooleanNode,
    UnaryOperationNode,
    AssignmentNode,
    WhileNode,
    ContinueNode,
    BreakNode,
    FunctionNode,
    FunctionCallNode,
    ReturnNode,
    ElifNode,
    IndexNode,
    ListNode,
    ImportNode,
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]

    def advance(self):
        self.position += 1

        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]

    def expect(self, token_type):
        if self.current_token.type == token_type:
            self.advance()

        else:
            raise Exception(
                f"Expected {token_type}, but got {self.current_token.type} "
                f"at line {self.current_token.line}, column {self.current_token.column}"
            )

    def parse_primary(self):

        if self.current_token.type == TokenType.LEFT_PAREN:
            self.advance()

            expression = self.parse_expression()

            self.expect(TokenType.RIGHT_PAREN)

            node = expression

        elif self.current_token.type == TokenType.LEFT_BRACKET:
            self.advance()

            elements = []

            if self.current_token.type != TokenType.RIGHT_BRACKET:
                while True:
                    elements.append(self.parse_expression())

                    if self.current_token.type == TokenType.RIGHT_BRACKET:
                        break

                    self.expect(TokenType.COMMA)

                self.expect(TokenType.RIGHT_BRACKET)

                node = ListNode(elements)


        elif self.current_token.type == TokenType.NUMBER:
            node = self.parse_number()

        elif self.current_token.type == TokenType.STRING:
            value = self.current_token.value
            self.advance()

            node = StringNode(value)

        elif self.current_token.type == TokenType.BOOLEAN:
            value = self.current_token.value == "true"
            self.advance()

            node = BooleanNode(value)

        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()

            # Function call inside an expression
            if self.current_token.type == TokenType.LEFT_PAREN:
                self.advance()

                arguments = []

                if self.current_token.type != TokenType.RIGHT_PAREN:
                    while True:
                        arguments.append(self.parse_expression())

                        if self.current_token.type == TokenType.RIGHT_PAREN:
                            break

                        self.expect(TokenType.COMMA)

                self.expect(TokenType.RIGHT_PAREN)

                node = FunctionCallNode(name, arguments)

            else:
                node = IdentifierNode(name)

        else:
            raise Exception(
                f"Unexpected token: {self.current_token.value}"
            )

        # Handle indexing: object[index]
        while self.current_token.type == TokenType.LEFT_BRACKET:
            self.advance()

            index = self.parse_expression()

            self.expect(TokenType.RIGHT_BRACKET)

            node = IndexNode(node, index)

        return node

    def parse_variable_declaration(self):
        self.expect(TokenType.LET)

        name = self.current_token.value
        self.expect(TokenType.IDENTIFIER)

        self.expect(TokenType.EQUAL)

        value = self.parse_expression()

        return VariableDeclarationNode(name, value)

    def parse_expression(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()

        while self.current_token.type == TokenType.OR:
            operator = self.current_token
            self.advance()

            right = self.parse_and()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )
        return left

    def parse_and(self):
        left = self.parse_comparison()

        while self.current_token.type == TokenType.AND:
            operator = self.current_token
            self.advance()

            right = self.parse_comparison()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )
        return left

    def parse_comparison(self):
        left = self.parse_term()

        while self.current_token.type in [
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.LESS,
            TokenType.GREATER,
        ]:
            operator = self.current_token
            self.advance()

            right = self.parse_term()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )
        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.current_token.type in [
            TokenType.PLUS,
            TokenType.MINUS
        ]:
            operator = self.current_token
            self.advance()

            right = self.parse_factor()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )
        return left

    def parse_factor(self):
        left = self.parse_unary()

        while self.current_token.type in [
            TokenType.DIVIDE,
            TokenType.MULTIPLY
        ]:
            operator = self.current_token
            self.advance()

            right = self.parse_unary()

            left = BinaryOperationNode(
                left,
                operator,
                right
            )
        return left

    def parse_unary(self):
        if self.current_token.type == TokenType.NOT:
            operator = self.current_token.value
            self.advance()

            operand = self.parse_unary()

            return UnaryOperationNode(
                operator,
                operand
            )
        return self.parse_primary()


    def parse_number(self):
        if self.current_token.type != TokenType.NUMBER:
            raise Exception(f"Unexpected number: {self.current_token.value}")

        token = self.current_token
        self.advance()

        return NumberNode(token.value)

    def parse_print(self):
        self.expect(TokenType.PRINT)


        value = self.parse_expression()

        return PrintNode(value)

    def parse_if(self):
        self.expect(TokenType.IF)

        # Main IF condition
        if_condition = self.parse_expression()

        self.expect(TokenType.COLON)

        # Main IF body
        if_body = self.parse_block()

        # ELIF branches
        elif_bodies = []

        while self.current_token.type == TokenType.ELIF:
            self.advance()

            elif_condition = self.parse_expression()

            self.expect(TokenType.COLON)

            elif_body = self.parse_block()

            elif_bodies.append(
                ElifNode(
                    elif_condition,
                    elif_body
                )
            )

        # ELSE branch
        else_body = None

        if self.current_token.type == TokenType.ELSE:
            self.advance()

            self.expect(TokenType.COLON)

            else_body = self.parse_block()

        return IfNode(
            if_condition,
            if_body,
            elif_bodies,
            else_body
        )

    def parse_statement(self):
        if self.current_token.type == TokenType.LET:
            return self.parse_variable_declaration()

        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print()

        elif self.current_token.type == TokenType.BREAK:
            self.advance()
            return BreakNode()

        elif self.current_token.type == TokenType.CONTINUE:
            self.advance()
            return ContinueNode()

        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.advance()

            if self.current_token.type == TokenType.LEFT_PAREN:
                self.advance()

                arguments = []

                if self.current_token.type != TokenType.RIGHT_PAREN:
                    while True:
                        arguments.append(self.parse_expression())

                        if self.current_token.type == TokenType.RIGHT_PAREN:
                            break

                        self.expect(TokenType.COMMA)

                self.expect(TokenType.RIGHT_PAREN)

                return FunctionCallNode(name, arguments)

            self.expect(TokenType.EQUAL)

            value = self.parse_expression()

            return AssignmentNode(
                name,
                value
            )
        elif self.current_token.type == TokenType.CREATE:
            return self.parse_function()

        elif self.current_token.type == TokenType.RETURN:
            self.advance()

            if self.current_token.type in [
                TokenType.NEWLINE,
                TokenType.DEDENT,
                TokenType.EOF,
            ]:
                return ReturnNode(None)

            value = self.parse_expression()

            return ReturnNode(value)

        elif self.current_token.type == TokenType.IF:
            return self.parse_if()

        elif self.current_token.type == TokenType.WHILE:
            return self.parse_while()

        elif self.current_token.type == TokenType.IMPORT:
            return self.parse_import()

        else:
            raise Exception(f"Unexpected token: {self.current_token.value} "
                            f"at line {self.current_token.line}, column{self.current_token.column}"
                            )

    def parse_block(self):
        self.expect(TokenType.NEWLINE)

        n = 50

        while self.current_token.type != TokenType.INDENT:

            self.advance()

            n -= 1
            if n == 0:
                raise Exception(f"No Indent found at line {self.current_token.line}, column{self.current_token.column}")


        self.expect(TokenType.INDENT)

        statements = []

        while self.current_token.type not in [
            TokenType.DEDENT,
            TokenType.EOF
        ]:
            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(self.parse_statement())

        self.expect(TokenType.DEDENT)

        return statements

    def parse_while(self):
        self.expect(TokenType.WHILE)

        condition = self.parse_expression()

        self.expect(TokenType.COLON)

        body = self.parse_block()

        return WhileNode(condition, body)

    def parse_function(self):
        self.expect(TokenType.CREATE)

        name = self.current_token.value
        self.expect(TokenType.IDENTIFIER)

        self.expect(TokenType.LEFT_PAREN)

        parameters = []

        if self.current_token.type != TokenType.RIGHT_PAREN:
            while True:
                if self.current_token.type != TokenType.IDENTIFIER:
                    raise Exception(f"Unexpected parameter name, "
                                    f"but got {self.current_token.value} at line {self.current_token.line}, column{self.current_token.column}")

                parameters.append(self.current_token.value)
                self.advance()

                if self.current_token.type == TokenType.RIGHT_PAREN:
                    break

                self.expect(TokenType.COMMA)

        self.expect(TokenType.RIGHT_PAREN)

        self.expect(TokenType.COLON)

        body = self.parse_block()

        return FunctionNode(
            name,
            parameters,
            body
        )

    def parse_import(self):
        self.expect(TokenType.IMPORT)

        filename = self.current_token.value
        self.expect(TokenType.STRING)

        return ImportNode(filename)

    def parse(self):
        statements = []

        while self.current_token.type != TokenType.EOF:

            if self.current_token.type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(self.parse_statement())

        return statements
