import uuid
import enum
import os
import datetime
from typing import Any
from decimal import Decimal
import requests

from storage import Item, Storage


class Currency(enum.StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


def convert_currency(from_currency: Currency, to_currency: Currency, amount: Decimal) -> Decimal | None:
    if from_currency == to_currency:
        return amount

    api_key: str | None = os.environ.get("API_KEY")
    date: str = f"{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day - 1}"
    url: str = f"https://api.currencyapi.com/v3/historical?apikey={api_key}&base_currency={from_currency}&date={date}"

    coef: Decimal = Decimal(requests.get(url, timeout=1000).json()["data"][to_currency]["value"])

    return Decimal(round(amount * coef, 2))


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

    @classmethod
    def validate_amount(cls, amount: int) -> int:
        if amount <= 0:
            raise ValueError("Amount cannot be negative or zero")
        return amount

    @classmethod
    def validate_price(cls, price: Decimal) -> Decimal:
        if price <= 0:
            raise ValueError("Price cannot be negative or zero")
        return price

    def __str__(self) -> str:
        return f"Stock #{self.id}: {self.compain} {self.amount} {self.currency} {self.price}"

    def __eq__(self, other: Item) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.id == other.id
            and self.title == other.title
            and self.compain == other.compain
            and self.amount == other.amount
            and self.price == other.price
            and self.currency == other.currency
        )


class InvestmentPortfolio(Storage):
    @property
    def total_amount(self) -> int:
        return sum(it.amount for it in self.items)  # type: ignore

    def get_total_price(self, currency: Currency) -> Decimal | None:
        total_price = Decimal(0)
        for it in self.items:
            if it.currency == currency:  # type: ignore
                total_price += it.total_price  # type: ignore
            else:
                try:
                    total_price += convert_currency(it.currency, currency, it.total_price)  # type: ignore
                except KeyError:
                    return None
        return total_price

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InvestmentPortfolio":
        data["items"] = [Stock.from_dict(it) for it in data["items"]]
        data["id"] = uuid.UUID(data["id"])
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
            price=Decimal(3000),
            currency=Currency.RUB,
            title="Microsoft",
        ),
        Stock(
            compain="Tesla",
            amount=3,
            price=Decimal(300),
            currency=Currency.EUR,
            title="Tesla",
        ),
    ]

    my_portfolio = InvestmentPortfolio(stocks)

    my_portfolio.write_to_file()
    print(InvestmentPortfolio.read_from_file(str(my_portfolio.id)))
