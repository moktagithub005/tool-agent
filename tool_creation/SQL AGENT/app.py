import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq

# Page setup
st.set_page_config(page_title="LangChain SQL Chatbot", page_icon="🤖")
st.title("🤖 LangChain SQL Chatbot")

# Database selection
radio_opt = ["Use SQLite (chatbot.db)", "Use MySQL Database"]
selected_opt = st.sidebar.radio("Choose the DB you want to use", radio_opt)

USE_SQLITE = "sqlite"
USE_MYSQL = "mysql"

if selected_opt == radio_opt[0]:
    db_type = USE_SQLITE
else:
    db_type = USE_MYSQL

# Groq API Key input
api_key = st.sidebar.text_input("Groq API Key", type="password")

# MySQL config (only shown if MySQL selected)
if db_type == USE_MYSQL:
    st.sidebar.markdown("---")
    st.sidebar.subheader("MySQL Configuration")
    mysql_host = st.sidebar.text_input("Host", value="localhost")
    mysql_user = st.sidebar.text_input("User", value="root")
    mysql_password = st.sidebar.text_input("Password", type="password")
    mysql_db = st.sidebar.text_input("Database", value="chatbot")

# Ensure all inputs are filled
if not api_key:
    st.warning("Please enter the Groq API key.")
    st.stop()

if db_type == USE_MYSQL and not (mysql_host and mysql_user and mysql_password and mysql_db):
    st.warning("Please enter all MySQL details.")
    st.stop()

# Create LLM
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# Function to configure the selected DB
@st.cache_resource(ttl="2h")
def configure_database():
    if db_type == USE_SQLITE:
        db_path = Path(__file__).parent / "chatbot.db"
        uri = f"sqlite:///{db_path}"
        return SQLDatabase.from_uri(uri)
    else:
        uri = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"
        return SQLDatabase.from_uri(uri)

# Try to load DB
try:
    db = configure_database()
except Exception as e:
    st.error(f"❌ Could not connect to the database: {e}")
    st.stop()

# Setup agent
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# Chat history
if "messages" not in st.session_state or st.sidebar.button("Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "👋 How can I help you with your database?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_query = st.chat_input("Ask something about your database...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[streamlit_callback])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        except Exception as e:
            st.error(f"💥 Error: {e}")
