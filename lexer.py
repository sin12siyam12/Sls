from tokens import Token, TokenType

KEYWORDS = {
            "let": TokenType.LET,
            "print": TokenType.PRINT,
            "if": TokenType.IF,
            "elif": TokenType.ELIF,
            "while": TokenType.WHILE,
            "else": TokenType.ELSE,
            "true": TokenType.BOOLEAN,
            "false": TokenType.BOOLEAN,
            "and": TokenType.AND,
            "or": TokenType.OR,
            "not": TokenType.NOT,
            "create": TokenType.CREATE,
            "return": TokenType.RETURN,
            "break": TokenType.BREAK,
            "continue": TokenType.CONTINUE,
            "import": TokenType.IMPORT,
        }

OPERATORS = {
    "=": TokenType.EQUAL,
    "+=": TokenType.PLUS_EQUAL,
    "-=": TokenType.MINUS_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,
    "==": TokenType.EQUAL_EQUAL,
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    "**": TokenType.POWER,
    "*": TokenType.MULTIPLY,




}

class Lexer:
    def __init__(self, text):
        self.current_operator = None
        self.expected_operator = None
        self.text = text
        self.position = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        self.at_line_start = True

        if len(text) > 0:
            self.current = text[0]
        else:
            self.current = None

    def advance(self):
        if self.current == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        self.position += 1

        if self.position < len(self.text):
            self.current = self.text[self.position]

        else:
            self.current = None


    def peek(self):
        next_position = self.position + 1

        if next_position >= len(self.text):
            return None

        else:
            return self.text[next_position]

    def skip_whitespace(self):
        while self.current is not None and self.current in " \t":
            self.advance()

    def count_indentation(self):
        count = 0

        while self.current == " ":
            count += 1
            self.advance()

        return count

    def read_identifier(self):
        word = ""
        start_column = self.column


        while(self.current is not None and (self.current.isalnum() or self.current == "_")):
            word += self.current
            self.advance()

        if word in KEYWORDS:
            return Token(
                KEYWORDS[word],
                word,
                self.line,
                start_column
            )
        else:
            return Token(
                TokenType.IDENTIFIER,
                word,
                self.line,
                start_column
            )

    def read_number(self):
        number = ""
        is_decimal = False

        start_column = self.column

        while self.current is not None:

            # Read digits
            if self.current.isdigit():
                number += self.current
                self.advance()

            # Read decimal point
            elif self.current == ".":

                # Prevent 5.6.7
                if is_decimal:
                    break

                is_decimal = True
                number += self.current
                self.advance()

            else:
                break

        if is_decimal:
            return Token(
                TokenType.DECIMAL,
                float(number),
                self.line,
                start_column
            )

        else:
            return Token(
                TokenType.NUMBER,
                int(number),
                self.line,
                start_column
            )

    def read_string(self):
        string = ""
        start_column = self.column

        # Skip opening quote
        self.advance()

        while self.current is not None and self.current != '"':

            if self.current == "\\":
                self.advance()

                if self.current == "n":
                    string += "\n"

                elif self.current == "t":
                    string += "\t"

                elif self.current == '"':
                    string += '"'

                elif self.current == "\\":
                    string += "\\"

                else:
                    string += self.current

            else:
                string += self.current

            self.advance()

        # Check if string was closed
        if self.current is None:
            raise Exception(
                f"Error at line {self.line}: Unterminated string."
            )

        # Skip closing quote
        self.advance()

        return Token(
            TokenType.STRING,
            string,
            self.line,
            start_column
        )
    
    def match_operator(self, current_operator, expected_operator, line, column):
        self.current_operator = current_operator
        self.expected_operator = expected_operator
        self.line = line
        self.column = column
        
        peek = self.peek()



        if peek is not None and peek == expected_operator:
            return_operator = current_operator + expected_operator

            self.advance()
            self.advance()

            return Token(
                OPERATORS[return_operator],
                return_operator,
                self.line,
                self.column
            )

        else:
            self.advance()

            return Token(
                OPERATORS[current_operator],
                current_operator,
                self.line,
                self.column
            )


    def scan_tokens(self):
        tokens = []

        while self.current is not None:

            if self.at_line_start:
                indent = self.count_indentation()


                if self.current == "\n":
                    tokens.append(
                        Token(
                            TokenType.NEWLINE,
                            None,
                            self.line,
                            self.column
                        )
                    )
                    self.advance()
                    self.at_line_start = True
                    continue

                if self.current is None:
                    break

                self.at_line_start = False

                if indent > self.indent_stack[-1]:
                    self.indent_stack.append(indent)

                    tokens.append(
                        Token(
                            TokenType.INDENT,
                            None,
                            self.line,
                            self.column
                        )
                    )

                while indent < self.indent_stack[-1]:
                    self.indent_stack.pop()

                    tokens.append(
                        Token(
                            TokenType.DEDENT,
                            None,
                            self.line,
                            self.column
                        )
                    )

            elif self.current in " \t":
                self.skip_whitespace()

            elif self.current == "\n":
                tokens.append(Token(TokenType.NEWLINE, None, self.line, self.column))
                self.advance()
                self.at_line_start = True

            elif self.current.isalpha() or self.current == "_":
                tokens.append(self.read_identifier())

            elif self.current.isdigit():
                tokens.append(self.read_number())

            elif self.current == '"':
                tokens.append(self.read_string())

            elif self.current == "=":
                tokens.append(
                    self.match_operator("=", "=", self.line, self.column)
                )

            elif self.current == "+":
                tokens.append(
                    self.match_operator("+", "=", self.line, self.column)
                )

            elif self.current == "-":
                tokens.append(
                    self.match_operator("-", "=", self.line, self.column)
                )


            elif self.current == "*":
                tokens.append(
                    self.match_operator("*", "*", self.line, self.column)
                )

            elif self.current == "/":
                tokens.append(
                    Token(
                        TokenType.DIVIDE,
                        "/",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == "!":
                peeks = self.peek()

                if peeks == "=":
                    tokens.append(
                        Token(
                        TokenType.NOT_EQUAL,
                            "!=",
                            self.line,
                            self.column
                        )
                    )
                else:
                    raise Exception(
                        f"Unexpected character '{self.current}'"
                        f" at line {self.line}, column {self.column}"
                    )
                self.advance()
                self.advance()

            elif self.current == "<":
                tokens.append(
                    self.match_operator("<", "=", self.line, self.column)
                )

            elif self.current == ">":
                tokens.append(
                    self.match_operator(">", "=", self.line, self.column)
                )


            elif self.current == ":":
                tokens.append(
                    Token(
                        TokenType.COLON,
                        ":",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == "(":
                tokens.append(
                    Token(
                        TokenType.LEFT_PAREN,
                        "(",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == "[":
                tokens.append(
                    Token(
                        TokenType.LEFT_BRACKET,
                        "[",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == "]":
                tokens.append(
                    Token(
                        TokenType.RIGHT_BRACKET,
                        "]",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == ",":
                tokens.append(
                    Token(
                        TokenType.COMMA,
                        ",",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            elif self.current == ")":
                tokens.append(
                    Token(
                        TokenType.RIGHT_PAREN,
                        ")",
                        self.line,
                        self.column
                    )
                )
                self.advance()

            else:
                raise Exception(
                    f"Unexpected character '{self.current}' "
                    f"at line {self.line}, column {self.column}"
                )

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()

            tokens.append(
                Token(
                    TokenType.DEDENT,
                    None,
                    self.line,
                    self.column
                )
            )

        tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return tokens