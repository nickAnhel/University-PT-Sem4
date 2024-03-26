import re
from typing import Any
from accessify import private


# fmt: off
class NegativeOrZeroAgeError(Exception): ...
class EmailPatternError(Exception): ...
class PasswordError(Exception): ...
# fmt: on


class User:
    __private_attrs: set[str] = {"name", "age", "gender", "address"}

    def __init__(self, name: str, password: str, age: int, gender: str, address: str, email: str = None) -> None:
        self.__dict__["name"] = name
        self.__dict__["age"] = self.__validate_age(age)
        self.__dict__["gender"] = gender
        self.__dict__["address"] = address
        self.__email: str = self.__validate_email(email)
        self.__password: str = self.__validate_password(password)

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, p: str) -> None:
        self.__password = self.__validate_password(p)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, e: str) -> None:
        self.__email = self.__validate_email(e)

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__private_attrs:
            raise AttributeError(f"You can't change the value of attribute '{name}' after initialization")

        super().__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"You can't delete attribute with name '{name}'")

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
            raise PasswordError(f"Password '{password}' is too short")

        pattern: re.Pattern[str] = re.compile(r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d#@$!%*?&]{8,}$")
        if not pattern.match(password):
            raise PasswordError(
                "Password must contain at least one uppercase letter (A-Z), one lowercase letter (a-z), "
                "one digit (0-9) and one special character from the '@$!%*?&' set"
            )

    @private
    @classmethod
    def __validate_email(cls, email) -> str:
        if email is None:
            return None

        if not isinstance(email, str):
            raise TypeError("Email type must be 'str'")

        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not pattern.match(email):
            raise EmailPatternError("Email should match the pattern 'youremail@site.com'")

        return email

    def __str__(self) -> str:
        return f"{self.name}, {self.gender}" \
               f"\nEmail: {self.__email}" \
               f"\nAge: {self.age}" \
               f"\nAddress: {self.address}"

    def __repr__(self) -> str:
        return f"User('{self.name}', 'CONFIDENTIALLY', {self.age}, '{self.gender}', '{self.address}', '{self.__email}')"
