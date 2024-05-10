import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Load environment variables from a .env file using python-dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY", "")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY", "")

# Set environment variables related to LangChain tracing and project
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "RAG Sample"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Specify the directory where FAISS vector store data is located
vectorstore_dir = "./vectorstore_faiss"

# Load the FAISS vector store if both the index files are present
if os.path.exists(os.path.join(vectorstore_dir, "index.faiss")) and os.path.exists(os.path.join(vectorstore_dir, "index.pkl")):
    vectorstore = FAISS.load_local(
        vectorstore_dir,
        OpenAIEmbeddings(),
        allow_dangerous_deserialization=True  # Enable potentially dangerous deserialization
    )
else:
    # Raise an error if the vector store files are missing
    raise ValueError(f"FAISS vector store not found at {vectorstore_dir}. Please ensure it's created and populated.")

# Create a retriever from the FAISS vector store
retriever = vectorstore.as_retriever()

# Define an improved prompt template for generating answers
improved_prompt_template = """You are an AI assistant specialized in helping with web application development tasks.
You are given a set of retrieved documents that are related to web application development.
Provide a comprehensive and detailed answer to the given question using the provided context.
If the provided context is insufficient, clearly mention what additional information is needed.

Please always specify the source of the material at the end. The source is included in the metadata in JSON format. Format the citation in markdown for better readability.

Question: {question}

Retrieved Documents:
{context}

Detailed Answer:
"""

# Create a prompt object from the improved prompt template
prompt = ChatPromptTemplate.from_template(improved_prompt_template)

# Streamlit UI for the Kysely QA application
st.title("Kysely Docs QA App")

# Initialize session state variables for question, result, and API key input
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "result" not in st.session_state:
    st.session_state["result"] = ""
if "custom_openai_key" not in st.session_state:
    st.session_state["custom_openai_key"] = ""

# Dropdown selection for choosing the LLM model
model = st.selectbox(
    "Choose LLM Model:",
    ["gpt-3.5-turbo", "gpt-4-turbo"]
)

# Text input for the custom OpenAI API key
custom_openai_key = st.text_input(
    "Enter a custom OpenAI API key to override the default key, or leave blank to use the default key:",
    st.session_state["custom_openai_key"]
)

# Update the session state with the custom API key
st.session_state["custom_openai_key"] = custom_openai_key

# Determine the API key to use, prioritizing the custom key if provided
api_key_to_use = custom_openai_key if custom_openai_key else openai_api_key

# Set up the ChatOpenAI model with the selected LLM and API key
llm = ChatOpenAI(model=model, openai_api_key=api_key_to_use)

# Create a RAG (retrieval-augmented generation) chain with the retriever, prompt, and LLM
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Text input for users to ask their questions
question = st.text_input("Ask a question:", value=st.session_state["question"])

# Update the session state with the latest question input
st.session_state["question"] = question

# Button to trigger answer generation
if st.button("Generate Answer"):
    with st.spinner("Generating answer..."):
        # Generate the answer and update session state
        st.session_state["result"] = rag_chain.invoke(st.session_state["question"])

# Display the generated result
st.write(st.session_state["result"])
