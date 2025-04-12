# organizer/logger.py

import logging
from pathlib import Path


def setup_logger(log_file: Path = Path("pyorganizer.log")) -> logging.Logger:
    """
    Configures and returns a logger that writes to both console and a file.

    Args:
        log_file (Path): Path to the log file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("PyOrganizer")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs if setup_logger is called multiple times
    if logger.hasHandlers():
        return logger

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
