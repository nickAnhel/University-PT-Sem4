# Task 9 user.py
import re
from typing import Any


# fmt: off
class NegativeOrZeroAgeError(Exception): ...
class EmailPatternError(Exception): ...
class PasswordError(Exception): ...
# fmt: on


class User:
    """Represents the user."""

    __private_attrs: set[str] = {"name", "age", "gender", "address"}

    def __init__(
        self, name: str, password: str, age: int, gender: str, address: str, email: str | None = None
    ) -> None:
        """
        Parametrs:
        ----------
        name : str, private
            User's name.
        password : str
            User's password.
        age : int, private
            User's age.
        gender : str, private
            User's gender.
        address : str, private
            User's address or city.
        email : str
            User's e-mail address.

        Raises:
        ------
        NegativeOrZeroAgeError
            If the given age less than or equal to zero.
        PasswordError
            If password didn't contain at least one uppercase letter (A-Z), one lowercase letter (a-z),
            one digit (0-9) and one special character from the '@$!%*?&' set.
        EmailPatternError
            If given email didn't match the pattern 'youremail@site.com'.
        """
        self.name: str = name
        self.age: int = self.__validate_age(age)
        self.gender: str = gender
        self.address: str = address
        self.__password: str = self.__validate_password(password)
        self.__email: str | None = self.__validate_email(email)

    @property
    def email(self) -> str | None:
        """Get user's e-mail address."""
        return self.__email

    @email.setter
    def email(self, new_e: str) -> None:
        """
        Set user's e-mail address.

        Raises:
        ------
        EmailPatternError
            If given email didn't match the pattern 'youremail@site.com'.
        """
        self.__email = self.__validate_email(new_e)

    def change_password(self, old_p: str, new_p: str) -> None:
        """
        Change user password.

        Parameters
        ----------
        old_p : str
            Old user password.
        new_p : str
            New password to set.

        Raises
        ------
        PasswordError
            If password didn't contain at least one uppercase letter (A-Z), one lowercase letter (a-z),
            one digit (0-9) and one special character from the '@$!%*?&' set
        """
        if old_p != self.__password:
            raise PasswordError(f"Password {old_p} is incorrect")
        self.__password = self.__validate_password(new_p)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Add the attribute with name 'name' and value 'value' or change it's value of existing attribute.

        Parameters
        ----------
        name : str
            Name of the attribute.
        value : Any
            Value of the attribute.

        Raises
        ------
        AttributeError
            If the attribute contaiend in private attributes set ("name", "age", "gender", "address").
        """
        if (name in self.__private_attrs) and (name in self.__dict__):
            raise AttributeError(f"You can't change the value of attribute '{name}' after initialization")

        super().__setattr__(name, value)

    def __delattr__(self, name: str) -> None:
        """Prohibits the deletion of object attributes."""
        raise AttributeError(f"You can't delete attribute with name '{name}'")

    @classmethod
    def __validate_age(cls, age) -> int:
        """
        Validate the given age.

        Parameters
        ----------
        age : int
            User's age.

        Returns
        -------
        int
            If the given age is correct.

        Raises
        ------
        TypeError
            If type of the agr is not 'int'
        NegativeOrZeroAgeError
            If the given age less than or equal to zero.
        """
        if not isinstance(age, int):
            raise TypeError("Age must be an 'int'")

        if age <= 0:
            raise NegativeOrZeroAgeError("Age must be greater then zero")

        return age

    @classmethod
    def __validate_password(cls, password: str) -> str:
        """Validate the password.

        Parameters
        ----------
        password : str
            User's password.

        Returns
        -------
        str
            Password if it is correct.

        Raises
        ------
        TypeError
            If type of the password is not 'str'.
        PasswordError
            If password is too short or didn't contains at least one uppercase letter (A-Z), one lowercase letter (a-z), "
                "one digit (0-9) and one special character from the '@$!%*?&' set.
        """
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

        return password

    @classmethod
    def __validate_email(cls, email: str | None) -> str | None:
        """Validate the email.

        Parameters
        ----------
        email : str | None
            User's email.

        Returns
        -------
        str | None
            Email if it is correct.

        Raises
        ------
        TypeError
            If type of the email is not 'str'.
        EmailPatternError
            If email didn't match the pattern 'youremail@site.com'.
        """
        if email is None:
            return None

        if not isinstance(email, str):
            raise TypeError("Email type must be 'str'")

        pattern: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not pattern.match(email):
            raise EmailPatternError("Email should match the pattern 'youremail@site.com'")

        return email

    def __str__(self) -> str:
        """Get the string represrentation of the user."""
        # fmt: off
        return (
            f"{self.name}, {self.gender}"
            f"\nEmail: {self.__email}"
            f"\nAge: {self.age}"
            f"\nAddress: {self.address}"
        )
        # fmt: on

    def __repr__(self) -> str:
        """Get the string represrentation of the user in class creation format."""
        return (
            f"User('{self.name}', 'CONFIDENTIALLY', {self.age}, '{self.gender}', '{self.address}', '{self.__email}')"
        )
