# [RAG-PersonalAssistant](https://github.com/worship-dog/RAG-PersonalAssistant)

## 项目介绍  
这是一个简单且基础的RAG玩具项目
本项目使用Python开发，采用MVC架构，通过RESTful API与SSE连接进行数据交互  
主要技术框架如下：
1. FastAPI-后端服务器
2. Langchain-大语言模型框架
3. Sqlalchemy-数据库ORM框架

所用数据库如下：
1. PostgreSQL  
   安装 pgvector 扩展，支持向量嵌入、检索
2. Redis  
   用于缓存与大模型的交互记录，实现大模型记忆功能

## 功能模块介绍
### 聊天模块
#### 对话管理-conversation
支持对话CRUD操作
#### 聊天-chat
1. 使用SSE连接与大模型进行交互 
2. 支持使用指定大模型
3. 支持使用指定提示词模板
4. 支持大模型记忆功能
5. 首次交互时，根据交互内容为对话命名
6. 支持通过文件标签检索知识库文件，输入#触发
### 系统设置模块
#### 大模型管理-llm
1. 支持大模型CRUD操作
2. 支持Ollama部署与OpenAI部署的大模型
#### 嵌入模型管理-embeddings
1. 支持嵌入模型CRUD操作
2. 支持Ollama部署与OpenAI部署的嵌入模型
#### 提示词模板管理-prompt_template
支持提示词模板CRUD操作
#### 知识库管理-knowledge
支持知识库文件CRUD操作
支持多模态文件向量嵌入（txt/markdown/docx/pdf）

[在线试用地址](https://chat.worship-dog.site)  
tips: 服务器性能很差，仅用于展示效果

## 快速开始
1. 创建Python运行环境
   1. 安装[UV](https://uv.doczh.com/getting-started/installation/)
   2. 安装Python  
      `uv python install 3.12.9`
2. 创建数据库
   1. 安装[PostgreSQL](https://www.postgresql.org/download/)
   2. 建立数据库
   3. 安装[pgvector](https://github.com/pgvector/pgvector)扩展
   4. 安装[Redis](https://www.redis.net.cn/)
3. 运行项目
   1. 拉取项目代码（选择合适路径运行以下命令，例如：F:\Project\Github）  
      `git clone https://github.com/worship-dog/RAG-PersonalAssistant.git`
   2. 拷贝项目目录下/app/config_base.py为/app/config.py
   3. 修改数据库连接参数与其他配置参数
   4. 建立虚拟环境  
      `uv venv`
   5. 安装项目依赖  
      `uv pip install -r requirements.txt`
   6. 启动程序  
      `uv python run run.py`
   7. 访问页面  
      `http://localhost:8001`

## 作者的话
本项目非常适合用于入门Python后端开发与大模型应用开发(为什么是入门呢，因为作者水平有限)
你可以在此项目中学习和了解以下实际开发中的技术点和概念：
1. MVC架构  
   Model-模型 View-视图 Controller-控制器
2. RESTful API  
   Representational State Transfer 表述性状态转移
3. ORM  
   Object Relational Mapping 对象关系映射
4. LCEL  
   LangChain Expression Language LangChain表达式语言
5. Embedding-嵌入
6. Vector-向量

## 后续开发计划
1. 消息复制按钮
2. 回答中的代码提供复制按钮

