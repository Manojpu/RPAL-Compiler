import unittest
from src.lexer import tokenize_file
from src.parser import parse_file
from src.evaluator import Evaluator

class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()

    def test_simple_expression(self):
        tokens = tokenize_file('examples/simple_expression.rpal')
        ast = parse_file('examples/simple_expression.rpal')
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, expected_value)

    def test_function_call(self):
        tokens = tokenize_file('examples/function_call.rpal')
        ast = parse_file('examples/function_call.rpal')
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, expected_value)

    def test_recursive_function(self):
        tokens = tokenize_file('examples/recursive_function.rpal')
        ast = parse_file('examples/recursive_function.rpal')
        result = self.evaluator.evaluate(ast)
        self.assertEqual(result, expected_value)

    def test_error_handling(self):
        tokens = tokenize_file('examples/error_handling.rpal')
        ast = parse_file('examples/error_handling.rpal')
        with self.assertRaises(Exception):
            self.evaluator.evaluate(ast)

if __name__ == '__main__':
    unittest.main()