import os
import sys
import traceback
import nltk
from dotenv import load_dotenv
from langchain import hub
from langchain_community.document_loaders import (
    DirectoryLoader, UnstructuredMarkdownLoader, UnstructuredHTMLLoader,
    JSONLoader, CSVLoader
)
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Download 'punkt' tokenizer data for text processing, if not already available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    print("Downloading 'punkt' tokenizer data...")
    nltk.download("punkt")

# Load environment variables from a .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")

# Output API keys to confirm they're loaded correctly
print("OpenAI API Key:", openai_api_key)
print("LangChain API Key:", langchain_api_key)

# Set environment variables for LangChain configuration
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "RAG Sample"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Specify the directory containing documents to be processed
documents = "./kysely"
if not os.path.exists(documents):
    sys.exit(1)  # Exit if the document directory doesn't exist

# Define the mapping of file types to their corresponding loader classes
file_loaders = {
    '**/*.md': UnstructuredMarkdownLoader,
    '**/*.html': UnstructuredHTMLLoader,
    '**/*.json': JSONLoader,
    '**/*.txt': UnstructuredMarkdownLoader,
    '**/*.csv': CSVLoader
}

# Load documents from the specified directory, based on file types
docs = []
for glob_pattern, loader_cls in file_loaders.items():
    try:
        # Special handling for JSON files to parse entire content
        if loader_cls == JSONLoader:
            loader = DirectoryLoader(
                documents,
                glob=glob_pattern,
                loader_cls=JSONLoader,
                loader_kwargs={"jq_schema": ".", "text_content": False},
                use_multithreading=True
            )
        else:
            # Load other document types
            loader = DirectoryLoader(
                documents,
                glob=glob_pattern,
                loader_cls=loader_cls,
                loader_kwargs={"skip_language_metadata": True},
                use_multithreading=True
            )
        # Append loaded documents to the main list
        docs.extend(loader.load())
    except Exception as e:
        print(f"Error loading files of type {glob_pattern}: {e}")
        # Uncomment the following line for more detailed debugging
        # traceback.print_exc()

# Create the vector store directory if it does not exist
vectorstore_dir = "./vectorstore_faiss"
if not os.path.exists(vectorstore_dir):
    os.makedirs(vectorstore_dir)

# Configure a text splitter to divide the documents into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Load the FAISS vector store from the directory, or create it if it doesn't exist
if os.path.exists(os.path.join(vectorstore_dir, "index")):
    # Load existing vector store
    vectorstore = FAISS.load_local(vectorstore_dir, OpenAIEmbeddings())
else:
    # Create a new vector store and save it to the specified directory
    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings()
    )
    vectorstore.save_local(vectorstore_dir)

# Configure a retriever to find the most relevant documents
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")  # Retrieve a prompt template from LangChain Hub

# Function to format the retrieved documents for display
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Set up a ChatOpenAI model using OpenAI's GPT-3.5 Turbo model
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=openai_api_key)
# Uncomment the following line to use GPT-4 Turbo instead
# llm = ChatOpenAI(model="gpt-4-turbo", openai_api_key=openai_api_key)

# Create a RAG chain combining the retriever, prompt, and language model
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
