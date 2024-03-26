import copy
from typing import Generic, Sequence, Generator, TypeVar
import timeit


T = TypeVar("T")

# fmt: off
class EmptyQueueError(Exception): ...
# fmt: on


class MyQueue(Generic[T]):
    def __init__(self, items: Sequence[T] | None = None) -> None:
        if items is None:
            self.__items: list[T] = []
        else:
            self.__items: list[T] = list(items)

    @property
    def items(self) -> list[T]:
        return copy.deepcopy(self.__items)

    @property
    def size(self) -> int:
        return len(self.__items)

    @property
    def empty(self) -> bool:
        return len(self.__items) == 0

    def push(self, item: T) -> None:
        self.__items.append(item)

    def get(self) -> T:
        if not self.__items:
            raise EmptyQueueError("Queue is empty.")

        return self.__items.pop(0)

    def __bool__(self) -> bool:
        return bool(self.__items)

    def __len__(self) -> int:
        return len(self.__items)

    def __iter__(self) -> Generator[T, None, None]:
        for item in self.__items:
            yield item

    def __contains__(self, item) -> bool:
        return item in self.__items

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.items == other.items

    def __add__(self, other) -> "MyQueue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return MyQueue(self.items + other.items)

    def __iadd__(self, other) -> "MyQueue":
        if not isinstance(other, self.__class__):
            raise TypeError
        return MyQueue(self.items + other.items)

    def __repr__(self) -> str:
        return f"MyQueue({self.__items})"

    def __str__(self) -> str:
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])


if __name__ == "__main__":
    print(
        timeit.timeit("[l.append(1) for _ in range(100)]", "l = []")
    )
    print(
        timeit.timeit("[q.push(1) for _ in range(100)]", "from my_queue import MyQueue; q = MyQueue()")
    )

    queue = MyQueue()
    for i in range(1, 10):
        queue.push(i)

    while not queue.empty:
        task_index = queue.get()
        print(f"Working on task #{task_index}")
