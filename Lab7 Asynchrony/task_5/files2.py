import asyncio


async def write(file_name: str, data: str):
    with open(file_name, mode="a", encoding="utf-8") as f:
        f.write(data)


async def main(file_name: str):
    with open(file_name, mode="r", encoding="utf-8") as f:
        index = 0
        for line in f:
            await write(f"./data/output_{index % 3}.txt", line)
            index += 1


if __name__ == "__main__":
    asyncio.run(main("./data/input.txt"))
