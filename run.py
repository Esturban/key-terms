
from ttk import process_files
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    data_folder = 'data'
    output_folder = 'output'
    process_files(data_folder, output_folder,logger)