from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
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

    def __create_chain(self, prompt_template: PromptTemplate, llm: OllamaLLM):
        chain_key = f"{llm.model}_{prompt_template.name}"
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template.content),
            ("human", "{input}")
        ])
        self.llm = llm

        chain = (
            RunnablePassthrough()
            # | RunnableLambda(debug_params)
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )
        self.chain_dict.setdefault(chain_key, chain)

        return chain

    def get_chain(self, prompt_template: PromptTemplate, llm: OllamaLLM):
        chain_key = f"{llm.model}_{prompt_template.name}"
        chain = self.chain_dict.get(chain_key)
        if chain is None:
            chain = self.__create_chain(prompt_template, llm)
        return chain


chain_manager = ChainManager()
