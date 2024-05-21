import asyncio


async def read(file_name: str):
    with open(file_name, mode="r", encoding="utf-8") as f:
        result = [[], [], []]
        index = 0
        for line in f:
            result[index % 3].append(line.strip("\n"))
            index += 1
        return result


async def write(file_name: str, data: list[str]):
    with open(file_name, mode="w", encoding="utf-8") as f:
        for item in data:
            f.write(item + "\n")


async def main():
    reader = asyncio.create_task(read("./data/input.txt"))
    data = await reader

    writers = [
        asyncio.create_task(write(f"./data/output_{i}.txt", d)) for i, d in enumerate(data)
    ]

    await asyncio.gather(*writers)

    print(data)


if __name__ == "__main__":
    asyncio.run(main())
