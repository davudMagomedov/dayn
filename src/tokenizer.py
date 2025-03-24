from enum import Enum
from typing import Optional

class TokenizerErrorKind(Enum):
    UNKNOWN_CHARACTER = 0

class TokenizerError(BaseException):
    def __init__(self, kind: TokenizerErrorKind, *args) -> None:
        self._kind = kind

        match kind:
            case TokenizerErrorKind.UNKNOWN_CHARACTER:
                # args = (int,)
                self._unknown_character_position = int(args[0])

    def __str__(self) -> str:
        match self.kind:
            case TokenizerErrorKind.UNKNOWN_CHARACTER:
                return f"unknown character: in {self._unknown_character_position} position"

    @property
    def kind(self) -> TokenizerErrorKind:
        return self._kind

class TokenType(Enum):
    VARIABLE            = 0
    AND_SIGN            = 1
    OR_SIGN             = 2
    NOT_SIGN            = 3
    INVESTIGATION_SIGN  = 4
    EQUAL_SIGN          = 5
    LEFT_PAREN          = 6
    RIGHT_PAREN         = 7
    XOR_SIGN            = 8

class Token:
    __slots__ = ("_token_type", "_name", "_borders")

    def __init__(self, token_type: TokenType, borders: tuple[int, int], *args) -> None:
        self._token_type = token_type
        self._borders = borders

        if token_type == TokenType.VARIABLE:
            # args = (name,)
            self._name = str(args[0])
        else:
            self._name = None

    def __repr__(self) -> str:
        s = f"{self.token_type.name}[{self._borders[0]}:{self._borders[1]}]"
        if self.token_type == TokenType.VARIABLE:
            s += f"('{self._name}')"

        return s

    def __str__(self) -> str:
        s = f"{self.token_type.name}[{self._borders[0]}:{self._borders[1]}]"
        if self.token_type == TokenType.VARIABLE:
            s += f"('{self._name}')"

        return s

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def token_type(self) -> TokenType:
        return self._token_type

    @property
    def borders(self) -> tuple[int, int]:
        return self._borders

def _is_var(char: str) -> bool:
    return char.lower()[0].isalpha()

def tokenize_string(string: str) -> list[Token]:
    tokens: list[Token] = []
    position = 0

    while position < len(string):
        match string[position]:
            case '&' | '*': tokens.append(Token(TokenType.AND_SIGN, (position, position + 1)))
            case '|' | '+': tokens.append(Token(TokenType.OR_SIGN, (position, position + 1)))
            case '^': tokens.append(Token(TokenType.XOR_SIGN, (position, position + 1)))
            case '=' if position + 1 < len(string) and string[position + 1] == '>':
                tokens.append(Token(TokenType.INVESTIGATION_SIGN, (position, position + 2)))
                position += 1
            case '=': tokens.append(Token(TokenType.EQUAL_SIGN, (position, position + 1)))
            case '(': tokens.append(Token(TokenType.LEFT_PAREN, (position, position + 1)))
            case ')': tokens.append(Token(TokenType.RIGHT_PAREN, (position, position + 1)))
            case '~': tokens.append(Token(TokenType.NOT_SIGN, (position, position + 1)))
            case '!': tokens.append(Token(TokenType.NOT_SIGN, (position, position + 1)))
            case '<' if position + 2 < len(string) and string[position:position + 3] == "<->":
                tokens.append(Token(TokenType.EQUAL_SIGN, (position, position + 3)))
                position += 2
            case 'и' if position + 2 < len(string) and string[position:position + 3] == 'или':
                tokens.append(Token(TokenType.OR_SIGN, (position, position + 3)))
                position += 2
            case 'и': tokens.append(Token(TokenType.AND_SIGN, (position, position + 1)))
            case 'н' if position + 1 < len(string) and string[position + 1] == 'е':
                tokens.append(Token(TokenType.NOT_SIGN, (position, position + 2)))
                position += 1
            case '-' if position + 1 < len(string) and string[position + 1] == '>':
                tokens.append(Token(TokenType.INVESTIGATION_SIGN, (position, position + 2)))
                position += 1
            case char if _is_var(char):
                tokens.append(Token(TokenType.VARIABLE, (position, position + 1), char))
            case ' ' | '\n': pass
            case _:
                raise TokenizerError(TokenizerErrorKind.UNKNOWN_CHARACTER, position)

        position += 1

    return tokens
