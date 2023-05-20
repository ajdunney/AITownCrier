import datetime
from datetime import timedelta
from utils.logger import get_logger

logger = get_logger(__name__)


def get_week_datetime():
    logger.info('Calculating datetime')
    today = datetime.datetime.now()
    last_monday = today - timedelta(days=today.weekday())
    last_monday_str = last_monday.strftime('%Y-%m-%d')
    logger.debug(f'Datetime: {last_monday_str}')
    return last_monday_str


def read_file_to_string(filepath):
    logger.debug(f'Opening {filepath}')
    try:
        with open(filepath, 'r') as file:
            data = file.read()
        return data
    except FileNotFoundError as e:
        logger.error(f"Error finding {filepath}: {e}")
        return None


def join_strings_with_newline(list_of_strings):
    return '\n'.join(list_of_strings)

