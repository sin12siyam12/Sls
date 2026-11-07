class NumberNode:
    def __init__(self, value):
        self.value = value

class IdentifierNode:
    def __init__(self, name):
        self.name = name

class VariableDeclarationNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class BinaryOperationNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class PrintNode:
    def __init__(self, value):
        self.value = value

class StringNode:
    def __init__(self, value):
        self.value = value

class BooleanNode:
    def __init__(self, value):
        self.value = value

class IfNode:
    def __init__(self, condition, body,elif_bodies, else_body=None):
        self.condition = condition
        self.body = body
        self.elif_bodies = elif_bodies or []
        self.else_body = else_body

class UnaryOperationNode:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

class AssignmentNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BreakNode:
    pass

class ContinueNode:
    pass

class FunctionNode:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class FunctionCallNode:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

class ReturnNode:
    def __init__(self, value):
        self.value = value

class ElifNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class IndexNode:
    def __init__(self,object_node, index):
        self.object_node = object_node
        self.index = index

class ListNode:
    def __init__(self, elements):
        self.elements = elements

class ImportNode:
    def __init__(self, filename):
        self.filename = filename

class ModuleNode:
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement