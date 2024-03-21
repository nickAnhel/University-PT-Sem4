import re
from typing import Any
from accessify import private


# fmt: off
class NegativeOrZeroAgeError(Exception): ...
class EmailPatternError(Exception): ...
# fmt: on


class User:
    __private_attrs: tuple[str] = ()

    @private
    @classmethod
    def fill_private_attrs_set(cls) -> None:
        cls.__private_attrs = ("name", "age", "gender", "address")

    def __init__(self, name: str, age: int, gender: str, address: str, email: str) -> None:
        self.name: str = name
        self.age: int = self.__validate_age(age)
        self.gender: str = gender
        self.address: str = address
        self.email: str = self.__validate_email(email)
        self.fill_private_attrs_set()

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__private_attrs:
            raise AttributeError("You can't change the value of this attribute after initialization")
        object.__setattr__(self, name, value)

    @private
    @classmethod
    def __validate_age(cls, age) -> int:
        if not isinstance(age, int):
            raise TypeError("Age must be an 'int'")

        if age <= 0:
            raise NegativeOrZeroAgeError("Age must be greater then zero")

        return age

    @private
    @classmethod
    def __validate_email(cls, email) -> str:
        if not isinstance(email, str):
            raise TypeError("Email must be 'str'")

        pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-z0-9-]+\.[a-z]{2, 4}")
        if not re.match(pattern, email):
            raise EmailPatternError("Email should match the pattern 'youremail@site.com' ")

        return email
