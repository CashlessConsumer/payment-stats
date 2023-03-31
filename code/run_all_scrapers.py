import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import scraper_utils

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    start_time = datetime.now()

    logger.info('Starting all scrapers...')

    scraper_modules = scraper_utils.get_scraper_modules()

    for module in scraper_modules:
        logger.info(f'Running scraper: {module.__name__}')
        module.run()
        logger.info(f'Finished scraper: {module.__name__}')

    end_time = datetime.now()
    duration = end_time - start_time
    logger.info(f'Total duration: {duration}')


if __name__ == '__main__':
    # Create log directory
    Path('logs').mkdir(parents=True, exist_ok=True)

    # Configure logging to write to a log file
    log_filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
    log_filepath = os.path.join('logs', log_filename)
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    # Run the main function
    main()
