from utils.logger import get_logger
import argparse
import os
from services.s3_service import get_articles, upload_to_s3
from services.language_model_service import run_town_crier
from utils.general import get_day_datetime

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description='AI Town Crier')
    parser.add_argument('--service', type=str, help='Service to initialize (llm or twitter)')
    args = parser.parse_args()
    service = args.service
    logger.info(f'Running script with {service}')
    if service == 'llm':
        news_data = 'resources/data.json'
        llm_output = 'resources/outputs.json'
        llm_clean_output = 'resources/outputs_clean.json'

        get_articles(bucket='medieval-news-press',
                     directory=os.path.join('articles', get_day_datetime()),
                     save_dir=news_data)
        run_town_crier(raw_input_path=news_data,
                       raw_output_path=llm_output,
                       clean_output_path=llm_clean_output)
        upload_to_s3(bucket_name='medieval-news-press',
                     input_filepath=llm_clean_output,
                     destination_s3_folder=os.path.join('outputs/', get_day_datetime()))
    elif service == 'twitter':
        # Initialize twitter service
        pass
    else:
        print(f'Unknown service: {service}')


if __name__ == '__main__':
    main()
