import asyncio
import pytest

from files import read, write


@pytest.mark.asyncio
async def test_read_empty_file():
    queues = [asyncio.Queue() for _ in range(3)]

    await read("./test_data/empty_input.txt", queues)

    for queue in queues:
        assert queue.empty()


@pytest.mark.asyncio
async def test_write_empty_queue():
    queue = asyncio.Queue()

    await write("./test_data/empty_output.txt", queue)

    with open("./test_data/empty_output.txt", "r", encoding="utf-8") as f:
        assert f.read() == ""


@pytest.mark.asyncio
async def test_read_write():
    queues = [asyncio.Queue() for _ in range(3)]

    await read("./test_data/input.txt", queues)

    for i, queue in enumerate(queues):
        await write(f"./test_data/output_{i}.txt", queue)

    for i in range(3):
        with open(f"./test_data/output_{i}.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == 1
            assert lines[0].strip() == f"line {i}"
