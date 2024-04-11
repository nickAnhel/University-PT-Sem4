import json
from typing import Any
from abc import ABC, abstractmethod


class Serilizer(ABC):
    @abstractmethod
    def write(self, data) -> None:
        raise NotImplementedError()

    @abstractmethod
    def read(self, id) -> dict[str, Any]:
        raise NotImplementedError()


class JsonSerializer(Serilizer):
    def write(self, data: dict[str, Any]) -> None:
        with open(f"Lab5 Files/data/json/{data['id']}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def read(self, id: str) -> dict[str, Any]:
        with open(f"Lab5 Files/data/json/{id}.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data


class TxtSerializer(Serilizer):
    def write(self, data: dict[str, Any]) -> None:
        with open(f"Lab5 Files/data/txt/{data['id']}.txt", "w", encoding="utf-8") as file:
            file.write(str(data))

    def read(self, id: str) -> dict[str, Any]:
        with open(f"Lab5 Files/data/txt/{id}.txt", "r", encoding="utf-8") as file:
            data = json.loads(file.read().replace("'", '"'))
        return data
