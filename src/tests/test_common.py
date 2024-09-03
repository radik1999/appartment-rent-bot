import datetime as dt
import logging
import time
from typing import Any, Callable, Dict, List, Tuple

import pytest

from common.utils import BraceMessage, CustomJsonFormatter, ExtraFormatter, LogTimer, Timer


@pytest.fixture
def log_record():
    return logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=10,
        msg="Test message",
        args=(),
        exc_info=None,
    )


def test_extra_formatter_format_time(log_record):
    formatter = ExtraFormatter()
    log_record.created = time.time()
    formatted_time = formatter.formatTime(log_record)
    assert formatted_time is not None
    assert isinstance(formatted_time, str)


def test_extra_formatter_format(log_record):
    formatter = ExtraFormatter()
    log_record.some_extra_attribute = "extra_value"
    formatted_message = formatter.format(log_record)
    assert "extra_value" in formatted_message
    assert "Test message" in formatted_message


def test_brace_message():
    message = BraceMessage("Hello, {}!", "world")
    assert str(message) == "Hello, world!"


def test_custom_json_formatter_process_log_record(log_record):
    formatter = CustomJsonFormatter()
    log_record.levelname = "INFO"
    log_record.asctime = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    processed_record = formatter.process_log_record(log_record.__dict__)
    assert processed_record["severity"] == "INFO"
    assert "timestamp" in processed_record
    assert "levelname" not in processed_record
    assert "asctime" not in processed_record


def test_custom_json_formatter_format_time(log_record):
    formatter = CustomJsonFormatter()
    log_record.created = time.time()
    formatted_time = formatter.formatTime(log_record)
    assert formatted_time.endswith("Z")


def test_timer():
    with Timer() as t:
        time.sleep(0.1)
    assert t.duration >= 0.1


def test_log_timer(monkeypatch: pytest.MonkeyPatch) -> None:
    log_messages: List[Tuple[str, Dict[str, Any]]] = []

    def mock_log_func(msg: str, *args: Any, **kwargs: Any) -> None:
        log_messages.append((msg, kwargs))

    # Patch the __init__ method of LogTimer to inject the mock_log_func
    def mock_init(
        self: LogTimer,
        _log_func: Callable[[str, Any], None],
        action_name: str,
        extra: Dict[str, Any] | None = None,
        log_start: bool = False,
    ) -> None:
        Timer.__init__(self)
        self.log_func = mock_log_func
        self.extra = {"action": action_name}
        if extra:
            self.extra.update(extra)
        self.log_start = log_start

    monkeypatch.setattr(LogTimer, "__init__", mock_init)

    with LogTimer(mock_log_func, "test_action", extra={"test": "test2"}, log_start=True) as lt:
        time.sleep(0.1)

    assert lt.duration >= 0.1
    assert len(log_messages) == 2

    start_msg, start_kwargs = log_messages[0]
    end_msg, end_kwargs = log_messages[1]

    assert start_msg == "Starting timed section..."
    assert "extra" in start_kwargs
    assert start_kwargs["extra"]["action"] == "test_action"

    assert end_msg == "Completed timed section"
    assert "extra" in end_kwargs
    assert end_kwargs["extra"]["action"] == "test_action"
    assert "time" in end_kwargs["extra"]
    assert end_kwargs["extra"]["time"] >= 0.1
