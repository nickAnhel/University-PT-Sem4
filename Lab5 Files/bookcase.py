import uuid
from decimal import Decimal
from typing import Any, Sequence

from storage import Storage, Item


class MaxWeightExcessError(Exception): ...


class Book(Item):
    def __init__(self, title: str, weight: int, author: str, price: Decimal, id: uuid.UUID | None = None) -> None:
        self.__weight: int = self.validate_weight(weight)
        self.__author: str = author
        self.__price: Decimal = self.validate_price(price)

        super().__init__(title, id)

    @property
    def weight(self) -> int:
        return self.__weight

    @property
    def author(self) -> str:
        return self.__author

    @property
    def price(self) -> Decimal:
        return self.__price

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data["price"] = float(self.price)
        return data

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
    def validate_price(cls, price: Decimal) -> Decimal:
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

    @property
    def max_weight(self) -> int:
        return self.__max_weight

    @property
    def total_book_weight(self) -> int:
        return sum(self.__items)  # type: ignore

    @property
    def total_book_price(self) -> Decimal:
        return sum(book.price for book in self.items)  # type: ignore

    def add(self, item: Book) -> None:
        if sum(self.__items) + item.weight > self.__max_weight:  # type: ignore
            raise MaxWeightExcessError("Total weight of books exceeds max weight of bookcase")
        super().add(item)

    def find_book_by_author(self, author: str) -> Book | None:
        for book in self.items:
            if book.author == author:  # type: ignore
                return book  # type: ignore
        return None

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
    my_books: list[Book] = [
        Book("book1", 10, "author1", Decimal(10)),
        Book("book2", 20, "author2", Decimal(10)),
        Book("book3", 30, "author3", Decimal(10)),
        Book("book4", 40, "author4", Decimal(10)),
    ]
    my_bookcase = Bookcase(100, my_books)
    # for book in my_bookcase:
    #     print(repr(book))

    # print(my_bookcase.to_dict())
    # print(Bookcase(**my_bookcase.to_dict()))
    # my_bookcase.write_to_file()
    # print(Bookcase.read_from_file(str(my_bookcase.id)))

    print(my_bookcase.total_book_price)
    print(my_bookcase.find_book_by_author("author1"))
