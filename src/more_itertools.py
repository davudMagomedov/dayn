from typing import Any, Iterable, Iterator

class peekable():
    __slots__ = ("_iterator", "_nextv")

    def __init__(self, iterable: Iterable) -> None:
        self._iterator: Iterator = iter(iterable)
        self._nextv: Any | None = None

    def __next__(self) -> Any:
        if self._nextv is not None:
            val = self._nextv
            self._nextv = None
            return val
        else:
            return next(self._iterator)

    def peek(self) -> Any:
        if self._nextv is None:
            self._nextv = next(self._iterator)

        return self._nextv

def filter_map(function, iterable: Iterable):
    for element in iterable:
        processed_element = function(element)
        if processed_element is not None:
            yield processed_element
