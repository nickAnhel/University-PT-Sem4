import uuid
import enum
from typing import Any
from decimal import Decimal

from storage import Item, Storage


class Currency(enum.StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class Stock(Item):
    def __init__(
        self, compain: str, amount: int, price: Decimal, currency: Currency, title: str, id: uuid.UUID | None = None
    ) -> None:
        self.__compain: str = compain
        self.__amount: int = amount
        self.__price: Decimal = round(price, 2)
        self.__currency: Currency = currency
        super().__init__(title, id)

    @property
    def compain(self) -> str:
        return self.__compain

    @property
    def amount(self) -> int:
        return self.__amount

    @property
    def price(self) -> Decimal:
        return self.__price

    @property
    def currency(self) -> Currency:
        return self.__currency

    @property
    def total_price(self) -> Decimal:
        return self.amount * self.price

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data["price"] = float(self.price)
        return data

    def __str__(self) -> str:
        return f"Stock #{self.id}: {self.compain} {self.amount} {self.currency} {self.price}"


class InvestmentPortfolio(Storage):
    @property
    def total_amount(self) -> int:
        return sum(it.amount for it in self.items)  # type: ignore

    @property
    def total_price(self) -> Decimal:
        return sum(it.total_price for it in self.items)  # type: ignore

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InvestmentPortfolio":
        data["items"] = [Stock(**it) for it in data["items"]]
        return cls(**data)


if __name__ == "__main__":
    stocks: list[Stock] = [
        Stock(
            compain="Apple",
            amount=10,
            price=Decimal(100),
            currency=Currency.USD,
            title="Apple",
        ),
        Stock(
            compain="Microsoft",
            amount=5,
            price=Decimal(200),
            currency=Currency.USD,
            title="Microsoft",
        ),
        Stock(
            compain="Tesla",
            amount=3,
            price=Decimal(300),
            currency=Currency.USD,
            title="Tesla",
        ),
    ]

    my_portfolio = InvestmentPortfolio(stocks)
    # print(my_portfolio.total_amount)
    # print(my_portfolio.total_price)

    my_portfolio.write_to_file()
    print(InvestmentPortfolio.read_from_file(str(my_portfolio.id)))
