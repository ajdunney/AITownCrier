import tweepy
import os
from utils.logger import get_logger
from services.s3_service import download_file_from_s3, list_jpgs, upload_to_s3
from utils.general import load_dict_from_json, get_day_datetime, load_list_from_txt, save_list_to_txt

logger = get_logger(__name__)


class TwitterBot:
    logger.info('Creating AITownCrier')

    def __init__(self):
        self._bearer_token = None
        self._api_key = None
        self._api_key_secret = None
        self._access_token = None
        self._access_token_secret = None

        use_aws = False
        if use_aws:
            raise NotImplementedError
        else:
            self._bearer_token = os.getenv('BEARER_TOKEN')
            self._api_key = os.getenv('CONSUMER_KEY')
            self._api_key_secret = os.getenv('CONSUMER_SECRET')
            self._access_token = os.getenv('ACCESS_TOKEN')
            self._access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

        self.client = tweepy.Client(self._bearer_token, self._api_key, self._api_key_secret, self._access_token,
                                    self._access_token_secret)

        self.auth = tweepy.OAuthHandler(self._api_key, self._api_key_secret)
        self.auth.set_access_token(key=self._access_token, secret=self._access_token_secret)
        self.api = tweepy.API(self.auth)

    @staticmethod
    def get_todays_tweets(bucket_name):
        today = get_day_datetime()
        local_tweet_path = 'resources/tweets.txt'

        filepath = os.path.join('outputs', today, 'tweets.txt')
        try:
            download_file_from_s3(bucket_name=bucket_name, s3_file_name=filepath,
                                  local_file_name=local_tweet_path)
        except FileNotFoundError:
            return []

        return load_list_from_txt(local_tweet_path)

    def post_tweet(self, text, ids):
        self.client.create_tweet(text=text, media_ids=ids)


def run_bot(bucket_name, news_data, clean_data_path):
    bot = TwitterBot()

    local_clean_path = 'resources/outputs_clean_dl.json'

    download_file_from_s3(bucket_name, clean_data_path, local_clean_path)
    clean_dict = load_dict_from_json(local_clean_path)

    past_tweets = TwitterBot.get_todays_tweets(bucket_name)

    today = get_day_datetime()

    imgs = list_jpgs(bucket_name, os.path.join('outputs', today))
    if not imgs:
        logger.info('No images ready to publish. Exiting.')
        return

    imgs_output_dict = {}
    for filename in imgs:
        if filename.split('/')[-1] in clean_dict:
            imgs_output_dict[filename] = clean_dict[filename.split('/')[-1]]
            logger.info(f'{filename} found in clean outputs')

    for key, value in imgs_output_dict.items():
        if key in past_tweets:
            logger.info(f'{value} already posted today.')
        else:
            local_img_path = os.path.join('resources', os.path.basename(key))
            download_file_from_s3(bucket_name=bucket_name, s3_file_name=key, local_file_name=local_img_path)
            ret = bot.api.media_upload(local_img_path)
            logger.info(f'Posting {value}')
            bot.post_tweet(text=value, ids=[ret.media_id_string])
            past_tweets.append(value)
            past_tweets.append(key)
            local_tweet_path = 'resources/tweets.txt'
            save_list_to_txt(local_tweet_path, past_tweets)
            upload_to_s3(bucket_name=bucket_name,
                         input_filepath=local_tweet_path,
                         destination_s3_folder=os.path.join('outputs', today))
            return
