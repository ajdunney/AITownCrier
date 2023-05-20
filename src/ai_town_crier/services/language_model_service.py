import os

from utils.logger import get_logger
from utils.general import read_file_to_string, join_strings_with_newline
from services.news_manager import NewsManager
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate

logger = get_logger(__name__)


class AITownCrier:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv('OPENAI_API_KEY'))

    def prompt(self, text):
        print(self.llm(text))


if __name__ == '__main__':
    # model = AITownCrier()
    #model.prompt('Hello town crier. How are you doing?')
    startup = read_file_to_string('resources/startup_template.txt')
    news_manager = NewsManager('resources/data.json')
    for batch in news_manager.get_titles(5):
        # print(batch)
        break

    batch_str = join_strings_with_newline(batch)
    no_input_prompt = PromptTemplate(input_variables=['news'], template=startup)
    prompt = no_input_prompt.format(news='')

    print(prompt)
    model = AITownCrier()
    model.prompt(prompt)
    # model.prompt(prompt)
