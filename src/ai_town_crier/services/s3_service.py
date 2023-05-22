import os
import boto3
from botocore.exceptions import NoCredentialsError
from utils.logger import get_logger
from utils.general import get_day_datetime, save_dicts_to_json

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

        logger.info(f'{len(files)} files downloaded')

        if 'Contents' not in s3_objects:
            logger.warning('No objects found in S3')

    except NoCredentialsError as e:
        logger.error(f'No AWS credentials found: {e}')


    return files


def get_articles(bucket, directory, save_dir):
    logger.info('Getting articles')
    news_stories = download_from_s3(bucket, directory)
    save_dicts_to_json(news_stories, save_dir)
    return


def upload_to_s3(bucket_name, input_filepath, destination_s3_folder):
    logger.info(f'Upload to S3 {bucket_name}, {input_filepath} -> {destination_s3_folder}')
    s3 = boto3.client('s3')
    filename = os.path.basename(input_filepath)
    logger.debug(filename)
    try:
        s3.upload_file(input_filepath, bucket_name, os.path.join(destination_s3_folder, filename))
        print('Upload complete')
    except NoCredentialsError:
        print('No AWS credentials found.')
    except:
        print('Some other error occured')
    return


if __name__ == '__main__':
    get_articles(bucket='medieval-news-press',
                 directory=os.path.join('articles', get_day_datetime()),
                 save_dir='resources/data.json')
