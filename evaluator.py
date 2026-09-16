from nox_ast import *
class Environment :
    def __init__(self,parent = None):
        self.store = {}
        self.constants = set()
        self.parent = parent
    def get(self, name): 
        if name in self.store:
            return self.store[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise Exception(f"unidentified variable '{name}'")
    def set(self, name, value):
        self.store[name] = value
    def set_const(self, name, value):
        self.store[name] = value
        self.constants.add(name)
    def assign(self, name, value):
        if name in self.constants:
            raise Exception(f"cannot reassign constants '{name}'")
        self.store[name] = value
class Evaluator:
    def __init__(self):
        self.environment = Environment()
    def evaluate(self, node):
        if isinstance(node, Program):
            result = None
            for stmt in node.statements:
                result = self.evaluate(stmt)
            return result
        elif isinstance(node, Intliteral):
            return int(node.value)
        elif isinstance(node, Floatliteral):
            return float(node.value)
        elif isinstance(node, Stringliteral):
            return str(node.value)
        elif isinstance(node, Booleanliteral):
            return node.value
        elif isinstance(node, Identifier):
            return self.environment.get(node.name)
        elif isinstance(node, Vardecl):
            value = self.evaluate(node.value)
            return self.environment.set(node.name, value)
        elif isinstance(node, Outstmt):
            value = self.evaluate(node.value)
            print(value)
        elif isinstance(node, Constdecl):
            value  = self.evaluate(node.value)
            return self.environment.set_const(node.name, value)
        elif isinstance(node, Assignment):
            value = self.evaluate(node.value)
            self.environment.assign(node.name, value)
        elif isinstance(node, Binaryop):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            match node.op:
                case "+" : return left + right
                case "-" : return left - right
                case "*" : return left * right
                case "/" : return left / right
                case "%" : return left % right
                case "==" : return left == right
                case "!=" : return left != right
                case ">" : return left > right
                case "<" : return left < right
                case ">=" : return left >= right
                case "<=" : return left <= right
                case "and" : return left and right
                case "or" : return left or right
                case _ : raise Exception(f"unknown operater{node.op}")
        elif isinstance(node, Unaryop):
            right = self.evaluate(node.operand)
            match node.op:
                case "not" : return not right
                case "-" : return - right
                case _: raise Exception(f"unknown operater{node.op}")
        elif isinstance(node, Ifstmt):
            condition = self.evaluate(node.condition)
            if condition :
                for statement in node.then_block:
                    self.evaluate(statement)
            else:
                matched = False
                for elf_condition, elf_block in node.elf_clauses:
                    if self.evaluate(elf_condition):
                        for stmt in elf_block:
                            self.evaluate(stmt)
                        matched = True
                        break
                if not matched and node.else_block:
                    for stmt in node.else_block:
                        self.evaluate(stmt)
        elif isinstance(node, Whilestmt):
            while self.evaluate(node.condition):
                for stmt in node.body :
                    self.evaluate(stmt)
        elif isinstance(node, Rangeloop):
            start = self.evaluate(node.start)
            end = self.evaluate(node.end)
            step = 1
            if node.step is not None:
                step = self.evaluate(node.step)
            for i in range(start, end, step):
                self.environment.set(node.var, i )
                for stmt in node.body :
                    self.evaluate(stmt)
        elif isinstance(node, Listloop):
            iterable = self.evaluate(node.iterable)
            for item in iterable :
                self.environment.set(node.var , item)
                for stmt in node.body :
                    self.evaluate(stmt)
        elif isinstance(node, Funcdecl):
            self.environment.set(node.name, node)
        elif isinstance(node, Functioncall):
            func = self.environment.get(node.name)
            args = []
            for arg in node.args:
                args.append(self.evaluate(arg))
            old_envi = self.environment
            self.environment = Environment(parent = old_envi)
            for param, arg in zip(func.params, args):
                self.environment.set(param, arg)
            result = None
            for stmt in func.body :
                result = self.evaluate(stmt)
            self.environment = old_envi
            return result
        elif isinstance(node, Returnstmt):
            return self.evaluate(node.value)
        elif isinstance(node, Askexpr):
            prompt = self.evaluate(node.value)
            user_input = input(prompt)
            try:
                return int(user_input)
            except ValueError:
                try:
                    return float(user_input)
                except ValueError:
                    return user_input