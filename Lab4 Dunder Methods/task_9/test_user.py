# Task 9 test_user.py
import pytest
from user import User, EmailPatternError, PasswordError


# Fixtures
@pytest.fixture(name="aduch")
def fixture_user() -> User:
    return User("Aduch", "166161#passWORD", 8, "male", "Piter")


# User test
def test_user_init(aduch) -> None:
    assert aduch.name == "Aduch"
    assert aduch.age == 8
    assert aduch.gender == "male"
    assert aduch.address == "Piter"


def test_user_private_attrs(aduch) -> None:
    with pytest.raises(AttributeError):
        aduch.name = "NotAduch"
    with pytest.raises(AttributeError):
        aduch.age = 18
    with pytest.raises(AttributeError):
        aduch.gender = "helicopter"
    with pytest.raises(AttributeError):
        aduch.address = "Amsterdam"


def test_user_validate_email(aduch) -> None:
    with pytest.raises(EmailPatternError):
        aduch.email = "incorrect@email"
    with pytest.raises(EmailPatternError):
        User("Not Aduch", "12093$WORDpass", 10, "male", "Samara", "incorrectEmail.com")

    aduch.email = "correct@email.com"
    assert aduch.email == "correct@email.com"


def test_user_validate_password(aduch) -> None:
    with pytest.raises(PasswordError):
        aduch.change_password("166161#passWORD", "123insorect")
    with pytest.raises(PasswordError):
        User("New Aduch", "inCor@", 12, "male", "Ryazan", "correct@mail.ru")
