from decimal import Decimal
import pytest

from bookcase import Book, Bookcase, MaxWeightExcessError


# Book tests
def test_book_init():
    book = Book("book1", 10, "author1", Decimal(10))
    assert book.title == "book1"
    assert book.author == "author1"
    assert book.weight == 10
    assert book.price == Decimal(10)


def test_book_radd():
    book = Book("book1", 10, "author1", Decimal(10))
    assert 10 + book == 20


# Bookcase tests
def test_bookcase_init():
    bookcase = Bookcase(100)
    assert bookcase.max_weight == 100


def test_bookcase_total_book_weight():
    bookcase = Bookcase(100)
    assert bookcase.total_book_weight == 0
    bookcase.add(Book("book1", 10, "author1", Decimal(10)))
    assert bookcase.total_book_weight == 10


def test_bookcase_total_book_price():
    bookcase = Bookcase(100)
    assert bookcase.total_book_price == Decimal(0)
    bookcase.add(Book("book1", 10, "author1", Decimal(10)))
    assert bookcase.total_book_price == Decimal(10)


def test_bookcase_add():
    bookcase = Bookcase(20)
    bookcase.add(Book("book1", 10, "author1", Decimal(10)))
    assert bookcase.total_book_weight == 10
    with pytest.raises(MaxWeightExcessError):
        bookcase.add(Book("book2", 20, "author2", Decimal(10)))


def test_bookcase_find_book_by_author():
    bookcase = Bookcase(100)
    book1 = Book("book1", 10, "author1", Decimal(10))
    book2 = Book("book2", 20, "author2", Decimal(10))
    book3 = Book("book3", 30, "author1", Decimal(10))
    bookcase.add(book1)
    bookcase.add(book2)
    bookcase.add(book3)
    assert bookcase.find_book_by_author("author1") == book1
    assert bookcase.find_book_by_author("author2") == book2
    assert bookcase.find_book_by_author("author3") is None
