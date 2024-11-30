import logging
import sys
from pathlib import Path
from typing import Optional

def setup_logger(log_file: Optional[Path] = None, debug_mode: bool = False) -> logging.Logger:
    """Configure application-wide logging with console and optional file output.
    
    Args:
        log_file: Optional path to log file
        debug_mode: Whether to enable debug logging
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger('fl_cubase_migration')
    logger.setLevel(logging.DEBUG if debug_mode else logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    file_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler if log_file is specified
    if log_file:
        try:
            # Ensure directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
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
    logger = logging.getLogger('fl_cubase_migration')
    
    # If logger has no handlers, set up a basic configuration
    if not logger.handlers:
        setup_logger()
        
    return logger

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