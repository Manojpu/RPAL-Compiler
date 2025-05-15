class CSEMachine:
    def __init__(self, ast, environment):
        self.ast = ast
        self.environment = environment

    def evaluate(self):
        return self._evaluate_node(self.ast)

    def _evaluate_node(self, node):
        if node.type == 'let':
            return self._evaluate_let(node)
        elif node.type == 'lambda':
            return self._evaluate_lambda(node)
        elif node.type == 'function_form':
            return self._evaluate_function_form(node)
        elif node.type == 'ID':
            return self.environment.get(node.value)
        elif node.type == 'INT':
            return node.value
        elif node.type == 'STR':
            return node.value
        elif node.type == 'true':
            return True
        elif node.type == 'false':
            return False
        elif node.type == 'nil':
            return None
        # Add more node types as needed
        else:
            raise Exception(f"Unknown AST node type: {node.type}")

    def _evaluate_let(self, node):
        # Implementation for evaluating let bindings
        pass

    def _evaluate_lambda(self, node):
        # Implementation for evaluating lambda expressions
        pass

    def _evaluate_function_form(self, node):
        # Implementation for evaluating function forms
        pass

    # Additional methods for handling other constructs can be added here.