import asyncio


async def read(file_name: str, queues: list[asyncio.Queue]):
    with open(file_name, mode="r", encoding="utf-8") as f:
        for index, line in enumerate(f):
            await queues[index % 3].put(line.strip("\n"))


async def write(file_name: str, queue: asyncio.Queue):
    with open(file_name, mode="w", encoding="utf-8") as f:
        while not queue.empty():
            item = await queue.get()
            f.write(item + "\n")


async def main():
    queues = [asyncio.Queue() for _ in range(3)]
    reader = asyncio.create_task(read("./data/input.txt", queues))
    writers = [asyncio.create_task(write(f"./data/output_{i}.txt", q)) for i, q in enumerate(queues)]

    await asyncio.gather(reader, *writers)


if __name__ == "__main__":
    asyncio.run(main())
