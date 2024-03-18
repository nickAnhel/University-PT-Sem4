from typing import Any


class User:
    private_attrs = ("age", "gender")

    def __init__(self, name: str, age: int, gender: str, address: str) -> None:
        self.name = name
        self.age = age
        self.gender = gender
        self.address = address

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.private_attrs:
            raise AttributeError
        self.name = value
