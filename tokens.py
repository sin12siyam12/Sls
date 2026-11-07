class Token:
    def __init__(self, token_type, value = None, line = 0, column = 0):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return (
            f"Token(type={self.type},"
            f" value={self.value},"
            f" line={self.line},"
            f" column={self.column})"
        )

class TokenType:
    LET = "LET"
    PRINT = "PRINT"
    IF = "IF"
    ELIF = "ELIF"
    WHILE = "WHILE"
    ELSE = "ELSE"
    AND = "AND"
    OR = "OR"
    NOT = "NOT"
    CREATE = "CREATE"
    RETURN = "RETURN"

    IMPORT = "IMPORT"

    BREAK = "BREAK"
    CONTINUE = "CONTINUE"

    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"

    IDENTIFIER = "IDENTIFIER"

    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    PLUS_EQUAL = "PLUS_EQUAL"
    MINUS_EQUAL = "MINUS_EQUAL"
    POWER = "POWER"

    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"

    GREATER = "GREATER"
    LESS = "LESS"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS_EQUAL = "LESS_EQUAL"

    COLON = "COLON"
    COMMA = "COMMA"

    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACKET = "LEFT_BRACKET"
    RIGHT_BRACKET = "RIGHT_BRACKET"

    INDENT = "INDENT"
    DEDENT = "DEDENT"

    NEWLINE = "NEWLINE"
    EOF = "EOF"