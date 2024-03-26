import copy
from dataclasses import dataclass
from typing import Mapping, Sequence, Generator, Any

# fmt: off
class EmptyQueueError(Exception): ...
# fmt: on


class MyQueue:
    def __init__(self, items: Sequence[Any] | Mapping[Any, Any] | None = None) -> None:
        if items is None:
            self.__items: list[Any] = []
        else:
            self.__items = list(items)

    @property
    def items(self):
        return copy.deepcopy(self.__items)

    @property
    def size(self) -> int:
        return len(self.__items)

    @property
    def empty(self) -> bool:
        return len(self.__items) == 0

    def push(self, item) -> None:
        self.__items.append(item)

    def get(self) -> Any:
        if not self.__items:
            raise EmptyQueueError("Queue is empty.")

        return self.__items.pop(0)

    def __bool__(self) -> bool:
        return bool(self.__items)

    def __len__(self):
        return len(self.__items)

    def __iter__(self) -> Generator[Any, Any, None]:
        for item in self.__items:
            yield item

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.items == other.items

    def __add__(self, other) -> "MyQueue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return MyQueue(self.items + other.items)

    def __iadd__(self, other) -> "MyQueue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return MyQueue(self.items + other.items)

    def __repr__(self) -> str:
        return f"MyQueue({self.__items})"

    def __str__(self) -> str:
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])
