from utils.logger import get_logger
import argparse
import os
from services.s3_service import get_articles, upload_to_s3
from services.language_model_service import run_town_crier
from services.twitter_bot import run_bot
from utils.general import get_day_datetime

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='AI Town Crier')
    parser.add_argument('--service', type=str, help='Service to initialize (llm or twitter)')
    args = parser.parse_args()
    service = args.service
    logger.info(f'Running script with {service}')

    day_string = get_day_datetime()

    bucket_name = 'medieval-news-press'
    news_data = 'resources/data.json'

    get_articles(bucket=bucket_name,
                 directory=os.path.join('articles', day_string),
                 save_dir=news_data)

    if service == 'llm':
        llm_output = 'resources/outputs.json'
        llm_clean_output = 'resources/outputs_clean.json'
        run_town_crier(raw_input_path=news_data,
                       raw_output_path=llm_output,
                       clean_output_path=llm_clean_output)
        upload_to_s3(bucket_name=bucket_name,
                     input_filepath=llm_clean_output,
                     destination_s3_folder=os.path.join('outputs/', day_string))

    elif service == 'twitter':
        clean_data_path = os.path.join('outputs', day_string, 'outputs_clean.json')
        run_bot(bucket_name, news_data, clean_data_path)
    else:
        print(f'Unknown service: {service}')


if __name__ == '__main__':
    main()
