import asyncio
# import aiofiles


async def write(file_name: str, data: str):
    # async with aiofiles.open(file_name, mode="a", encoding="utf-8") as f:
    #     await f.write(data)

    with open(file_name, mode="a", encoding="utf-8") as f:
        f.write(data)


async def main(file_name: str):
    # async with aiofiles.open(file_name, mode="r", encoding="utf-8") as f:
    #     index = 0
    #     async for line in f:
    #         await write(f"./data/output_{index % 3}.txt", line)
    #         index += 1

    with open(file_name, mode="r", encoding="utf-8") as f:
        index = 0
        for index, line in enumerate(f):
            await write(f"./data/output_{index % 3}.txt", line)


if __name__ == "__main__":
    asyncio.run(main("./data/input.txt"))
    # print(timeit.timeit(lambda: asyncio.run(main("./data/input.txt")), globals=globals(), number=10))
