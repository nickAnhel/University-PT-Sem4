# Task 2 my_queue.py
import copy
from curses.ascii import EM
from dataclasses import dataclass
from typing import Generic, Generator, Optional, TypeVar


T = TypeVar("T")


class EmptyQueueError(Exception): ...


@dataclass
class Node(Generic[T]):
    value: T
    next: Optional["Node[T]"]
    prev: Optional["Node[T]"]


class MyQueue(Generic[T]):
    """Represents the queue data structure."""

    def __init__(self) -> None:
        """
        Parameters
        ----------
        items : Sequence[T] | None, optional
            Initial sequence, by default None
        """
        self.__tail: Optional[Node[T]] = None
        self.__head: Optional[Node[T]] = None
        self.__size: int = 0

    @property
    def size(self) -> int:
        """Get the queue items count."""
        return self.__size

    @property
    def empty(self) -> bool:
        """Return True if queue is empty, or False."""
        return self.__size == 0

    def push(self, item: T) -> None:
        """
        Push new item to the queue

        Parameters
        ----------
        item : T
            New item to add to the queue.
        """
        if self.__head is None and self.__tail is None:
            self.__head = self.__tail = Node[T](item, None, None)
            self.__head.prev = self.__tail
            self.__tail.next = self.__head

        elif self.__head is self.__tail:
            self.__head.next = None
            self.__tail = Node[T](item, self.__head, None)
            self.__head.prev = self.__tail

        else:
            node = Node[T](item, self.__tail, None)
            self.__tail = node
            self.__tail.next.prev = self.__tail

        self.__size += 1

    def get(self) -> T | None:
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
        if self.__size == 0:
            raise EmptyQueueError("Queue is empty")

        if self.__head is self.__tail:
            node = self.__head
            self.__head = self.__tail = None
            self.__size -= 1
            return node.value

        node = self.__head
        self.__head = self.__head.prev
        self.__head.next = None

        self.__size -= 1

        return node.value

    def __bool__(self) -> bool:
        """Get the boolen represenation of the queue."""
        return self.__size == 0

    def __len__(self) -> int:
        """Get the number of items in the queue."""
        return self.__size

    def __contains__(self, value: T) -> bool:
        temp = self.__head
        while temp is not None:
            if temp.value == value:
                return True
            temp = temp.prev
        return False

    def __iter__(self) -> Generator:
        temp = self.__head
        while temp is not None:
            yield temp.value
            temp = temp.prev

    def __str__(self) -> str:
        res: list[str] = []

        temp = self.__tail
        while temp is not None:
            res.append(f"{temp.value}")
            temp = temp.next

        return " -> ".join(res)


if __name__ == "__main__":
    queue = MyQueue[int]()

    for i in range(1, 10):
        queue.push(i)

    print(queue)
