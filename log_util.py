# log_util.py
# A homemade logger. The logging module felt like "too much magic" in 2013.

import time

LOG_LINES: list[str] = []   # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Append a timestamped message to the in-memory log and print it."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-prefixed message (only when DEBUG is True)."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Write all buffered log lines to *path* (append mode) and clear the buffer."""
    f = open(path, "a")
    for line in LOG_LINES:
        f.write(line + "\n")
    f.close()
    del LOG_LINES[:]
