from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory, RunnableParallel, RunnableLambda
from loguru import logger

from app.models.prompt_template import PromptTemplate
from app.utils.history_message import history_message_manager
from app.utils.vector import vector_manager


class ChainManager:
    def __init__(self):
        self.prompt_template = None
        self.llm = None
        self.chain_dict = {}

    def _create_chain(self, prompt_template: PromptTemplate, llm, chain_key, embeddings):
        vector_store = vector_manager.get_vector("默认知识库", embeddings, async_mode=True)
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 6})

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_template.content),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        self.llm = llm

        chain = (
            RunnableParallel({
                "input": lambda x:x["input"] ,
                "context": RunnableLambda(lambda x:x["input"]) | retriever | self.format_docs,
                # "context": RunnableLambda(lambda x: x["input"]),
                "history": lambda x:x["history"]
            })
            | history_message_manager.limit_history_messages
            # | self.debug_params
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

    def get_chain(self, prompt_template: PromptTemplate, llm, embeddings):
        llm_name = llm.model if hasattr(llm, "model") else llm.model_name
        chain_key = f"{llm_name}_{prompt_template.name}"
        chain = self.chain_dict.get(chain_key)
        if chain is None:
            chain = self._create_chain(prompt_template, llm, chain_key, embeddings)
        return chain

    @staticmethod
    def debug_params(x):
        logger.info("整合历史对话记录")
        print(x)
        return x

    @staticmethod
    def format_docs(docs):
        logger.info("整合知识库检索结果")
        doc_str = "\n\n".join([doc.page_content for doc in docs])
        return doc_str


chain_manager = ChainManager()
