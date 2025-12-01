# app/core/logging_config.py
import logging
from .configs import settings


def configure_logging() -> None:
    """
    Simple global logging setup. Call this once at startup.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
