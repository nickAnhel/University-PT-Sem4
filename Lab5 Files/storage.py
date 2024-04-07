import copy
import uuid
from dataclasses import dataclass, field
from typing import Generator, Sequence, Any


@dataclass
class Item:
    __id: uuid.UUID = field(init=False, repr=False, compare=False)
    title: str = field(default="Item")

    def __post_init__(self) -> None:
        self.__id = uuid.uuid4()

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    def __str__(self) -> str:
        return f"{self.title} #{self.id}"


class Storage:
    def __init__(self, items: Sequence[Item] | None) -> None:
        self.__id: uuid.UUID = uuid.uuid4()
        if items is None:
            self.__items: list[Item] = []
        else:
            self.__items: list[Item] = list(items)

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def items(self) -> list[Item]:
        return copy.deepcopy(self.__items)

    def add(self, item: Item) -> None:
        self.__items.append(item)

    def get(self, index: int) -> Item:
        if index not in range(-len(self.__items), len(self.__items)):
            raise ValueError(f"Index '{index}' is out of range")
        return self.__items.pop(index)

    def remove(self, item: Item) -> None:
        if item not in self.__items:
            raise IndexError(f"Item {item.title} not in storage")
        self.__items.remove(item)

    def __getitem__(self, index: int) -> Item:
        return self.__items[index]

    def __setitem__(self, index: int, item: Item) -> None:
        self.__items.insert(index, item)

    def __delitem__(self, index: int) -> None:
        if index not in range(-len(self.__items), len(self.__items)):
            raise IndexError(f"Index '{index}' is out of range")
        del self.__items[index]

    def __contains__(self, item: Item) -> bool:
        return item in self.__items

    def __iter__(self) -> Generator[Item, Any, None]:
        for item in self.__items:
            yield item

    def __len__(self) -> int:
        return len(self.__items)

    def __str__(self) -> str:
        return f"Storage #{self.id}\n"\
                "Items:\n" + "\n".join([str(item) for item in self.__items])

    def __repr__(self) -> str:
        return f"Storage(items={[repr(item) for item in self.__items]})"


if __name__ == "__main__":
    things: list[Item] = [
        Item("book1"),
        Item("book2"),
        Item("book3"),
        Item("book4"),
    ]
    storage = Storage(things)
    print(repr(storage))
    print(storage)
