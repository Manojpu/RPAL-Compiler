from environment import Environment

class Evaluator:
    def __init__(self, environment):
        self.environment = environment

    def evaluate(self, node):
        if node.type == 'let':
            return self.evaluate_let(node)
        elif node.type == 'lambda':
            return self.evaluate_lambda(node)
        elif node.type == 'function_form':
            return self.evaluate_function_form(node)
        elif node.type == 'ID':
            return self.environment.get(node.value)
        elif node.type == 'INT':
            return int(node.value)
        elif node.type == 'STR':
            return node.value
        elif node.type == 'true':
            return True
        elif node.type == 'false':
            return False
        elif node.type == 'nil':
            return None
        elif node.type == '=':
            return self.evaluate_assignment(node)
        elif node.type in ['+', '-', '*', '/']:
            return self.evaluate_arithmetic(node)
        elif node.type == 'and':
            return self.evaluate_and(node)
        elif node.type == 'or':
            return self.evaluate_or(node)
        elif node.type == 'not':
            return self.evaluate_not(node)
        elif node.type in ['gr', 'ge', 'ls', 'le', 'eq', 'ne']:
            return self.evaluate_comparison(node)
        elif node.type == 'tau':
            return self.evaluate_tuple(node)
        elif node.type == 'where':
            return self.evaluate_where(node)
        elif node.type == 'gamma':
            return self.evaluate_gamma(node)
        else:
            raise Exception(f"Unknown node type: {node.type}")

    def evaluate_let(self, node):
        # let <definitions> in <expression>
        if len(node.children) != 2:
            raise Exception("Invalid 'let' expression: Expected 2 children")
        
        definitions = node.children[0]
        expression = node.children[1]
        
        # Create a new environment for the let scope
        new_env = Environment(self.environment)
        
        # Process definitions
        if definitions.type == '=':
            # Simple definition: let x = e in ...
            var_name = definitions.children[0].value
            var_value = self.evaluate(definitions.children[1])
            new_env.set(var_name, var_value)
        elif definitions.type == 'function_form':
            # Function definition: let f(x) = e in ...
            self.process_function_definition(definitions, new_env)
        else:
            # Other definition types
            raise Exception(f"Unsupported definition type: {definitions.type}")
        
        # Evaluate the expression in the new environment
        old_env = self.environment
        self.environment = new_env
        result = self.evaluate(expression)
        self.environment = old_env
        
        return result

    def evaluate_where(self, node):
        # e where <definitions>
        if len(node.children) != 2:
            raise Exception("Invalid 'where' expression: Expected 2 children")
        
        expression = node.children[0]
        definitions = node.children[1]
        
        # Create a new environment for the where scope
        new_env = Environment(self.environment)
        
        # Process definitions
        if definitions.type == '=':
            # Simple definition: e where x = e
            var_name = definitions.children[0].value
            var_value = self.evaluate(definitions.children[1])
            new_env.set(var_name, var_value)
        elif definitions.type == 'function_form':
            # Function definition: e where f(x) = e
            self.process_function_definition(definitions, new_env)
        elif definitions.type == 'rec':
            # Recursive definition: e where rec f(x) = e
            self.process_recursive_definition(definitions.children[0], new_env)
        else:
            # Other definition types
            raise Exception(f"Unsupported definition type in where: {definitions.type}")
        
        # Evaluate the expression in the new environment
        old_env = self.environment
        self.environment = new_env
        result = self.evaluate(expression)
        self.environment = old_env
        
        return result

    def process_function_definition(self, node, env):
        if node.type != 'function_form':
            raise Exception("Expected function form")
        
        func_name = node.children[0].value
        params = [child.value for child in node.children[1:-1]]
        body = node.children[-1]
        
        # Create a closure
        def function(*args):
            if len(args) != len(params):
                raise Exception(f"Function {func_name} expects {len(params)} arguments, got {len(args)}")
            
            # Create a new environment with parameter bindings
            func_env = Environment(env)
            for param, arg in zip(params, args):
                func_env.set(param, arg)
            
            # Evaluate the function body in this environment
            old_env = self.environment
            self.environment = func_env
            result = self.evaluate(body)
            self.environment = old_env
            
            return result
        
        env.set(func_name, function)

    def process_recursive_definition(self, node, env):
        # Simplified recursive function definition handling
        if node.type == 'function_form':
            func_name = node.children[0].value
            params = [child.value for child in node.children[1:-1]]
            body = node.children[-1]
            
            # Create a placeholder function that will be updated after definition
            def recursive_function(*args):
                # The actual function will be set in the environment later
                return env.get(func_name)(*args)
            
            # Set the placeholder in the environment
            env.set(func_name, recursive_function)
            
            # Now define the actual function
            self.process_function_definition(node, env)
        else:
            # Handle other recursive definition types
            raise Exception(f"Unsupported recursive definition type: {node.type}")

    def evaluate_arithmetic(self, node):
        if len(node.children) != 2:
            raise Exception(f"Invalid arithmetic expression: Expected 2 children for {node.type}")
        
        left = self.evaluate(node.children[0])
        right = self.evaluate(node.children[1])
        
        if node.type == '+':
            return left + right
        elif node.type == '-':
            return left - right
        elif node.type == '*':
            return left * right
        elif node.type == '/':
            if right == 0:
                raise Exception("Division by zero")
            return left / right
        else:
            raise Exception(f"Unknown arithmetic operator: {node.type}")

    def evaluate_comparison(self, node):
        if len(node.children) != 2:
            raise Exception(f"Invalid comparison expression: Expected 2 children for {node.type}")
        
        left = self.evaluate(node.children[0])
        right = self.evaluate(node.children[1])
        
        if node.type == 'eq':
            return left == right
        elif node.type == 'ne':
            return left != right
        elif node.type == 'gr' or node.type == 'gt':
            return left > right
        elif node.type == 'ge':
            return left >= right
        elif node.type == 'ls' or node.type == 'lt':
            return left < right
        elif node.type == 'le':
            return left <= right
        else:
            raise Exception(f"Unknown comparison operator: {node.type}")

    def evaluate_gamma(self, node):
        # Function application (gamma node)
        if len(node.children) != 2:
            raise Exception("Invalid function application: Expected 2 children")
        
        # Evaluate the function and argument
        function_node = node.children[0]
        argument_node = node.children[1]
        
        # Handle the special case where a tuple is followed by an integer
        # This implements the T N syntax in RPAL for accessing tuple elements
        if function_node.type == 'ID' and function_node.value == 'Sum':
            # Special case for Sum function - Sum expects a tuple
            argument = self.evaluate(argument_node)
            function = self.environment.get('Sum')
            
            # Make sure argument is a tuple
            if not isinstance(argument, tuple):
                argument = (argument,)
                
            return function(argument)
        
        function = self.evaluate(function_node)
        argument = self.evaluate(argument_node)
        
        # Handle tuple access: if function is a tuple and argument is an integer,
        # access the tuple element instead of calling the tuple as a function
        if isinstance(function, tuple) and isinstance(argument, int):
            return self.environment.get('_tuple_access')(function, argument)
        
        # Normal function application
        if callable(function):
            # If the argument is a tuple, unpack it for the function call
            # But not for all functions - respect the function's expected signature
            if isinstance(argument, tuple) and function.__name__ != 'lambda_function':
                return function(*argument)
            else:
                return function(argument)
        else:
            raise Exception(f"Cannot apply non-function value: {function}")

    def evaluate_tuple(self, node):
        # Create a tuple from the children nodes
        values = []
        for child in node.children:
            values.append(self.evaluate(child))
        return tuple(values)

    def evaluate_lambda(self, node):
        # Lambda expression: fn x.e
        if len(node.children) < 2:
            raise Exception("Invalid lambda expression")
        
        param_node = node.children[0]
        body_node = node.children[-1]
        
        # Create a closure that captures the current environment
        def lambda_function(arg):
            # Create a new environment with the parameter bound to arg
            new_env = Environment(self.environment)
            new_env.set(param_node.value, arg)
            
            # Evaluate the body in the new environment
            old_env = self.environment
            self.environment = new_env
            result = self.evaluate(body_node)
            self.environment = old_env
            
            return result
        
        return lambda_function

    def evaluate_function_form(self, node):
        # Function form: ID(x1, x2, ...) = e
        if len(node.children) < 2:
            raise Exception("Invalid function form")
        
        func_name = node.children[0].value
        params = [child.value for child in node.children[1:-1]]
        body = node.children[-1]
        
        # Create a function that captures the current environment
        def function(*args):
            if len(args) != len(params):
                raise Exception(f"Function {func_name} expects {len(params)} arguments, got {len(args)}")
            
            # Create a new environment with parameters bound to arguments
            new_env = Environment(self.environment)
            for param, arg in zip(params, args):
                new_env.set(param, arg)
            
            # Evaluate the body in the new environment
            old_env = self.environment
            self.environment = new_env
            result = self.evaluate(body)
            self.environment = old_env
            
            return result
        
        # Add the function to the environment
        self.environment.set(func_name, function)
        
        return function

    def evaluate_assignment(self, node):
        # Assignment: x = e
        if len(node.children) != 2:
            raise Exception("Invalid assignment expression")
        
        left = node.children[0]
        right = self.evaluate(node.children[1])
        
        if left.type == 'ID':
            self.environment.set(left.value, right)
        else:
            raise Exception(f"Cannot assign to {left.type}")
        
        return right

    def evaluate_and(self, node):
        # Logical AND: e1 & e2
        if len(node.children) != 2:
            raise Exception("Invalid AND expression")
        
        left = self.evaluate(node.children[0])
        # Short-circuit evaluation
        if not left:
            return False
        
        right = self.evaluate(node.children[1])
        return right

    def evaluate_or(self, node):
        # Logical OR: e1 or e2
        if len(node.children) != 2:
            raise Exception("Invalid OR expression")
        
        left = self.evaluate(node.children[0])
        # Short-circuit evaluation
        if left:
            return left
        
        right = self.evaluate(node.children[1])
        return right

    def evaluate_not(self, node):
        # Logical NOT: not e
        if len(node.children) != 1:
            raise Exception("Invalid NOT expression")
        
        value = self.evaluate(node.children[0])
        return not value