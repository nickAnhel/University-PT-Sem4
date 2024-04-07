from abc import ABC, abstractmethod
import json


class Serilizer(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError()

    @abstractmethod
    def read(self):
        raise NotImplementedError()


class JsonSerializer(Serilizer):
    def write(self, data):
        with open("test.json", "w", encoding="utf-8") as file:
            json.dump(data, file)

    def read(self):
        with open("test.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data


class TxtSerializer(Serilizer):
    def write(self, data):
        with open("test.txt", "w", encoding="utf-8") as file:
            file.write(str(data))

    def read(self):
        with open("test.txt", "r", encoding="utf-8") as file:
            data = file.readlines()
        return data


JsonSerializer().write({"1": "2"})
print(JsonSerializer().read())
