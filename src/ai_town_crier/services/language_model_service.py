import os
import json
from utils.logger import get_logger
from utils.general import add_to_dict, save_dicts_to_json, check_string
from services.prompt_manager import PromptManager
from services.news_manager import NewsManager
from langchain.chat_models import ChatOpenAI
from langchain import LLMChain

logger = get_logger(__name__)


class AITownCrier:
    def __init__(self):
        logger.info('Creating AITownCrier')
        self.llm = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo", openai_api_key=os.getenv('OPENAI_API_KEY'))

    def chat_with_prompt(self, prompt, query):
        logger.info('Prompting AITownCrier')
        chain = LLMChain(llm=self.llm, prompt=prompt)
        return chain.run(query)


def run_town_crier(raw_input_path, raw_output_path, clean_output_path):
    logger.info('Running town crier')
    news_manager = NewsManager(raw_input_path)
    prompt_manager = PromptManager('resources/startup_template.txt')
    model = AITownCrier()
    d = None
    for _, batch in enumerate(news_manager.get_titles(5)):
        logger.debug(f'Batch: {batch}')
        print(batch)
        response = model.chat_with_prompt(prompt=prompt_manager.create_chat_prompt(), query=batch)
        print(response)
        logger.debug(f'Response {response}')
        response_list = [line for line in response.split('\n') if line.strip()]
        print(len(batch), len(response_list))
        d = add_to_dict(d, batch, response_list)
        if _ > 10:
            break
    save_dicts_to_json(d, raw_output_path)
    logger.info('Reopening outputs to check for sensitive content')
    with open(raw_output_path) as f:
        data = json.load(f)
    sensitivity_manager = PromptManager('resources/sensitivity_checker_template.txt')
    for key in list(data.keys()):
        print(key)
        response = model.chat_with_prompt(prompt=sensitivity_manager.create_chat_prompt(), query=key)
        print(response)
        if not check_string(response, 'OK'):
            del data[key]
    save_dicts_to_json(data, clean_output_path)