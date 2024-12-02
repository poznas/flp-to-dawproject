# src/fl2cu/utils/logger.py
import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[Path] = None) -> logging.Logger:
    """Set up and configure logger.
    
    Args:
        log_file: Optional path to log file. If None, logs to console only.
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('fl2cu')
    
    if not logger.handlers:  # Only add handlers if none exist
        logger.setLevel(logging.DEBUG)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler (if requested)
        if log_file is not None:
            try:
                log_file = Path(log_file)
                log_file.parent.mkdir(parents=True, exist_ok=True)
                file_handler = logging.FileHandler(str(log_file))
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.error(f"Failed to set up file logging to {log_file}: {e}")
    
    return logger

def get_logger() -> logging.Logger:
    """Get the configured logger instance.
    
    Returns:
        Logger instance
    """
    return logging.getLogger('fl2cu')

def log_error(error: Exception, context: Optional[str] = None) -> None:
    """Log an error with optional context information.
    
    Args:
        error: Exception to log
        context: Optional context information
    """
    logger = get_logger()
    error_message = f"{error.__class__.__name__}: {str(error)}"
    if context:
        error_message = f"{context} - {error_message}"
    logger.error(error_message, exc_info=True)