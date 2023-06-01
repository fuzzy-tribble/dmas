import sys
import signal
import time
from contextlib import contextmanager

from utils import logger

shutting_down = False

@contextmanager
def sigterm_handler():
    """Handle SIGTERM gracefully."""
    def _handler(signum, frame):
        global shutting_down
        logger.info("SIGTERM received. Preparing to exit gracefully.")
        shutting_down = True
        
        # if needed, add extra time for ongoing operations to complete
        time.sleep(5)
        
        sys.exit(0)

    # Register the handler for SIGTERM
    original_sigterm_handler = signal.signal(signal.SIGTERM, _handler)
    try:
        yield
    finally:
        # Restore the original handler
        signal.signal(signal.SIGTERM, original_sigterm_handler)
