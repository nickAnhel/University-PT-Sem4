import logging
import asyncio
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


async def monitor_directory(path):
    event_handler = LoggingEventHandler()

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()


async def main():
    logging.basicConfig(
        # filename="fs.log",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # dirs_to_monitor = ["./data"]
    dirs_to_monitor = ["./data/dir1", "./data/dir2", "./data/dir3"]
    monitors = []
    for dir in dirs_to_monitor:
        monitors.append(asyncio.create_task(monitor_directory(dir)))

    await asyncio.gather(*monitors)


if __name__ == "__main__":
    asyncio.run(main())
