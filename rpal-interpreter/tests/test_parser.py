import unittest
from src.lexer import tokenize_file
from src.parser import Parser
from src.ast import ASTNode

class TestParser(unittest.TestCase):
    def setUp(self):
        self.valid_input = "let Sum(A) = Psum(A, Order A) where rec Psum(T, N) = N eq 0 -> 0 | Psum(T, N-1) + T N in Print(Sum(1, 2, 3, 4, 5))"
        self.tokens = tokenize_file("input.txt")
        self.parser = Parser(self.tokens)

    def test_parse_let_expression(self):
        ast = self.parser.parse()
        self.assertIsInstance(ast, ASTNode)
        self.assertEqual(ast.type, 'let')

    def test_parse_function_definition(self):
        ast = self.parser.parse()
        function_node = ast.children[0]  # Assuming the first child is the function definition
        self.assertEqual(function_node.type, 'function_form')

    def test_parse_where_clause(self):
        ast = self.parser.parse()
        where_node = ast.children[1]  # Assuming the second child is the where clause
        self.assertEqual(where_node.type, 'where')

    def test_parse_expression_with_parameters(self):
        ast = self.parser.parse()
        sum_node = ast.children[0]  # Assuming the first child is the function definition
        param_node = sum_node.children[0]  # Assuming the first child is the parameter
        self.assertEqual(param_node.type, 'ID')
        self.assertEqual(param_node.value, 'A')

    def test_invalid_input(self):
        invalid_input = "let Sum(A) = Psum(A, Order A) where rec Psum(T, N) = N eq 0 -> 0 | Psum(T, N-1) + T N in Print(Sum(1, 2, 3, 4, 5"
        self.parser = Parser(tokenize_file("invalid_input.txt"))
        with self.assertRaises(Exception):
            self.parser.parse()

if __name__ == '__main__':
    unittest.main()