from decimal import Decimal
from investment_portfolio import InvestmentPortfolio, Stock, Currency


# Stock tests
def test_stock_init():
    stock = Stock(
        compain="Apple",
        amount=10,
        price=Decimal(100),
        currency=Currency.USD,
        title="Apple",
    )
    assert stock.compain == "Apple"
    assert stock.amount == 10
    assert stock.price == Decimal(100)
    assert stock.currency == Currency.USD
    assert stock.title == "Apple"


def test_stock_total_price():
    stock = Stock(
        compain="Apple",
        amount=10,
        price=Decimal(100),
        currency=Currency.USD,
        title="Apple",
    )
    assert stock.total_price == Decimal(1000)


# InvestmentPortfolio tests
def test_investment_portfolio_init():
    stock = Stock(
        compain="Apple",
        amount=10,
        price=Decimal(100),
        currency=Currency.USD,
        title="Apple",
    )
    portfolio = InvestmentPortfolio([stock])
    assert portfolio.total_amount == 10
    assert portfolio.items == [stock]


def test_investment_portfolio_total_amount():
    stock = Stock(
        compain="Apple",
        amount=10,
        price=Decimal(100),
        currency=Currency.USD,
        title="Apple",
    )
    portfolio = InvestmentPortfolio([stock])
    assert portfolio.total_amount == 10


def test_investment_portfolio_get_total_price():
    stocks = [
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
            price=Decimal(300),
            currency=Currency.USD,
            title="Microsoft",
        ),
    ]
    portfolio = InvestmentPortfolio(stocks)
    assert portfolio.get_total_price(Currency.USD) == Decimal(2500)
