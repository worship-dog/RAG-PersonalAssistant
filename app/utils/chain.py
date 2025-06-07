from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory

from app.models.prompt_template import PromptTemplate
from app.utils.history_message import history_message_manager


def debug_params(x):
    print(x)
    return x


class ChainManager:
    def __init__(self):
        self.prompt_template = None
        self.llm = None
        self.chain_dict = {}

    def _create_chain(self, prompt_template: PromptTemplate, llm, chain_key):
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template.content),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.llm = llm

        chain = (
            history_message_manager.limit_history_messages
            | self.prompt_template
            | self.llm
            | StrOutputParser()
        )

        chain_with_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: history_message_manager.get_history_messages(session_id),
            input_messages_key="input",
            history_messages_key="history"
        )

        self.chain_dict.setdefault(chain_key, chain_with_history)

        return chain_with_history

    def get_chain(self, prompt_template: PromptTemplate, llm):
        llm_name = llm.model if hasattr(llm, "model") else llm.model_name
        chain_key = f"{llm_name}_{prompt_template.name}"
        chain = self.chain_dict.get(chain_key)
        if chain is None:
            chain = self._create_chain(prompt_template, llm, chain_key)
        return chain


chain_manager = ChainManager()
