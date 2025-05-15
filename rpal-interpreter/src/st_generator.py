class SymbolTableGenerator:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = {}

    def enter_scope(self):
        self.current_scope = {}

    def exit_scope(self):
        self.symbol_table.update(self.current_scope)
        self.current_scope = {}

    def visit(self, node):
        method_name = f'visit_{node.type}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_let(self, node):
        self.enter_scope()
        for declaration in node.children:
            self.visit(declaration)
        self.exit_scope()

    def visit_function_form(self, node):
        func_name = node.children[0].value
        self.current_scope[func_name] = 'function'
        for param in node.children[1:]:
            self.current_scope[param.value] = 'parameter'
        self.visit(node.children[-1])  # Visit the function body

    def visit_ID(self, node):
        if node.value not in self.current_scope:
            self.current_scope[node.value] = 'variable'

    def visit_rec(self, node):
        self.enter_scope()
        self.visit(node.children[0])  # Visit the declaration
        self.exit_scope()

    def visit_tau(self, node):
        for child in node.children:
            self.visit(child)

    def generate_symbol_table(self, ast):
        self.visit(ast)
        return self.symbol_table