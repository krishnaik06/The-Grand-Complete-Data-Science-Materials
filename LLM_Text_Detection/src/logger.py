'''
file: logger.py

This file is used for logging all logs or recording all steps execution in a separate file.
Here, we first create a log file at the beginning of code execution, and this file will now take record of all logs generated during program execution.
'''

# Required modules
import os
import logging
from datetime import datetime

# Defining a new folder for all log files "Project_logs"
LOGS_PATH = os.path.join(os.getcwd(), 'LOGS')

# Checking whether a folder exists or not in the project folder; if not, create this folder directory
if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH, exist_ok=True)

# Log file name and its path
log_file_name = f"{datetime.now().strftime('%Y_%m_%d %H_%M_%S')}.log"
log_file_path = os.path.join(LOGS_PATH, log_file_name)

# Creating a log file
with open(log_file_path, 'w'):
    pass

# Configuring log format with logging.basicConfig()
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
