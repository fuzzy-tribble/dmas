"""Main entry point for the application.""" ""
import os
import asyncio
import signal
import sys
import time

from contextlib import contextmanager
from subscriber import Subscriber

from utils import Logger
from shutdown_manager import shutting_down

current_file_dir = os.path.dirname(os.path.abspath(__file__))
logger = Logger(current_file_dir, "subscriber").logger

@contextmanager
def sigterm_handler():
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


if __name__ == "__main__":
    try:
        preproc = Preprocessor(logger)
        preproc.setup()
        
        # start the loop in a context manager to handle clean exit
        with sigterm_handler():
            while not shutting_down:
                preproc.run()
                
        if shutting_down:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(preproc.shutdown())
    
    except Exception as e:
        logger.critical(f"Subscriber failed to start main with error: \n{e}", exc_info=True)
