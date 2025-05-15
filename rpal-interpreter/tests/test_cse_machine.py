import unittest
from src.cse_machine import CSEMachine
from src.parser import Parser
from src.lexer import tokenize_file

class TestCSEMachine(unittest.TestCase):

    def setUp(self):
        self.machine = CSEMachine()

    def test_simple_expression(self):
        tokens = tokenize_file('examples/simple_expression.rpal')
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.machine.execute(ast)
        self.assertEqual(result, expected_result)

    def test_function_definition_and_call(self):
        tokens = tokenize_file('examples/function_definition.rpal')
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.machine.execute(ast)
        self.assertEqual(result, expected_result)

    def test_control_structures(self):
        tokens = tokenize_file('examples/control_structures.rpal')
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.machine.execute(ast)
        self.assertEqual(result, expected_result)

    def test_recursive_function(self):
        tokens = tokenize_file('examples/recursive_function.rpal')
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.machine.execute(ast)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()