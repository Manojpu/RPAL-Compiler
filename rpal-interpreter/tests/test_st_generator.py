import unittest
from src.ast import ASTNode
from src.st_generator import SymbolTableGenerator

class TestSymbolTableGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = SymbolTableGenerator()

    def test_simple_function_declaration(self):
        ast = ASTNode('function_form')
        id_node = ASTNode('ID', 'myFunction')
        param_node = ASTNode('ID', 'x')
        body_node = ASTNode('ID', 'x')
        
        ast.add_child(id_node)
        ast.add_child(param_node)
        ast.add_child(body_node)

        symbol_table = self.generator.generate(ast)
        self.assertIn('myFunction', symbol_table)
        self.assertEqual(symbol_table['myFunction']['params'], ['x'])
        self.assertEqual(symbol_table['myFunction']['body'], body_node)

    def test_variable_declaration(self):
        ast = ASTNode('=')
        id_node = ASTNode('ID', 'myVar')
        value_node = ASTNode('INT', 10)

        ast.add_child(id_node)
        ast.add_child(value_node)

        symbol_table = self.generator.generate(ast)
        self.assertIn('myVar', symbol_table)
        self.assertEqual(symbol_table['myVar']['value'], 10)

    def test_nested_function_declaration(self):
        ast = ASTNode('let')
        func_node = ASTNode('function_form')
        id_node = ASTNode('ID', 'outerFunction')
        param_node = ASTNode('ID', 'y')
        inner_func_node = ASTNode('function_form')
        inner_id_node = ASTNode('ID', 'innerFunction')
        inner_param_node = ASTNode('ID', 'z')
        inner_body_node = ASTNode('ID', 'z')

        func_node.add_child(id_node)
        func_node.add_child(param_node)
        func_node.add_child(ASTNode('ID', 'y'))
        inner_func_node.add_child(inner_id_node)
        inner_func_node.add_child(inner_param_node)
        inner_func_node.add_child(inner_body_node)

        ast.add_child(func_node)
        ast.add_child(inner_func_node)

        symbol_table = self.generator.generate(ast)
        self.assertIn('outerFunction', symbol_table)
        self.assertIn('innerFunction', symbol_table)
        self.assertEqual(symbol_table['outerFunction']['params'], ['y'])
        self.assertEqual(symbol_table['innerFunction']['params'], ['z'])

if __name__ == '__main__':
    unittest.main()