# filepath: /rpal-interpreter/rpal-interpreter/src/main.py
import sys
from lexer import tokenize_file
from parser import Parser
from evaluator import Evaluator
from environment import Environment

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file.rpal>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    try:
        tokens = tokenize_file(input_file)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Print the AST structure
        print("AST structure:")
        ast.print_ast()
        
        # Create an environment and pass it to the evaluator
        environment = Environment()
        # Add built-in functions to the environment
        add_built_ins(environment)
        
        evaluator = Evaluator(environment)
        result = evaluator.evaluate(ast)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

def add_built_ins(env):
    # Add built-in functions like Print, arithmetic operations, etc.
    env.set('Print', lambda x: print(x) or x)
    env.set('+', lambda x, y: x + y)
    env.set('-', lambda x, y: x - y)
    env.set('*', lambda x, y: x * y)
    env.set('/', lambda x, y: x / y)
    env.set('eq', lambda x, y: x == y)
    env.set('ne', lambda x, y: x != y)
    
    # Add tuple access function - lets you get Nth element (1-based indexing)
    def order(t):
        if isinstance(t, tuple):
            return len(t)
        return 1
    
    # This allows accessing elements of a tuple by index (1-based)
    def tuple_access(t, n):
        if isinstance(t, tuple):
            if isinstance(n, int) and 1 <= n <= len(t):
                return t[n-1]  # Convert to 0-based indexing
            raise Exception(f"Tuple index {n} out of bounds for tuple of length {len(t)}")
        if n == 1:
            return t
        raise Exception(f"Cannot access index {n} of non-tuple value")
    
    # Add these functions to the environment
    env.set('Order', order)
    
    # Special handler for tuple elements
    # In RPAL, if T is a tuple, T N means "get the Nth element of T"
    # We need to make this happen via the evaluator
    env.set('_tuple_access', tuple_access)

    # Add Sum function that can work with the tuple format in sum.rpal
    def sum_function(tuple_arg):
        # For sum.rpal, the sum function expects a tuple
        if not isinstance(tuple_arg, tuple):
            tuple_arg = (tuple_arg,)
        
        # Sum the elements of the tuple
        result = sum(tuple_arg) if tuple_arg else 0
        return result
    
    env.set('Sum', sum_function)

if __name__ == "__main__":
    main()