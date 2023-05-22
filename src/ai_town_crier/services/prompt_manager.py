from utils.general import read_file_to_string
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


class PromptManager():
    def __init__(self, startup_path):
        self.start_prompt = read_file_to_string(startup_path)
        self.system_message_prompt = SystemMessagePromptTemplate.from_template(self.start_prompt)
        self.human_template = "{text}"
        self.human_message_prompt = HumanMessagePromptTemplate.from_template(self.human_template)

    def create_chat_prompt(self, *args):
        return ChatPromptTemplate.from_messages([self.system_message_prompt, self.human_message_prompt] + list(args))
