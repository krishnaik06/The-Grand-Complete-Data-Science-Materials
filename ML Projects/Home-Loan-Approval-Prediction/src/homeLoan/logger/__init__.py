import logging
import os


os.makedirs('logs', exist_ok=True)
log_file_path = os.path.join('logs', 'running_logs.log')

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s : %(name)s - %(levelname)s - %(message)s',
    handlers = [
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)