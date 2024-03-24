import re
from typing import Any
from accessify import private


# fmt: off
class NegativeOrZeroAgeError(Exception): ...
class EmailPatternError(Exception): ...
class PasswordError(Exception): ...
# fmt: on


class User:
    __private_attrs: tuple[str] = ()

    @private
    @classmethod
    def __fill_private_attrs_set(cls) -> None:
        cls.__private_attrs = ("name", "age", "gender", "address")

    def __new__(cls, *args, **kwargs):
        cls.__private_attrs = ()
        return super().__new__(cls)

    def __init__(self, name: str, password: str, email: str, age: int, gender: str, address: str) -> None:
        self.name: str = name
        self.email: str = self.__validate_email(email)
        self.password: str = self.__validate_password(password)
        self.age: int = self.__validate_age(age)
        self.gender: str = gender
        self.address: str = address
        self.__fill_private_attrs_set()

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
    def __validate_password(cls, password: str) -> str:
        if not isinstance(password, str):
            raise TypeError("Password type must be 'str'")

        if len(password) < 8:
            raise PasswordError(f"Password '{password}' if too short")

        pattern = re.compile(r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d#@$!%*?&]{8,}$")
        if not pattern.match(password):
            raise PasswordError(
                "Password must contain at least one uppercase letter (A-Z), one lowercase letter (a-z), "
                "one digit (0-9) and one special character from the '@$!%*?&' set"
            )

    @private
    @classmethod
    def __validate_email(cls, email) -> str:
        if not isinstance(email, str):
            raise TypeError("Email type must be 'str'")

        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not pattern.match(email):
            raise EmailPatternError("Email should match the pattern 'youremail@site.com'")

        return email
