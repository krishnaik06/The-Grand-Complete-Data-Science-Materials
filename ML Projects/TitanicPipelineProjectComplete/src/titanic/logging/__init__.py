import os
import sys
import logging

# Format of the log that will be saved
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# LOGS directory
log_dir = "logs"

# Log filepath and then making the directory
log_filepath = os.path.join(log_dir, "running_logs.log")
os.makedirs(log_dir, exist_ok=True)

# Basic Configs of Logging
logging.basicConfig(
    level= logging.INFO,
    format=logging_str,

    handlers=[
        # It will save the log to the filepath
        logging.FileHandler(log_filepath),

        # It will print the log in the terminal
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("titanicLogger")