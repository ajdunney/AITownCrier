import json
from utils.logger import get_logger
logger = get_logger(__name__)


class NewsManager:
    def __init__(self, filepath):
        logger.debug('Creating NewsManager')
        self.filepath = filepath
        self.titles = []
        self.load_data()

    def load_data(self):
        logger.debug(f'Opening data at {self.filepath}')
        try:
            with open(self.filepath, 'r') as file:
                data = json.load(file)
            self.process_data(data)
        except json.JSONDecodeError:
            logger.error(f"File {self.filepath} is not a valid JSON.")
        except FileNotFoundError:
            logger.error(f'File not found {self.filepath}.')

    def process_data(self, data):
        logger.debug('Processing data')
        assert isinstance(data, list)
        for item in data:
            if 'filename' in item:
                logger.debug(f'Appending {item}')
                self.titles.append(item['filename'])

    def get_titles(self, chunk_size=5):
        for i in range(0, len(self.titles), chunk_size):
            yield self.titles[i:i+chunk_size]

