from lexer import Lexer
from parser import Parser
from interpreter import Interpreter


with open("compiler.sls", "r") as file:
    source = file.read()


lexer = Lexer(source)
tokens = lexer.scan_tokens()

for token in tokens:
    print(token.type, token.value)


parser = Parser(tokens)
ast = parser.parse()


interpreter = Interpreter()

for statement in ast:
    interpreter.visit(statement)