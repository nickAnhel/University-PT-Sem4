# Task 2 my_queue.py
import copy
from typing import Generic, Sequence, Generator, TypeVar


T = TypeVar("T")


class EmptyQueueError(Exception): ...


class MyQueue(Generic[T]):
    """Represents the queue data structure."""

    def __init__(self, items: Sequence[T] | None = None) -> None:
        """
        Parameters
        ----------
        items : Sequence[T] | None, optional
            Initial sequence, by default None
        """
        if items is None:
            self.__items: list[T] = []
        else:
            self.__items: list[T] = list(items)

    @property
    def items(self) -> list[T]:
        """Get the queue items."""
        return copy.deepcopy(self.__items)

    @property
    def size(self) -> int:
        """Get the queue items count."""
        return len(self.__items)

    @property
    def empty(self) -> bool:
        """Return True if queue is empty, or False."""
        return len(self.__items) == 0

    def push(self, item: T) -> None:
        """
        Push new item to the queue

        Parameters
        ----------
        item : T
            New item to add to the queue.
        """
        self.__items.append(item)

    def get(self) -> T:
        """
        Pop the first added to the queue item.

        Returns
        -------
        T
            The first added to the queue item.

        Raises
        ------
        EmptyQueueError
            If queue is empty.
        """
        if not self.__items:
            raise EmptyQueueError("Queue is empty.")

        return self.__items.pop(0)

    def __bool__(self) -> bool:
        """Get the boolen represenation of the queue."""
        return bool(self.__items)

    def __len__(self) -> int:
        """Get the number of items in the queue."""
        return len(self.__items)

    def __iter__(self) -> Generator[T, None, None]:
        """Get the number of items in the queue."""
        for item in self.__items:
            yield item

    def __contains__(self, item) -> bool:
        """Return True if item is queued, else False."""
        return item in self.__items

    def __eq__(self, other) -> bool:
        """Return True if item is queued, else False."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.items == other.items

    def __add__(self, other) -> "MyQueue":
        """Stack two queues."""
        if not isinstance(other, self.__class__):
            return NotImplemented
        return MyQueue(self.items + other.items)

    def __iadd__(self, other) -> "MyQueue":
        """Add one queue to another."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        self.__items += other.items
        return self

    def __repr__(self) -> str:
        """Get the string represrentation of the queue in class creation format."""
        return f"MyQueue({self.__items})"

    def __str__(self) -> str:
        """Get the string represrentation of the queue."""
        return "Queue: " + " -> ".join(str(item) for item in self.__items[::-1])


if __name__ == "__main__":
    queue = MyQueue()
    for i in range(1, 10):
        queue.push(i)

    while not queue.empty:
        task_index = queue.get()
        print(f"Working on task #{task_index}")
