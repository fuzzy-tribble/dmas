"""Main entry point for mas"""
import sys
import time

from multi_agent_system import MultiAgentSystem
from utils import shutting_down, sigterm_handler, logger, MAS_UID

if __name__ == "__main__":
    try:
        # create multi-agent system instance (it will get all its info from the DB) this will setup internal messaging system and register handlers for essential perceptors. The mas is init'd with status "sleeping". To wake up, a manager sends a wake signal through default exteroceptor and the mas exteroceptor handlers will handle it and start the wake up procedure.
        mas = MultiAgentSystem(
          uid=MAS_UID,
        )
    
        # start the loop in a context manager to handle clean exit
        with sigterm_handler():
            while not shutting_down:
                mas.internal_messenger.broadcast({'heartbeat'})
                time.sleep(1)
    
    except Exception as error:
        logger.crictical("MultiAgentSystem (UID: %s) failed to start main with error: \n%s", MAS_UID, error, exc_info=True)
        sys.exit(1)