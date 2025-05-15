def handle_error(message):
    raise Exception(message)

def type_check(value, expected_type):
    if not isinstance(value, expected_type):
        handle_error(f"Expected value of type {expected_type}, got {type(value)}")

def print_ast(ast_node):
    if ast_node is None:
        return
    ast_node.print_ast()