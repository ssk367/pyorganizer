# organizer/logger.py

import logging
from pathlib import Path


def setup_logger(
    log_file: Path = Path("pyorganizer.log"), level: str = "INFO"
) -> logging.Logger:
    logger = logging.getLogger("PyOrganizer")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
