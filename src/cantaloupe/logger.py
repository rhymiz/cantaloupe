import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s [%(levelname)s] - %(message)s",
)


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Returns a logger with the given name.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
