class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []
    
    def add_child(self, node):
        self.children.append(node)
        return node
    
    def print_ast(self, prefix=""):
        if self.value is not None:
            print(f"{prefix}{self.type}:{self.value}")
        else:
            print(f"{prefix}{self.type}")
        for child in self.children:
            child.print_ast(prefix + ".")