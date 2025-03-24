from typing import Any
from enum import Enum

from .more_itertools import peekable

from .ast_node import *
from .tokenizer import Token, TokenType

TokenIterator = peekable
# `ParserFunc` is alias to `function(TokenIterator) -> AstNode`.
ParserFunc = Any

class AstParserErrorKind(Enum):
    UNEXPECTED_END = 0
    INVALID_TOKEN = 1
    UNEXPECTED_TOKEN = 2

class AstParserError(BaseException):
    def __init__(self, kind: AstParserErrorKind, *args) -> None:
        self._kind = kind

        match kind:
            case AstParserErrorKind.INVALID_TOKEN:
                # args = (invalid_token,)
                self._invalid_token: Token = args[0]
                self._valid_token_types: list[TokenType] = args[1]
            case AstParserErrorKind.UNEXPECTED_TOKEN:
                self._unexpected_token: Token = args[0]

    def stringify_with(self, expr: str) -> str:
        match self.kind:
            case AstParserErrorKind.UNEXPECTED_END:
                return "unexpected end"
            case AstParserErrorKind.INVALID_TOKEN:
                valid_token_type_joint = self._valid_token_types[0].name
                if len(self._valid_token_types) > 1:
                    for valid_token_type in self._valid_token_types[1:-1]:
                        valid_token_type_joint += f', {valid_token_type.name}'
                    valid_token_type_joint += f' or {self._valid_token_types[-1].name}'

                b1, b2 = self._invalid_token.borders
                return f"invalid operator in {b1} position ('{expr[b1:b2]}'), expected \
{valid_token_type_joint}"

            case AstParserErrorKind.UNEXPECTED_TOKEN:
                b1, b2 = self._unexpected_token.borders
                return f"unexpected token in {b1} position ('{expr[b1:b2]}')"

    @property
    def kind(self) -> AstParserErrorKind:
        return self._kind

# OPERATIONS:
# 1. ->   (INVESTIGATION)
# 2. =    (EQUAL)
# 3. |    (OR)
# 4. &    (AND)
# 5. не   (NOT)
# 6. (...) / variable

def parse_ast(tokens: list[Token]) -> AstNode:
    result: AstNode = l1(peekable(tokens))
    return result

def l1(tokens: TokenIterator) -> AstNode:
    result = _invest_parser(tokens, l2)

    return result

def l2(tokens: TokenIterator) -> AstNode:
    return _equal_parser(tokens, l3)

def l3(tokens: TokenIterator) -> AstNode:
    return _or_parser(tokens, l4)

def l4(tokens: TokenIterator) -> AstNode:
    return _and_parser(tokens, l5)

def l5(tokens: TokenIterator) -> AstNode:
    return _not_parser(tokens, l6)

def l6(tokens: TokenIterator) -> AstNode:
    return _var_parser(tokens, l1)

def _equal_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    val: AstNode = next_level(tokens)

    try:
        while True:
            peeked = tokens.peek()
            match peeked.token_type:
                case TokenType.EQUAL_SIGN:
                    next(tokens)
                    n = next_level(tokens)
                    val = EQUALNode(val, n, (val.borders[0], n.borders[1]))
                case TokenType.XOR_SIGN:
                    next(tokens)
                    n = next_level(tokens)
                    val = XORNode(val, n, (val.borders[0], n.borders[1]))
                case _:
                    break
    except StopIteration:
        pass

    return val

def _invest_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    val: AstNode = next_level(tokens)

    try:
        while tokens.peek().token_type == TokenType.INVESTIGATION_SIGN:
            next(tokens)
            n: AstNode = next_level(tokens)
            val = INVESTNode(val, n, (val.borders[0], n.borders[1]))
    except StopIteration:
        pass

    return val

def _or_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    val = next_level(tokens)

    try:
        while tokens.peek().token_type == TokenType.OR_SIGN:
            next(tokens)
            n: AstNode = next_level(tokens)
            val = ORNode(val, n, (val.borders[0], n.borders[1]))
    except StopIteration:
        pass

    return val

def _and_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    val = next_level(tokens)

    try:
        while tokens.peek().token_type == TokenType.AND_SIGN:
            next(tokens)
            n: AstNode = next_level(tokens)
            val = ANDNode(val, n, (val.borders[0], n.borders[1]))
    except StopIteration:
        pass

    return val

def _not_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    try:
        if tokens.peek().token_type == TokenType.NOT_SIGN:
            next(tokens)
            n: AstNode = next_level(tokens)
            return NOTNode(n, (n.borders[0] - 1, n.borders[1]))
        else:
            return next_level(tokens)
    except StopIteration:
        raise AstParserError(AstParserErrorKind.UNEXPECTED_END)

def _var_parser(tokens: TokenIterator, next_level: ParserFunc) -> AstNode:
    try:
        token = next(tokens)
        if token.token_type == TokenType.VARIABLE:
            return VARNode(token.name, token.borders)
        elif token.token_type == TokenType.LEFT_PAREN:
            val = next_level(tokens)

            if (unexpected_token := next(tokens)).token_type != TokenType.RIGHT_PAREN:
                expected_token_type = TokenType.RIGHT_PAREN
                raise AstParserError(
                    AstParserErrorKind.INVALID_TOKEN,
                    unexpected_token, [expected_token_type]
                )

            return val
        else:
            raise AstParserError(
                AstParserErrorKind.INVALID_TOKEN,
                token,
                [TokenType.LEFT_PAREN, TokenType.VARIABLE]
            )
    except StopIteration:
        raise AstParserError(AstParserErrorKind.UNEXPECTED_END)
