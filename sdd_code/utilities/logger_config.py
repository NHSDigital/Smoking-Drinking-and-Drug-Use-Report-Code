import logging
import logging.handlers
import sys

# Type hinting
from typing import Optional, Type
from types import TracebackType


def setup_logger(
    console_log_level: int = logging.INFO,
    file_name: Optional[str] = None,
    file_log_level: int = logging.DEBUG,
    catch_errors: bool = True,
) -> logging.Logger:
    """Create instance of a logger

    Parameters:
    -------
        console_log_level: int
            The level of log to output to the console, any of the standard logging
            levels
        file_name: str
            Optional, the name/path to the output logs, without a file extension.
            If none then  no log file will be created.
        file_log_level: int
            The level of log to output to the file, any of the standard logging
            levels
        catch_errors: Bool
            Replace python standard sys.excepthook with a new exception
            handler that sends them to the log, default of True
    Returns:
    -------
    logging.Logger
        A logging object
    """
    # Send warnings from warnings.warn to the log
    logging.captureWarnings(True)

    # Format and extended format to use in logger output
    basic_format = "[%(asctime)s - %(module)s:%(funcName)s - %(levelname)s] :: %(message)s"
    # Currently extended formats are all equal, but could add additional info if needed
    file_format = basic_format

    # Setup basic logger and console output, note that level here is the minimum
    # that will be output
    # Get root logger, we just want to log straight to the root
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Setup INFO logging to console
    console_hdlr = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(basic_format)
    console_hdlr.setFormatter(formatter)
    console_hdlr.setLevel(console_log_level)
    logger.addHandler(console_hdlr)

    # If passed a filename, setup file logs
    if file_name:
        log_hdlr = logging.FileHandler(file_name)
        formatter = logging.Formatter(file_format)
        log_hdlr.setFormatter(formatter)
        log_hdlr.setLevel(file_log_level)
        logger.addHandler(log_hdlr)

    if catch_errors:
        # Replaces excepthook with our own exception handler
        sys.excepthook = handle_exception
    return logger


def handle_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: TracebackType,
) -> None:
    """Sends uncaught exceptions to the log"""

    # Allow ending program using Ctrl + C
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger = logging.getLogger()

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


def clean_up_handlers(logger: logging.Logger):
    """Remove and close handlers, to avoid repeated output

    Parameters
    ----------
    logger : logging.Logger
        A logger

    Returns
    -------
    None.

    """
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.close()
        logger.removeHandler(handler)
