# RPAL Interpreter

## Overview
The RPAL interpreter is a project designed to interpret and execute programs written in the RPAL programming language. It includes a lexer for tokenizing input, a parser for constructing an abstract syntax tree (AST), and an evaluator for executing the AST. The interpreter supports various constructs of the RPAL language, including function definitions, conditionals, and arithmetic operations.

## Project Structure
```
rpal-interpreter
├── src
│   ├── lexer.py               # Lexical analyzer for tokenizing input text
│   ├── parser.py              # Parser for constructing the AST from tokens
│   ├── ast.py                 # Defines the ASTNode class for the AST
│   ├── st_generator.py        # Generates a symbol table from the AST
│   ├── cse_machine.py         # Implements the CSE machine for executing the AST
│   ├── environment.py         # Manages the execution environment and variable bindings
│   ├── evaluator.py           # Evaluates the AST and handles function calls
│   ├── utils.py               # Utility functions for error handling and type checking
│   └── main.py                # Entry point for the interpreter
├── tests
│   ├── test_lexer.py          # Unit tests for the lexer
│   ├── test_parser.py         # Unit tests for the parser
│   ├── test_st_generator.py    # Unit tests for the symbol table generator
│   ├── test_cse_machine.py    # Unit tests for the CSE machine
│   └── test_evaluator.py      # Unit tests for the evaluator
├── examples
│   ├── factorial.rpal         # Example RPAL program for calculating factorial
│   ├── fibonacci.rpal         # Example RPAL program for calculating Fibonacci numbers
│   └── sum.rpal               # Example RPAL program for summing a list of numbers
├── requirements.txt           # Lists dependencies required for the project
├── setup.py                   # Setup script for the project
└── README.md                  # Documentation for the project
```

## Installation
To install the RPAL interpreter, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd rpal-interpreter
pip install -r requirements.txt
```

## Usage
To run the RPAL interpreter, use the following command:

```bash
python src/main.py <input_file.rpal>
```

Replace `<input_file.rpal>` with the path to your RPAL program.

## Examples
The `examples` directory contains several example RPAL programs that demonstrate the capabilities of the interpreter. You can run these examples to see how the interpreter processes different RPAL constructs.

## Testing
To run the unit tests for the RPAL interpreter, use the following command:

```bash
pytest tests/
```

This will execute all the tests in the `tests` directory and report any failures.

## Contributing
Contributions to the RPAL interpreter are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.