import unittest
from src.lexer import tokenize_file

class TestLexer(unittest.TestCase):
    
    def test_tokenize_simple_expression(self):
        input_text = "let x = 5 in x + 1"
        tokens = tokenize_file(input_text)
        expected_tokens = [
            ('let', None),
            ('ID', 'x'),
            ('=', None),
            ('INT', 5),
            ('in', None),
            ('ID', 'x'),
            ('+', None),
            ('INT', 1),
            ('EOF', None)
        ]
        self.assertEqual([(token.type, token.value) for token in tokens], expected_tokens)

    def test_tokenize_function_definition(self):
        input_text = "let f(x) = x + 1 in f(2)"
        tokens = tokenize_file(input_text)
        expected_tokens = [
            ('let', None),
            ('ID', 'f'),
            ('(', None),
            ('ID', 'x'),
            (')', None),
            ('=', None),
            ('ID', 'x'),
            ('+', None),
            ('INT', 1),
            ('in', None),
            ('ID', 'f'),
            ('(', None),
            ('INT', 2),
            (')', None),
            ('EOF', None)
        ]
        self.assertEqual([(token.type, token.value) for token in tokens], expected_tokens)

    def test_tokenize_with_comments(self):
        input_text = "let x = 5 // this is a comment\nin x + 1"
        tokens = tokenize_file(input_text)
        expected_tokens = [
            ('let', None),
            ('ID', 'x'),
            ('=', None),
            ('INT', 5),
            ('in', None),
            ('ID', 'x'),
            ('+', None),
            ('INT', 1),
            ('EOF', None)
        ]
        self.assertEqual([(token.type, token.value) for token in tokens], expected_tokens)

    def test_tokenize_multiline_comment(self):
        input_text = "let x = 5 /* this is a\nmultiline comment */ in x + 1"
        tokens = tokenize_file(input_text)
        expected_tokens = [
            ('let', None),
            ('ID', 'x'),
            ('=', None),
            ('INT', 5),
            ('in', None),
            ('ID', 'x'),
            ('+', None),
            ('INT', 1),
            ('EOF', None)
        ]
        self.assertEqual([(token.type, token.value) for token in tokens], expected_tokens)

if __name__ == '__main__':
    unittest.main()