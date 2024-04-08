from typing import Any, Sequence
import uuid
from storage import Storage, Item


class MaxWeightExcessError(Exception): ...


class Book(Item):
    def __init__(self, title: str, weight: int, author: str, price: int, id: uuid.UUID | None = None) -> None:
        self.__weight: int = self.validate_weight(weight)
        self.__author: str = author
        self.__price = self.validate_price(price)

        super().__init__(title, id)

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def author(self) -> str:
        return self.__author

    @property
    def price(self) -> int:
        return self.__price

    def __str__(self) -> str:
        return f"Book #{self.id}: {self.title} by {self.author} with weight {self.weight} and price {self.price}"

    def __repr__(self) -> str:
        return (
            f"Book(title={self.title}, author={self.author}, weight={self.weight}, price={self.price}, id={self.id})"
        )

    def __radd__(self, other: int) -> int:
        if not isinstance(other, int):
            return NotImplemented
        return self.__weight + other

    @classmethod
    def validate_price(cls, price: int) -> int:
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @classmethod
    def validate_weight(cls, weight: int) -> int:
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        return weight


class Bookcase(Storage):
    def __init__(self, max_weight: int, items: Sequence[Book] | None = None, id: uuid.UUID | None = None) -> None:
        self.__max_weight: int = self.validate_max_weight(max_weight)

        if sum(items) > self.__max_weight:  # type: ignore
            raise MaxWeightExcessError("Total weight of books exceeds max weight of bookcase")
        super().__init__(items, id)

    def add(self, item: Book) -> None:
        if sum(self.__items) + item.weight > self.__max_weight:  # type: ignore
            raise MaxWeightExcessError("Total weight of books exceeds max weight of bookcase")
        super().add(item)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Bookcase":
        data["items"] = [Book(**it) for it in data["items"]]
        return cls(**data)

    @classmethod
    def validate_max_weight(cls, max_weight: int) -> int:
        if max_weight < 0:
            raise ValueError("Max weight cannot be negative")
        return max_weight


if __name__ == "__main__":
    my_books = [
        Book("book1", 10, "author1", 10),
        Book("book2", 20, "author2", 20),
        Book("book3", 30, "author3", 30),
        Book("book4", 40, "author4", 40),
    ]
    my_bookcase = Bookcase(100, my_books)
    # for book in my_bookcase:
    #     print(repr(book))

    # print(my_bookcase.to_dict())
    # print(Bookcase(**my_bookcase.to_dict()))
    my_bookcase.write_to_file()

    print(Bookcase.read_from_file())
