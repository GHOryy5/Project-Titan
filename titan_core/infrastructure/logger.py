import logging
import os
from datetime import datetime

class TitanLogger:
    def __init__(self):
        # Setup a secure log file
        self.log_file = "titan_audit.log"
        logging.basicConfig(filename=self.log_file, level=logging.INFO, 
                           format='%(asctime)s - %(levelname)s - %(message)s')

    def log_op(self, module, action, status="SUCCESS"):
        """
        Writes a structured log entry.
        """
        msg = f"[{module}] Action: {action} | Status: {status}"
        logging.info(msg)
        # Also print to a hidden debug stream if needed
