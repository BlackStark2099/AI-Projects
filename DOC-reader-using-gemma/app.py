import os
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter  # For splitting text into chunks 
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate,PromptTemplate
from langchain_community.vectorstores import FAISS  # For FAISS vector store usage 
from langchain.chains import create_retrival_chain
from langchain_community.vectorstores import FAISS  # For FAISS vector store usage
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')