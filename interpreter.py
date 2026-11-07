from ast_nodes import (
    VariableDeclarationNode,
    BinaryOperationNode,
    NumberNode,
    IdentifierNode,
    PrintNode,
    StringNode,
    IfNode,
    BooleanNode,
    UnaryOperationNode,
    AssignmentNode,
    WhileNode,
    BreakNode,
    ContinueNode,
    FunctionNode,
    FunctionCallNode,
    ReturnNode,
    IndexNode,
    ListNode,
    ImportNode,
)
from environment import Environment
from lexer import Lexer
from tokens import TokenType
from parser import Parser

class BreakException(Exception):
    pass

class ContinueException(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.environment = Environment()
        self.functions = {}
        self.loop_depth = 0

    def visit(self, node):

        if isinstance(node, NumberNode):
            return node.value

        elif isinstance(node, BinaryOperationNode):
            return self.visit_binary(node)

        elif isinstance(node, VariableDeclarationNode):
            return self.visit_variable(node)

        elif isinstance(node, IdentifierNode):
            return self.visit_identifier(node)

        elif isinstance(node, PrintNode):
            return self.visit_print(node)

        elif isinstance(node, StringNode):
            return self.visit_StringNode(node)

        elif isinstance(node, IfNode):
            return self.visit_if(node)

        elif isinstance(node, BooleanNode):
            return node.value

        elif isinstance(node, UnaryOperationNode):
            return self.visit_unary(node)

        elif isinstance(node, AssignmentNode):
            return self.visit_assignment(node)

        elif isinstance(node, WhileNode):
            return self.visit_while(node)

        elif isinstance(node, BreakNode):
            return self.visit_break(node)

        elif isinstance(node, ContinueNode):
            return self.visit_continue(node)

        elif isinstance(node, FunctionNode):
            return self.visit_function(node)

        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call(node)

        elif isinstance(node, ReturnNode):
            return self.visit_return(node)

        elif isinstance(node, IndexNode):
            return self.visit_index(node)

        elif isinstance(node, ListNode):
            return self.visit_list(node)
        elif isinstance(node, ImportNode):
            return self.visit_import(node)

        else:
            raise Exception(f"Unknown node type: {type(node)}")

    def visit_binary(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)


        if node.operator.type == TokenType.PLUS:
            return left + right

        elif node.operator.type == TokenType.MINUS:
            return left - right

        elif node.operator.type == TokenType.MULTIPLY:
            return left * right

        elif node.operator.type == TokenType.DIVIDE:
            return left / right

        elif node.operator.type == TokenType.POWER:
            return left ** right

        elif node.operator.type == TokenType.GREATER:
            return left > right

        elif node.operator.type == TokenType.LESS:
            return left < right

        elif node.operator.type == TokenType.GREATER_EQUAL:
            return left >= right

        elif node.operator.type == TokenType.NOT_EQUAL:
            return left != right

        elif node.operator.type == TokenType.EQUAL_EQUAL:
            return left == right

        elif node.operator.type == TokenType.LESS_EQUAL:
            return left <= right

        elif node.operator.type == TokenType.AND:
            return left and right

        elif node.operator.type == TokenType.OR:
            return left or right


        else:
            raise Exception(f"Unknown operator type: {type(node)}")

    def visit_StringNode(self, node):
        return node.value

    def visit_unary(self, node):
        operand = self.visit(node.operand)

        if node.operator == "not":
            return not operand

        raise Exception(
            f"Unknown unary operator: {node.operator}"
        )

    def visit_variable(self, node):
        value = self.visit(node.value)

        self.environment.define(node.name, value)

        return value

    def visit_identifier(self, node):
        return self.environment.get(node.name)

    def visit_print(self, node):
        value = self.visit(node.value)

        return print(value)

    def visit_if(self, node):
        condition = self.visit(node.condition)

        if condition:
            for statement in node.body:
                self.visit(statement)
            return

        for elif_node in node.elif_bodies:
            condition = self.visit(elif_node.condition)

            if condition:
                for statement in elif_node.body:
                    self.visit(statement)
                return

        if node.else_body is not None:
            for statement in node.else_body:
                self.visit(statement)

    def visit_while(self, node):
        while self.visit(node.condition):
            try:
                for statement in node.body:
                    self.visit(statement)

            except BreakException:
                break

            except ContinueException:
                continue

            finally:
                self.loop_depth -= 1

    def visit_assignment(self, node):
        value = self.visit(node.value)

        self.environment.assign(node.name, value)

        return value

    def visit_break(self, node):
        if self.loop_depth == 0:
            raise Exception(f"'break' outside loop")

        raise BreakException()

    def visit_continue(self, node):
        if self.loop_depth == 0:
            raise Exception(f"'continue' outside loop")

        raise ContinueException()

    def visit_function(self, node):
        if node.name in self.functions:
            raise Exception(f"Function '{node.name}' is already defined")

        self.functions[node.name] = node

    def visit_function_call(self, node):

        if node.name == "read_file":

            if len(node.arguments) != 1:
                raise Exception(
                    "read_file() expects exactly 1 argument"
                )

            filename = self.visit(node.arguments[0])

            if not isinstance(filename, str):
                raise Exception(
                    "read_file() expects a string filename"
                )

            try:
                with open(filename, "r", encoding="utf-8") as file:
                    return file.read()

            except FileNotFoundError:
                raise Exception(
                    f"file not found: {filename}"
                )

        if node.name == "contains":
            if len(node.arguments) != 2:
                raise Exception(
                    "contains() expects 2 arguments"
                )

            text = self.visit(node.arguments[0])
            value = self.visit(node.arguments[1])

            try:
                return value in text
            except TypeError:
                raise Exception(
                    "contains() can't be used on this value"
                )

        if node.name == "length":
            if len(node.arguments) != 1:
                raise Exception(
                    "length() expects exactly 1 argument"
                )

            value = self.visit(node.arguments[0])

            try:
                return len(value)
            except TypeError:
                raise Exception(
                    "length() can't be used on this value"
                )

        if node.name not in self.functions:
            raise Exception(f"Undefined function: {node.name}")

        function = self.functions[node.name]

        if len(node.arguments) != len(function.parameters):
            raise Exception(
                f"Function '{node.name}' expects "
                f"{len(function.parameters)} argument(s), "
                f"but got {len(node.arguments)}"
            )

        # Evaluate arguments in the current environment
        arguments = [
            self.visit(argument)
            for argument in node.arguments
        ]

        # Save current environment
        previous_environment = self.environment

        # Create a new local environment whose parent
        # is the current environment
        self.environment = Environment(previous_environment)

        try:
            # Bind parameters
            for parameter, argument in zip(
                    function.parameters,
                    arguments
            ):
                self.environment.define(parameter, argument)

            # Execute function body
            try:
                for statement in function.body:
                    self.visit(statement)

            except ReturnException as return_value:
                return return_value.value

        finally:
            # Restore previous environment
            self.environment = previous_environment

    def visit_return(self, node):

        if node.value is None:
            raise ReturnException(None)

        value = self.visit(node.value)
        raise ReturnException(value)

    def visit_index(self, node):
        object_value = self.visit(node.object_node)
        index_value = self.visit(node.index)

        try:
            return object_value[index_value]
        except IndexError:
            raise Exception(f"Index out of range: {index_value}")

        except TypeError:
            raise Exception(f"Can't index this value: {index_value}")

    def visit_list(self, node):
        elements = []

        for element in node.elements:
            elements.append(self.visit(element))

        return elements

    def visit_import(self, node):
        with open(node.filename, "r", encoding="utf-8") as f:
            source = f.read()

        lexer = Lexer(source)
        token = lexer.scan_tokens()

        parser = Parser(token)
        program = parser.parse()

        for statement in program:
            self.visit(statement)
