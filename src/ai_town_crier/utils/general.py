import datetime
from datetime import timedelta
from utils.logger import get_logger
import json
import string

logger = get_logger(__name__)


def get_day_datetime():
    logger.info('Calculating datetime')
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    logger.debug(f'Datetime: {today}')
    return today


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


def add_to_dict(main_dict, list1, list2):
    if len(list1) != len(list2):
        raise ValueError('Lists must be the same length')
    if main_dict is None:
        main_dict = {}
    main_dict.update(dict(zip(list1, list2)))
    return main_dict


def load_dict_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def save_dicts_to_json(dicts, file_path):
    logger.info(f'Saving dictionary to {file_path}')
    with open(file_path, 'w') as f:
        json.dump(dicts, f)


def load_list_from_txt(file_path):
    logger.info(f'Loading {file_path} locally')
    with open(file_path, 'r') as file:
        tweets = file.readlines()
    return [tweet.strip() for tweet in tweets]


def save_list_to_txt(file_path, data_list):
    logger.info(f'Saving file locally to {file_path}')
    with open(file_path, 'w') as file:
        for item in data_list:
            file.write(str(item) + '\n')

def check_string(s, val):
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = s.replace(" ", "")
    s = s.upper()
    return s == val