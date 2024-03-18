from typing import Sequence


class Queue:
    def __init__(self, items: Sequence | None = None) -> None:
        if items is None:
            self.__items: list = []
        else:
            self.__items = list(items)

    @property
    def items(self):
        return self.__items

    @property
    def size(self):
        return len(self.__items)

    @property
    def empty(self):
        return bool(self.__items)

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        item = self.__items[0]
        self.__items.remove(item)
        return item

    def __bool__(self):
        return bool(self.__items)

    def __len__(self):
        return len(self.__items)

    def __iter__(self):
        index = 0
        while index < len(self.__items):
            yield self.__items[index]
            index += 1

    def __contains__(self, item):
        return item in self.__items

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return Queue(self.items + other.items)

    def __iadd__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return Queue(self.items + other.items)

    def __repr__(self) -> str:
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])
