import logging
import os
import tempfile

from servicepathmapper.common.logger import Logger


def test_logger_console_and_file(monkeypatch):
    # Remove all handlers before test to ensure a clean state
    Logger._logger.handlers.clear()

    # 1. Test console logger
    Logger.create_console_logger()
    # Should only add one StreamHandler
    stream_handlers = [h for h in Logger._logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(stream_handlers) == 1

    # 2. Test log method
    Logger.log("Test console log", level=logging.ERROR)

    # 3. Test file logger
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        log_path = tmpfile.name

    try:
        Logger.create_file_logger(log_path)
        file_handlers = [h for h in Logger._logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 1

        # Log a message to file
        test_message = "Test file log"
        Logger.log(test_message, level=logging.INFO)

        # Flush all handlers to ensure writing
        for handler in Logger._logger.handlers:
            handler.flush()

        # Check that the message is in the file
        with open(log_path, "r") as f:
            content = f.read()
            assert test_message in content

    finally:
        os.remove(log_path)
