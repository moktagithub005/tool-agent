# chatbot_core.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from dotenv import load_dotenv

load_dotenv()

# 1. Load the knowledge base
with open("unisole.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 2. Split text
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.create_documents([content])

# 3. Create embeddings
embedding = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embedding)

# 4. LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

# 5. LangChain memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    input_key="question"
)

# 6. RAG Chain
retriever = vectorstore.as_retriever()

rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=False
)

# 7. Ask function
def ask_question(query: str):
    return rag_chain.run({"question": query})
