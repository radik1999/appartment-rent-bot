import datetime as dt
import logging
import sys
import time
from typing import Any, Callable, OrderedDict

from pythonjsonlogger.jsonlogger import JsonFormatter


class ExtraFormatter(logging.Formatter):
    converter = dt.datetime.fromtimestamp
    RESERVED_ATTRS = {
        "args",
        "asctime",
        "created",
        "exc_info",
        "exc_text",
        "filename",
        "funcName",
        "levelname",
        "levelno",
        "lineno",
        "module",
        "msecs",
        "message",
        "msg",
        "name",
        "pathname",
        "process",
        "processName",
        "relativeCreated",
        "stack_info",
        "thread",
        "threadName",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.src_tz = None
        if "django" in sys.modules:
            self.src_tz = dt.datetime.now().astimezone().tzinfo

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        ct = self.converter(record.created)

        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%H:%M:%S")
            s = f"{t}.{int(record.msecs):03d}"
        return s

    def format(self, record: logging.LogRecord) -> str:
        s = super().format(record)

        parts = [
            f"{k}={v}"
            for k, v in record.__dict__.items()
            if k not in self.RESERVED_ATTRS and not (hasattr(k, "startswith") and k.startswith("_"))
        ]

        if parts:
            s = f'{s} | {", ".join(parts)}'

        return s


class BraceMessage:
    def __init__(self, fmt: str, *args: tuple, **kwargs: tuple):
        self.fmt = fmt
        self.args = args
        self.kwargs = kwargs

    def __str__(self):
        return self.fmt.format(*self.args, **self.kwargs)


class CustomJsonFormatter(JsonFormatter):
    converter = dt.datetime.fromtimestamp

    def process_log_record(self, log_record: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
        level = log_record.get("levelname")
        if level is not None:
            # Python logging level names match to cloud severity names.
            log_record["severity"] = level
            del log_record["levelname"]

        asctime = log_record.get("asctime")
        if asctime is not None:
            log_record["timestamp"] = asctime
            del log_record["asctime"]

        return log_record

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        ct = self.converter(record.created)
        return ct.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


class Timer:
    """
    Measure execution time of a code snippet. Usage:

    with Timer() as t:
        do_some_serious_job()
    print(t.duration)

    """

    def __init__(self):
        self.start: float | None = None
        self.finish: float | None = None

    def __enter__(self):
        self.start = time.monotonic()
        return self

    def __exit__(self, *_):
        self.finish = time.monotonic()

    @property
    def duration(self) -> float:
        return self.finish - self.start


class LogTimer(Timer):
    """
    Log execution time of a code snippet, optionally with starting message.
    Usage:

    with LogTimer(my_logger.info, 'serious job', True):
        do_some_serious_job()

    Will print:
    INFO: Starting timed section... | action=serious job
    INFO: Completed doing some serious job | action=serious job, time=...

    """

    def __init__(self, log_func: Callable, action_name: str, extra: dict | None = None, log_start: bool = False):
        super().__init__()
        self.log_func = log_func
        self.extra = {"action": action_name}
        if extra:
            self.extra.update(extra)
        self.log_start = log_start

    def __enter__(self):
        if self.log_start:
            self.log_func("Starting timed section...", stacklevel=2, extra=self.extra)
        super().__enter__()
        return self

    def __exit__(self, *_):
        super().__exit__()
        self.extra["time"] = round(self.duration, 3)
        self.log_func("Completed timed section", stacklevel=2, extra=self.extra)
