from typing import Sequence, Generator, Any


# fmt: off
class EmptyQueueError(Exception): ...
# fmt: on


class Queue:
    def __init__(self, items: Sequence | None = None) -> None:
        if items is None:
            self.__items: list[Any] = []
        else:
            self.__items = list(items)

    @property
    def items(self) -> list[Any]:
        return self.__items

    @property
    def size(self) -> int:
        return len(self.__items)

    @property
    def empty(self) -> bool:
        return not bool(self.__items)

    def push(self, item) -> None:
        self.__items.append(item)

    def pop(self) -> Any:
        if not self.__items:
            raise EmptyQueueError("Queue is empty")

        item = self.__items[0]
        self.__items.remove(item)
        return item

    def __bool__(self) -> bool:
        return bool(self.__items)

    def __len__(self):
        return len(self.__items)

    def __iter__(self) -> Generator[Any, Any, None]:
        for item in self.__items:
            yield item

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __add__(self, other) -> "Queue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return Queue(self.items + other.items)

    def __iadd__(self, other) -> "Queue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return Queue(self.items + other.items)

    def __repr__(self) -> str:
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])

    def __str__(self) -> str:
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])
