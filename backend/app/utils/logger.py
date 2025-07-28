import logging

# * Configuring Logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler()],
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


# ? Helper Functions


def log_debug(message: str, **kwargs):
    """Log debug message with optional extra data"""
    logger.debug(message, extra=kwargs)


def log_info(message: str, **kwargs):
    """Log info message with optional extra data"""
    logger.info(message, extra=kwargs)


def log_warning(message: str, **kwargs):
    """Log warning message with optional extra data"""
    logger.warning(message, extra=kwargs)


def log_error(message: str, **kwargs):
    """Log error message with optional extra data"""
    logger.error(message, extra=kwargs)
