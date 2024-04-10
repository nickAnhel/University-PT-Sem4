import copy
import uuid
from typing import Generator, Sequence, Any

from serializers import Serilizer, JsonSerializer


class Item:
    def __init__(self, title: str, id: uuid.UUID | None = None) -> None:
        self.__title: str = title
        if id is None:
            self.__id: uuid.UUID = uuid.uuid4()
        else:
            self.__id: uuid.UUID = id

    @property
    def title(self) -> str:
        return self.__title

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for attr, item in self.__dict__.items():
            if isinstance(item, uuid.UUID):
                item = str(item)

            if "__" in attr:
                attr = attr.rsplit("__", maxsplit=1)[-1]
            data[attr] = item
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Item":
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.__title} #{self.id}"

    def __repr__(self) -> str:
        return f"Item(title={self.__title}, id={repr(self.id)})"


class Storage:
    __serializer: Serilizer = JsonSerializer()

    def __init__(self, items: Sequence[Item] | None = None, id: uuid.UUID | None = None) -> None:
        if items is None:
            self.__items: list[Item] = []
        else:
            self.__items: list[Item] = list(items)

        if id is None:
            self.__id: uuid.UUID = uuid.uuid4()
        else:
            self.__id: uuid.UUID = id

    @property
    def id(self) -> uuid.UUID:
        return self.__id

    @property
    def items(self) -> list[Item]:
        return copy.deepcopy(self.__items)

    def add(self, item: Item) -> None:
        self.__items.append(item)

    def pop(self, index: int = -1) -> Item:
        if index not in range(-len(self.__items), len(self.__items)):
            raise IndexError(f"Index '{index}' is out of range")
        return self.__items.pop(index)

    def remove(self, item: Item) -> None:
        if item not in self.__items:
            raise ValueError(f"Item {item.title} not in storage")
        self.__items.remove(item)

    def clear(self) -> None:
        self.__items.clear()

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        for attr, item in self.__dict__.items():
            if "serializer" in attr:
                continue
            if "__" in attr:
                attr = attr.rsplit("__", maxsplit=1)[-1]
            data[attr] = item

        data["items"] = [it.to_dict() for it in data["items"]]
        data["id"] = str(self.id)

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Storage":
        data["items"] = [Item(**it) for it in data["items"]]
        return cls(**data)

    def write_to_file(self) -> None:
        data: dict[str, Any] = self.to_dict()
        self.__serializer.write(data)

    @classmethod
    def read_from_file(cls, id: str) -> "Storage":
        data: dict[str, Any] = cls.__serializer.read(id)
        return cls.from_dict(data)

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
        return StorageIterator(self.items)

    def __len__(self) -> int:
        return len(self.__items)

    def __str__(self) -> str:
        return f"Storage #{self.id}\n" "Items:\n" + "\n".join([str(item) for item in self.__items])

    def __repr__(self) -> str:
        return f"Storage(items={[repr(item) for item in self.__items]})"


class StorageIterator(Generator[Item, Any, None]):
    def __init__(self, storage_items: list[Item]) -> None:
        self.__items: list[Item] = storage_items
        self.__index: int = 0

    def __iter__(self) -> "StorageIterator":
        return self

    def __next__(self) -> Item:
        if self.__index < len(self.__items):
            item: Item = self.__items[self.__index]
            self.__index += 1
            return item
        raise StopIteration

    def to_start(self) -> None:
        self.__index = 0

    def to_index(self, index: int) -> None:
        if index not in range(-len(self.__items), len(self.__items)):
            raise IndexError(f"Index '{index}' is out of range")
        self.__index = index

    def send(self, value: Item) -> None:
        self.__items.append(value)

    def throw(self, typ: Exception, val: Any = None, tb: Any = None) -> None:
        raise typ


if __name__ == "__main__":
    things: list[Item] = [
        Item(title="book1"),
        Item(title="book2"),
        Item(title="book3"),
        Item(title="book4"),
    ]
    my_storage = Storage(things)

    my_storage.write_to_file()
    print(Storage.read_from_file(str(my_storage.id)))
