"""Define the different verbosity of the logs.
"""

_log_level = 1  # pylint: disable=invalid-name
"""Verbosity level"""

NONE = 0
INFO = 1
DEBUG = 2


def set_verbosity(log_level: int):
    """Define verbosity level.

    Parameters
    ----------
    log_level : int
        log level

    Raises
    ------
    ValueError
        if not in range [NONE;DEBUG]
    """
    global _log_level  # pylint: disable=invalid-name,global-statement
    if not NONE <= log_level <= DEBUG:
        raise ValueError(f"log_level must be in [{NONE};{DEBUG}]")
    _log_level = log_level


def get_log_level():
    """Access to current log level."""
    return _log_level


def log(level, *args, **kwargs):
    """log basis function"""
    if level >= DEBUG and "flush" not in kwargs:
        kwargs["flush"] = True
    if _log_level >= level:
        print(*args, **kwargs)


def info(*args, **kwargs):
    """Log info level. Use it as print function."""
    log(INFO, *args, **kwargs)


def debug(*args, **kwargs):
    """Log debug level. Use it as print function."""
    log(DEBUG, *args, **kwargs)
