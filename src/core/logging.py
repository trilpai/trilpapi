import logging
from logging.config import dictConfig
from src.core.config import settings

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",  # Log file location
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",  # Default level, overridden by settings
        "handlers": ["file", "console"],
    },
}

def setup_logging():
    """
    Configures logging for the application.

    The logging level is dynamically set based on the LOG_LEVEL specified
    in the application's settings (defaults to INFO).
    """
    log_level = settings.log_level.upper() if hasattr(settings, 'log_level') else "INFO"

    # Update the root logger level dynamically based on settings
    LOGGING_CONFIG["root"]["level"] = log_level

    dictConfig(LOGGING_CONFIG)
