from typing import Mapping
from abc import ABC, abstractmethod

bit = int;

class AstNode(ABC):
    __slots__ = ("_borders",)

    def __init__(self, borders: tuple[int, int]):
        self._borders = borders

    @abstractmethod
    def calculate(
        self,
        symbols: Mapping[str, bit]
    ) -> bit: pass

    @property
    def borders(self) -> tuple[int, int]:
        return self._borders

class ORNode(AstNode):
    __slots__ = ("_a1", "_a2")

    def __init__(self, a1: AstNode, a2: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a1, self._a2 = a1, a2

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return self._a1.calculate(symbols) | self._a2.calculate(symbols)

class XORNode(AstNode):
    __slots__ = ("_a1", "_a2")

    def __init__(self, a1: AstNode, a2: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a1, self._a2 = a1, a2

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return int(self._a1.calculate(symbols) != self._a2.calculate(symbols))

class ANDNode(AstNode):
    __slots__ = ("_a1", "_a2")

    def __init__(self, a1: AstNode, a2: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a1, self._a2 = a1, a2

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return self._a1.calculate(symbols) & self._a2.calculate(symbols)

class INVESTNode(AstNode):
    __slots__ = ("_a1", "_a2")

    def __init__(self, a1: AstNode, a2: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a1, self._a2 = a1, a2

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return int(self._a1.calculate(symbols) <= self._a2.calculate(symbols))

class EQUALNode(AstNode):
    __slots__ = ("_a1", "_a2")

    def __init__(self, a1: AstNode, a2: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a1, self._a2 = a1, a2

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return int(self._a1.calculate(symbols) == self._a2.calculate(symbols))

class NOTNode(AstNode):
    __slots__ = ("_a",)

    def __init__(self, a: AstNode, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._a = a

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return int(self._a.calculate(symbols) == 0)

class VARNode(AstNode):
    __slots__ = ("_varname",)

    def __init__(self, varname: str, borders: tuple[int, int]) -> None:
        super().__init__(borders)
        self._varname = varname

    def calculate(self, symbols: Mapping[str, bit]) -> bit:
        return symbols[self._varname]
