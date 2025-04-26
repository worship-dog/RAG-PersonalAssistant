from langchain_ollama import OllamaLLM

from app.models import LLM, PromptTemplate
from app.utils.chain import chain_manager
from app.utils.database import AsyncSessionLocal


class ChatManager:
    async def astream_generate_answer(
            self,
            session: AsyncSessionLocal,
            conversation_id: str,
            chat_id: str,
            question: str,
            llm_id: str=None,
            prompt_template_id: str=None
    ):
        # 初始化大语言模型
        llm: LLM = await session.get(LLM, llm_id)
        # DB模型转为OllamaLLM模型
        llm: OllamaLLM = llm.init()

        # 初始化提示词模板
        if prompt_template_id:
            prompt_template: PromptTemplate = await session.get(PromptTemplate, prompt_template_id)
        else:
            prompt_template = PromptTemplate()
            prompt_template.name = "默认"
            prompt_template.content = "你是一个智能助手，帮助用户解答以下问题"

        chain = chain_manager.get_chain(prompt_template, llm)
        async for token in chain.astream(input={"input": question}):
            yield f"data: {token}\n\n"  # 以SSE格式返回回答


chat_manager = ChatManager()