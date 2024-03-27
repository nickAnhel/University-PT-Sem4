# Task 2 test_my_queue.py
import pytest
from my_queue import EmptyQueueError, MyQueue


# Fixtures
@pytest.fixture(name="queue")
def fixture_queue() -> MyQueue:
    return MyQueue([1, 2, 3, 4])


@pytest.fixture(name="empty_queue")
def fixture_empty_queue() -> MyQueue:
    return MyQueue()


# MyQueue tests
def test_queue_init_and_props(queue: MyQueue) -> None:
    assert queue.items == [1, 2, 3, 4]
    assert queue.empty is False
    assert queue.size == 4


def test_queue_push(queue: MyQueue) -> None:
    queue.push(5)
    assert queue.items == [1, 2, 3, 4, 5]
    assert queue.size == 5


def test_queue_get(queue: MyQueue, empty_queue: MyQueue) -> None:
    item: int = queue.get()
    assert queue.items == [2, 3, 4]
    assert queue.size == 3
    assert item == 1

    with pytest.raises(EmptyQueueError):
        empty_queue.get()


def test_queue_to_bool(queue: MyQueue, empty_queue: MyQueue) -> None:
    assert bool(queue) is True
    assert bool(empty_queue) is False


def test_queue_len(queue: MyQueue, empty_queue: MyQueue) -> None:
    assert len(queue) == 4
    assert len(empty_queue) == 0


def test_queue_contains(queue: MyQueue) -> None:
    assert (1 in queue) is True
    assert (5 in queue) is False


def test_queue_add_iadd(queue: MyQueue) -> None:
    assert queue + MyQueue([5, 6]) == MyQueue([1, 2, 3, 4, 5, 6])

    queue += MyQueue([5, 6])
    assert queue == MyQueue([1, 2, 3, 4, 5, 6])
