from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import OllamaLLM

from app.models.prompt_template import PromptTemplate


def debug_params(x):
    print(x)
    return x

class ChainManager:
    def __init__(self):
        self.prompt_template = None
        self.llm = None
        self.chain_dict = {}

    def _create_chain(self, prompt_template: PromptTemplate, llm: OllamaLLM):
        chain_key = f"{llm.model}_{prompt_template.name}"
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template.content),
            # MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.llm = llm

        chain = (
            self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        self.chain_dict.setdefault(chain_key, chain)

        return chain

    def get_chain(self, prompt_template: PromptTemplate, llm: OllamaLLM):
        chain_key = f"{llm.model}_{prompt_template.name}"
        chain = self.chain_dict.get(chain_key)
        if chain is None:
            chain = self._create_chain(prompt_template, llm)
        return chain


chain_manager = ChainManager()
