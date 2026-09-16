class Node:
    pass
#literals
class Intliteral (Node):
    def __init__(self, value):
        self.value = value
class Floatliteral (Node):
    def __init__(self, value):
        self.value = value
class Stringliteral (Node):
    def __init__(self, value):
        self.value = value
class Booleanliteral (Node):
    def __init__(self, value):
        self.value = value
class Identifier(Node):
    def __init__(self, name):
        self.name = name
#expressions 
class Binaryop(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
class Unaryop(Node):
    def __init__(self, op, right):
        self.op = op
        self.operand = right
class Functioncall(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args
class Assignment(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
#statements
class Vardecl(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
class Constdecl(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
class Funcdecl(Node):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
class Returnstmt(Node):
    def __init__(self, value):
        self.value = value
class Outstmt(Node):
    def __init__(self, value):
        self.value = value
class Askexpr(Node):
    def __init__(self, value):
        self.value = value
#control states
class Ifstmt(Node):
    def __init__(self, condition, then_block, elf_clauses, else_block):
        self.condition   = condition
        self.then_block  = then_block
        self.elf_clauses = elf_clauses 
        self.else_block  = else_block
class Whilestmt(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body      = body
class Rangeloop(Node):
    def __init__(self, var, start, end,step, body):
        self.var   = var
        self.start = start
        self.end   = end
        self.step = step
        self.body  = body
class Listloop(Node):
    def __init__(self, var, iterable, body):
        self.var      = var
        self.iterable = iterable
        self.body     = body
class Program(Node):
    def __init__(self, statements):
        self.statements = statements