from unittest.mock import MagicMock
from watchdog.events import FileSystemEvent

from fs_monitoring import Handler


async def test_handler_init() -> None:
    handler = Handler("some/path")
    assert handler._path == "some/path"


async def test_handler_on_created() -> None:
    handler = Handler("some/path")
    handler.logger = MagicMock()
    event = FileSystemEvent("some/path/file.txt", "CREATE")
    handler.on_created(event)
    assert handler.logger.info.call_count == 1


async def test_handler_on_deleted() -> None:
    handler = Handler("some/path")
    handler.logger = MagicMock()
    event = FileSystemEvent("some/path/file.txt", "DELETE")
    handler.on_deleted(event)
    assert handler.logger.info.call_count == 1


async def test_handler_on_moved() -> None:
    handler = Handler("some/path")
    handler.logger = MagicMock()
    event = FileSystemEvent("some/path/file.txt", "MOVE")
    handler.on_moved(event)
    assert handler.logger.info.call_count == 1


async def test_handler_on_modified() -> None:
    handler = Handler("some/path")
    handler.logger = MagicMock()
    first_event = FileSystemEvent("some/path")
    handler.on_modified(first_event)
    assert handler.logger.info.call_count == 0
    second_event = FileSystemEvent("some/path/test.txt", "MODIFY")
    handler.on_modified(second_event)
    assert handler.logger.info.call_count == 1
