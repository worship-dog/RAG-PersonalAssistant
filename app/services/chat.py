from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified

from app.models import Chat, Embeddings, LLM, PromptTemplate
from app.utils.chain import chain_manager
from app.utils.database import AsyncSession, Session


class ChatManager:
    def __init__(self):
        self.llm_dict = {}
        self.embedding_dict = {}
        self.prompt_dict  = {}

    async def astream_generate_answer(
            self,
            timer,
            session: AsyncSession,
            conversation_id: str,
            chat_id: str,
            question: str,
            llm_id: str=None,
            prompt_template_id: str=None
    ):
        # 初始化大语言模型
        if llm_id in self.llm_dict:
            llm_chat = self.llm_dict[llm_id]
        else:
            llm: LLM|None = await session.get(LLM, llm_id)
            # DB模型转为Chat模型
            llm_chat = llm.init()
            self.llm_dict.setdefault(llm_id, llm_chat)

        # 初始化嵌入模型
        if self.embedding_dict:
            embeddings = list(self.embedding_dict.values())[0]
        else:
            stmt = select(Embeddings).where(Embeddings.default == True)
            select_result = await session.execute(stmt)
            embeddings = select_result.scalars().first()
            # DB模型转为Embeddings模型
            embeddings = embeddings.init()
            self.embedding_dict.setdefault(embeddings.model, embeddings)

        # 初始化提示词模板
        if prompt_template_id:
            prompt_template: PromptTemplate|None = await session.get(PromptTemplate, prompt_template_id)
        else:
            prompt_template = PromptTemplate()
            prompt_template.name = "默认"
            prompt_template.content = """
你是一个智能助手
"""
        prompt_template.content += """
请根据上下文和历史对话帮助用户解答问题
**上下文**  
{context}

使用markdown进行格式化输出
"""
        timer.start_timer()  # 开始思考计时
        chain = chain_manager.get_chain(prompt_template, llm_chat, embeddings)
        async for token in chain.astream(
            input={"input": question},
            config={"configurable": {"session_id": conversation_id}}
        ):
            yield token

    @staticmethod
    async def save_chat(session: AsyncSession, answer, think_time, **data):
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
    
    @staticmethod
    def get_chats(session: Session, conversation_id):
        chat_list = session.query(Chat.chat_content).filter_by(
            conversation_id=conversation_id
        ).order_by(Chat.create_time).all()
        return [chat.chat_content for chat in chat_list]


chat_manager = ChatManager()