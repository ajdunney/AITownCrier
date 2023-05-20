import os
import boto3
from botocore.exceptions import NoCredentialsError
from utils.logger import get_logger
from utils.general import get_week_datetime
import json

logger = get_logger(__name__)


def download_from_s3(bucket_directory, directory):
    logger.info('Connecting to S3')
    files = []
    s3 = boto3.client('s3')
    dir_prefix = os.path.join(directory, 'images/')
    try:
        logger.debug(f'Trying to list objects in {dir_prefix}')
        s3_objects = s3.list_objects_v2(Bucket=bucket_directory, Prefix=dir_prefix)

        for object in s3_objects['Contents']:
            logger.debug(f'Adding {object["Key"]} to list')
            files.append({"filename": object['Key'].rsplit('/', 1)[-1], "filepath": object['Key']})

        if 'Contents' not in s3_objects:
            logger.warning('No objects found in S3')

    except NoCredentialsError as e:
        logger.error(f'No AWS credentials found: {e}')

    return files


def save_dicts_to_json(dicts, file_path):
    logger.info(f'Saving dictionary to {file_path}')
    with open(file_path, 'w') as f:
        json.dump(dicts, f)


if __name__ == '__main__':
    bucket_name = 'medieval-news-press'
    directory = os.path.join('articles', get_week_datetime())
    save_dir = 'resources/data.json'
    news_stories = download_from_s3(bucket_name, directory)
    save_dicts_to_json(news_stories, save_dir)
