class ASTNode:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []
        self.no_of_children = 0  # Initialize number of children
    
    def add_child(self, node):
        self.children.append(node)
        self.no_of_children += 1  # Increment child count
        return node
    
    def print_ast(self, prefix=""):
        if self.value is not None:
            print(f"{prefix}{self.type}:{self.value}")
        else:
            print(f"{prefix}{self.type}")
        for child in self.children:
            child.print_ast(prefix + ".")
    
    def __str__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return self.type

class Parser:
    def __init__(self, tokens):
        if not tokens:
            raise Exception("No tokens provided to parser. Check your input file or lexer.")
        self.tokens = tokens
        self.ast = []
        self.string_ast = []
        self.current_token_index = 0
        self.current_token = self.tokens[0]
    
    def error(self, expected=None):
        token = self.current_token
        if expected:
            raise Exception(f"Expected {expected}, got {token} at line {token.line}, column {token.column}")
        else:
            raise Exception(f"Unexpected token {token} at line {token.line}, column {token.column}")
    
    def consume(self, expected_type=None):
        if expected_type and (not self.current_token or self.current_token.type != expected_type):
            self.error(expected_type)
        if self.current_token_index < len(self.tokens) - 1:
            self.current_token_index += 1
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None
    

    def parse_e(self):
        if self.current_token and self.current_token.type == 'let':
            node = ASTNode('let')
            self.consume('let')
            d_node = self.parse_d()
            node.add_child(d_node)
            if not self.current_token or self.current_token.type != 'in':
                self.error('in')
            self.consume('in')
            e_node = self.parse_e()
            node.add_child(e_node)
            return node
        elif self.current_token and self.current_token.type == 'fn':
            node = ASTNode('lambda')
            self.consume('fn')
            while self.current_token and self.current_token.type != '.':
                vb_node = self.parse_vb()
                node.add_child(vb_node)
                if not self.current_token:
                    self.error('.')
            self.consume('.')
            body_node = self.parse_e()
            node.add_child(body_node)
            return node
        else:
            return self.parse_ew()
    
    def parse_ew(self):
        t_node = self.parse_t()
        if self.current_token and self.current_token.type == 'where':
            where_node = ASTNode('where')
            self.consume('where')
            where_node.add_child(t_node)
            where_node.add_child(self.parse_dr())
            return where_node
        return t_node
    
    def parse_t(self):
        left = self.parse_ta()
        while self.current_token and self.current_token.type == ',':
            tau_node = ASTNode('tau')
            self.consume(',')
            tau_node.add_child(left)
            tau_node.add_child(self.parse_ta())
            left = tau_node
        return left
    
    def parse_ta(self):
        left = self.parse_tc()
        while self.current_token and self.current_token.type == '->':
            arrow_node = ASTNode('->')
            self.consume('->')
            then_branch = self.parse_tc()
            arrow_node.add_child(left)
            arrow_node.add_child(then_branch)
            if self.current_token and self.current_token.type == '|':
                self.consume('|')
                else_branch = self.parse_tc()
                arrow_node.add_child(else_branch)
            left = arrow_node
        return left
    
    def parse_tc(self):
        left = self.parse_b()
        while self.current_token and self.current_token.type == '&':
            and_node = ASTNode('and')
            self.consume('&')
            and_node.add_child(left)
            and_node.add_child(self.parse_b())
            left = and_node
        return left
    
    def parse_b(self):
        left = self.parse_bt()
        while self.current_token and self.current_token.type == 'or':
            or_node = ASTNode('or')
            self.consume('or')
            or_node.add_child(left)
            or_node.add_child(self.parse_bt())
            left = or_node
        return left
    
    def parse_bt(self):
        left = self.parse_bs()
        if self.current_token and self.current_token.type == 'not':
            not_node = ASTNode('not')
            self.consume('not')
            not_node.add_child(left)
            not_node.add_child(self.parse_bs())
            return not_node
        return left
    
    def parse_bs(self):
        left = self.parse_a()
        comparison_ops = {
            'gr': 'gr', '>': 'gr',
            'ge': 'ge', '>=': 'ge',
            'ls': 'ls', '<': 'ls',
            'le': 'le', '<=': 'le',
            'eq': 'eq', '=': 'eq',
            'ne': 'ne', '!=': 'ne'
        }
        if self.current_token and self.current_token.type in comparison_ops:
            op_type = comparison_ops[self.current_token.type]
            op_node = ASTNode(op_type)
            self.consume(self.current_token.type)
            op_node.add_child(left)
            op_node.add_child(self.parse_a())
            return op_node
        return left
    
    def parse_a(self):
        left = self.parse_at()
        while self.current_token and self.current_token.type in ['+', '-']:
            op_type = self.current_token.type
            op_node = ASTNode(op_type)
            self.consume(op_type)
            op_node.add_child(left)
            op_node.add_child(self.parse_at())
            left = op_node
        return left
    
    def parse_at(self):
        left = self.parse_af()
        while self.current_token and self.current_token.type in ['*', '/']:
            op_type = self.current_token.type
            op_node = ASTNode(op_type)
            self.consume(op_type)
            op_node.add_child(left)
            op_node.add_child(self.parse_af())
            left = op_node
        return left
    
    def parse_af(self):
        left = self.parse_ap()
        if self.current_token and self.current_token.type == '@':
            at_node = ASTNode('@')
            self.consume('@')
            at_node.add_child(left)
            at_node.add_child(self.parse_ap())
            return at_node
        return left
    
    def parse_ap(self):
        left = self.parse_r()
        if self.current_token and self._is_r_start():
            gamma_node = ASTNode('gamma')
            gamma_node.add_child(left)
            gamma_node.add_child(self.parse_r())
            return gamma_node
        return left
    def convert_ast_to_string_ast(self):
        dots = ""
        stack = []

        while self.ast:
            if not stack:
                if self.ast[-1].no_of_children == 0:
                    self.add_strings(dots, self.ast.pop())
                else:
                    node = self.ast.pop()
                    stack.append(node)
            else:
                if self.ast[-1].no_of_children > 0:
                    node = self.ast.pop()
                    stack.append(node)
                    dots += "."
                else:
                    stack.append(self.ast.pop())
                    dots += "."
                    while stack[-1].no_of_children == 0:
                        self.add_strings(dots, stack.pop())
                        if not stack:
                            break
                        dots = dots[:-1]
                        node = stack.pop()
                        node.no_of_children -= 1
                        stack.append(node)

        # Reverse the list
        self.string_ast.reverse()
        return self.string_ast
    
    def _is_r_start(self):
        if not self.current_token:
            return False
        return self.current_token.type in ['(', 'ID', 'INT', 'STR', 'true', 'false', 'nil', 'dummy']
    
    def parse_r(self):
        if self.current_token and self.current_token.type == '(':
            self.consume('(')
            expr = self.parse_e()
            if self.current_token and self.current_token.type == ',':
                tuple_node = ASTNode('tau')
                tuple_node.add_child(expr)
                while self.current_token and self.current_token.type == ',':
                    self.consume(',')
                    tuple_node.add_child(self.parse_e())
                if not self.current_token or self.current_token.type != ')':
                    self.error(')')
                self.consume(')')
                return tuple_node
            if not self.current_token or self.current_token.type != ')':
                self.error(')')
            self.consume(')')
            return expr
        elif self.current_token and self.current_token.type == 'true':
            node = ASTNode('true')
            self.consume('true')
            return node
        elif self.current_token and self.current_token.type == 'false':
            node = ASTNode('false')
            self.consume('false')
            return node
        elif self.current_token and self.current_token.type == 'nil':
            node = ASTNode('nil')
            self.consume('nil')
            return node
        elif self.current_token and self.current_token.type == 'dummy':
            node = ASTNode('dummy')
            self.consume('dummy')
            return node
        elif self.current_token and self.current_token.type == 'INT':
            node = ASTNode('INT', self.current_token.value)
            self.consume('INT')
            return node
        elif self.current_token and self.current_token.type == 'STR':
            node = ASTNode('STR', self.current_token.value)
            self.consume('STR')
            return node
        elif self.current_token and self.current_token.type == 'ID':
            node = ASTNode('ID', self.current_token.value)
            self.consume('ID')
            return node
        else:
            self.error("R expression")
    
    def parse_d(self):
        left = self.parse_da()
        while self.current_token and self.current_token.type == 'and':
            and_node = ASTNode('and')
            self.consume('and')
            and_node.add_child(left)
            and_node.add_child(self.parse_da())
            left = and_node
        return left
    
    def parse_da(self):
        if self.current_token and self.current_token.type == 'rec':
            rec_node = ASTNode('rec')
            self.consume('rec')
            rec_node.add_child(self.parse_dr())
            return rec_node
        return self.parse_dr()
    
    def parse_dr(self):
        if self.current_token and self.current_token.type == 'let':
            let_node = ASTNode('let')
            self.consume('let')
            let_node.add_child(self.parse_d())
            if not self.current_token or self.current_token.type != 'in':
                self.error('in')
            self.consume('in')
            let_node.add_child(self.parse_dr())
            return let_node
        return self.parse_db()
    
    def parse_db(self):
        if self.current_token and self.current_token.type == '(':
            self.consume('(')
            d_node = self.parse_d()
            if not self.current_token or self.current_token.type != ')':
                self.error(')')
            self.consume(')')
            return d_node
        elif (self.current_token and self.current_token.type == 'ID' and 
              self.current_token_index + 1 < len(self.tokens) and 
              self.tokens[self.current_token_index + 1].type == '('):
            func_name = ASTNode('ID', self.current_token.value)
            self.consume('ID')
            self.consume('(')
            params = []
            if self.current_token and self.current_token.type != ')':
                params.append(self.parse_vb())
                while self.current_token and self.current_token.type == ',':
                    self.consume(',')
                    params.append(self.parse_vb())
            if not self.current_token or self.current_token.type != ')':
                self.error(')')
            self.consume(')')
            if not self.current_token or self.current_token.type != '=':
                self.error('=')
            self.consume('=')
            body = self.parse_e()
            func_form = ASTNode('function_form')
            func_form.add_child(func_name)
            for param in params:
                func_form.add_child(param)
            func_form.add_child(body)
            return func_form
        elif self.current_token and self.current_token.type == 'rec':
            return self.parse_da()
        else:
            vl_node = self.parse_vl()
            if not self.current_token or self.current_token.type != '=':
                self.error('=')
            self.consume('=')
            equals_node = ASTNode('=')
            equals_node.add_child(vl_node)
            equals_node.add_child(self.parse_e())
            return equals_node
    
    def parse_vl(self):
        if self.current_token and self.current_token.type == 'ID':
            id_node = ASTNode('ID', self.current_token.value)
            self.consume('ID')
            return id_node
        elif self.current_token and self.current_token.type == '(':
            self.consume('(')
            vl_node = self.parse_vl()
            if not self.current_token or self.current_token.type != ')':
                self.error(')')
            self.consume(')')
            return vl_node
        else:
            self.error('ID or (')
    
    def parse_vb(self):
        if self.current_token and self.current_token.type == 'ID':
            id_node = ASTNode('ID', self.current_token.value)
            self.consume('ID')
            return id_node
        elif self.current_token and self.current_token.type == '(':
            self.consume('(')
            vb_node = self.parse_vb()
            if not self.current_token or self.current_token.type != ')':
                self.error(')')
            self.consume(')')
            return vb_node
        else:
            self.error('ID or (')
    
    def parse(self):
        ast = self.parse_e()
        if self.current_token and self.current_token.type != 'EOF':
            self.error("end of input")
        return ast

def parse_file(filename):
    from lexer import tokenize_file
    tokens = tokenize_file(filename)
    parser = Parser(tokens)
    return parser.parse()