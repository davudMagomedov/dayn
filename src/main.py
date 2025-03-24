from itertools import product

from .tokenizer import tokenize_string, Token, TokenType, TokenizerError
from .ast_node import *
from .ast_parser import parse_ast, AstParserError
from .more_itertools import filter_map

def variables_in_tokens(tokens: list[Token]) -> list[str]:
    return list(set(filter_map(
        lambda token: token.name if token.token_type == TokenType.VARIABLE else None,
        tokens
    )))

def make_tables(variables: list[str]) -> list[dict[str, bit]]:
    return list(map(
        lambda bits: dict(zip(variables, bits)),
        product([0, 1], repeat = len(variables))
    ))

def make_line(variables: list[str], table: dict[str, bit], result: bit) -> str:
    return ' '.join(map(lambda variable: str(table[variable]), variables)) + f' {result}'

def print_tables(tables: list[dict[str, bit]], variables: list[str], ast_expression: AstNode):
    print(' '.join(variables) + ' RESULT')

    for table in tables:
        result = ast_expression.calculate(table)
        print(make_line(variables, table, result))

def run_shell():
    PROMPT: str = "#> "

    while True:
        try:
            content: str = input(PROMPT)
            try:
                tokens = tokenize_string(content)
            except TokenizerError as e:
                print(f"error: {e}"); continue
            variables = sorted(variables_in_tokens(tokens))
            try:
                ast_expression = parse_ast(tokens)
            except AstParserError as e:
                print(f"syntax error: {e.stringify_with(content)}"); continue

            tables = make_tables(variables)

            print_tables(tables, variables, ast_expression)
        except KeyboardInterrupt:
            break

def main():
    run_shell()

if __name__ == "__main__":
    main()
