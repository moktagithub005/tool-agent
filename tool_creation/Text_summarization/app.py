import streamlit as st
import validators
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# Streamlit UI
st.set_page_config(page_title="LangChain: Summarize Text From YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From YT or Website")
st.subheader("Summarize a YouTube video or Website URL")

# Sidebar input for Groq API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

# URL input field
generic_url = st.text_input("Enter a YouTube or Website URL", label_visibility="visible")

# Prompt Template
prompt_template = """
Provide a clear, concise 300-word summary of the following content:
{text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# Summarization logic
if st.button("Summarize the Content"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both the Groq API key and a valid URL.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (YouTube or website).")
    else:
        try:
            with st.spinner("Loading and summarizing content..."):
                # Load content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) "
                                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                                          "Chrome/116.0.0.0 Safari/537.36"
                        }
                    )
                docs = loader.load()

                # Initialize Groq LLM
                llm = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)

                # Load summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                # Display result
                st.success("Summary:")
                st.write(output_summary)

        except Exception as e:
            import traceback
            st.error("An error occurred:")
            st.text(str(e))
            st.text(traceback.format_exc())
