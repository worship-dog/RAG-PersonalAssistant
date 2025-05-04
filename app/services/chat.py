from langchain_ollama import OllamaLLM
from sqlalchemy.orm.attributes import flag_modified

from app.models import Chat, LLM, PromptTemplate
from app.utils.chain import chain_manager
from app.utils.database import AsyncSession, Session


class ChatManager:
    async def astream_generate_answer(
            self,
            session: AsyncSession,
            conversation_id: str,
            chat_id: str,
            question: str,
            llm_id: str=None,
            prompt_template_id: str=None
    ):
        # 初始化大语言模型
        llm: LLM|None = await session.get(LLM, llm_id)
        # DB模型转为OllamaLLM模型
        llm: OllamaLLM = llm.init()

        # 初始化提示词模板
        if prompt_template_id:
            prompt_template: PromptTemplate|None = await session.get(PromptTemplate, prompt_template_id)
        else:
            prompt_template = PromptTemplate()
            prompt_template.name = "默认"
            prompt_template.content = "你是一个智能助手，帮助用户解答以下问题"

        chain = chain_manager.get_chain(prompt_template, llm)
        async for token in chain.astream(input={"input": question}):
            yield token

    async def save_chat(self, session: AsyncSession, answer, think_time, **data):
        if data.get("chat_id"):
            chat = await session.get(Chat, data["chat_id"])
        else:
            chat = Chat(**data)
            chat.chat_content = {
                "human": data["question"],
                "ai": [],
                "system": data["prompt_template_id"]
            }
            session.add(chat)
        # answer为空时，表示只保存问题
        if answer != "":
            ai_content = {"llm": data["llm_id"], "answer": answer, "think_time": think_time}
            chat.chat_content["ai"].append(ai_content)
            flag_modified(chat, "chat_content")  # 标记chat_content被修改
        await session.commit()
        return chat.id
    
    def get_chats(self, session: Session, conversation_id):
        chat_list = session.query(Chat.chat_content).filter_by(
            conversation_id=conversation_id
        ).order_by(Chat.create_time).all()
        return [chat.chat_content for chat in chat_list]


chat_manager = ChatManager()