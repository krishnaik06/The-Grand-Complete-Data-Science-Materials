import os
import sys
import logging

# Format of the log
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Location of the log
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")

# Making the log directory
os.makedirs(log_dir, exist_ok=True)

# Making the logging function
logging.basicConfig(
    level=logging.INFO, 
    format=logging_str, 
    handlers=[
        # To add the log in the log file
        logging.FileHandler(log_filepath),

        # To print the log in the terminal at the time of generation
        logging.StreamHandler(sys.stdout)
    ]
)

# Naming the logger as cnnClassifierLogger
logger = logging.getLogger("titanicLogger")
