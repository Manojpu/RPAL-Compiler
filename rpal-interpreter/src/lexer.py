class Token:
    def __init__(self, type, value=None, line=0, column=0):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return self.type

class LexicalAnalyzer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.current_char = None
        self.advance()
    
    def advance(self):
        if self.position < len(self.input_text):
            self.current_char = self.input_text[self.position]
            self.position += 1
            self.column += 1
        else:
            self.current_char = None
    
    def peek(self, n=1):
        peek_pos = self.position + n - 1
        if peek_pos < len(self.input_text):
            return self.input_text[peek_pos]
        return None
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            self.advance()
    
    def skip_comment(self):
        while self.current_char and self.current_char != '\n':
            self.advance()
    
    def handle_multi_line_comment(self):
        while self.current_char:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()
                self.advance()
                return
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
            self.advance()
        raise Exception("Unclosed multi-line comment")
    
    def read_identifier(self):
        start_column = self.column
        id_str = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        keywords = {
            'let': 'let', 'in': 'in', 'fn': 'fn', 'where': 'where',
            'aug': 'aug', 'or': 'or', 'not': 'not', 'gr': 'gr',
            'ge': 'ge', 'ls': 'ls', 'le': 'le', 'eq': 'eq',
            'ne': 'ne', 'true': 'true', 'false': 'false',
            'nil': 'nil', 'dummy': 'dummy', 'rec': 'rec',
            'within': 'within', 'and': 'and'
        }
        if id_str in keywords:
            return Token(keywords[id_str], None, self.line, start_column)
        else:
            return Token('ID', id_str, self.line, start_column)
    
    def read_integer(self):
        start_column = self.column
        num_str = ''
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token('INT', int(num_str), self.line, start_column)
    
    def read_string(self):
        start_column = self.column
        self.advance()
        string_value = ''
        while self.current_char and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                elif self.current_char == '\\':
                    string_value += '\\'
                elif self.current_char == '"':
                    string_value += '"'
                else:
                    string_value += self.current_char
            else:
                string_value += self.current_char
            self.advance()
        if self.current_char != '"':
            raise Exception(f"Unclosed string literal at line {self.line}, column {start_column}")
        self.advance()
        return Token('STR', string_value, self.line, start_column)
    
    def tokenize(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '/' and self.peek() == '/':
                self.advance()
                self.advance()
                self.skip_comment()
                continue
            if self.current_char == '/' and self.peek() == '*':
                self.advance()
                self.advance()
                self.handle_multi_line_comment()
                continue
            if self.current_char.isalpha() or self.current_char == '_':
                self.tokens.append(self.read_identifier())
                continue
            if self.current_char.isdigit():
                self.tokens.append(self.read_integer())
                continue
            if self.current_char == '"':
                self.tokens.append(self.read_string())
                continue
            if self.current_char == '+':
                self.tokens.append(Token('+', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '-':
                if self.peek() == '>':
                    self.tokens.append(Token('->', None, self.line, self.column))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token('-', None, self.line, self.column))
                    self.advance()
                continue
            if self.current_char == '*':
                self.tokens.append(Token('*', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '/':
                self.tokens.append(Token('/', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '=':
                self.tokens.append(Token('=', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '(':
                self.tokens.append(Token('(', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == ')':
                self.tokens.append(Token(')', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == ';':
                self.tokens.append(Token(';', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == ',':
                self.tokens.append(Token(',', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '.':
                self.tokens.append(Token('.', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == ':':
                self.tokens.append(Token(':', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '&':
                self.tokens.append(Token('&', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '@':
                self.tokens.append(Token('@', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '|':
                self.tokens.append(Token('|', None, self.line, self.column))
                self.advance()
                continue
            if self.current_char == '\\':
                self.tokens.append(Token('\\', None, self.line, self.column))
                self.advance()
                continue
            raise Exception(f"Unknown character '{self.current_char}' at line {self.line}, column {self.column}")
        self.tokens.append(Token('EOF', None, self.line, self.column))
        return self.tokens

def tokenize_file(filename):
    with open(filename, 'r') as file:
        input_text = file.read()
    lexer = LexicalAnalyzer(input_text)
    return lexer.tokenize()