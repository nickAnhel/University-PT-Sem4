import asyncio
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, LoggingEventHandler


class Handler(LoggingEventHandler):
    def __init__(self, path: str, logger: logging.Logger | None = None) -> None:
        self._path: str = path
        super().__init__(logger)

    def on_modified(self, event: FileSystemEvent) -> None:
        if event.src_path == self._path:
            return
        super().on_modified(event)


async def monitor_directory(path: str) -> None:
    logger: logging.Logger = logging.getLogger(path.split("/")[-1])
    logger.setLevel(logging.INFO)

    # File logs
    fh = logging.FileHandler(f"./logs/{path.split('/')[-1]}.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    logger.addHandler(fh)

    # Console logs
    # ch = logging.StreamHandler()
    # ch.setLevel(logging.INFO)
    # ch.setFormatter(logging.Formatter("%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    # logger.addHandler(ch)

    event_handler = Handler(path, logger)

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while observer.is_alive():
            await asyncio.sleep(1)
    finally:
        observer.stop()
        observer.join()


async def main() -> None:
    dirs_to_monitor: list[str] = ["./data/dir1", "./data/dir2", "./data/dir3"]
    monitors: list[asyncio.Task] = []
    for dir in dirs_to_monitor:
        monitors.append(asyncio.create_task(monitor_directory(dir)))

    await asyncio.gather(*monitors)


if __name__ == "__main__":
    asyncio.run(main())
