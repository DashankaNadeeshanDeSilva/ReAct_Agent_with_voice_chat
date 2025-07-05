import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
#from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader 
from langchain_huggingface import HuggingFaceEmbeddings



def init_vector_store():
    """
    Initialize and setup Pinecone vector store.
    """
    # Load environment variables
    load_dotenv()

    index_name = os.getenv("PINECONE_INDEX_NAME")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")

    if not pinecone_api_key or not index_name:
        raise EnvironmentError("Missing PINECONE_API_KEY or PINECONE_INDEX_NAME in environment variables.")
    
    # initialize Pinecone
    pinecone = Pinecone(api_key=pinecone_api_key)

    # initialize the index and connect to a serverless index
    index = pinecone.Index(index_name)

    ## initialize embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-V2")

    # Create and return the vector store
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    return vector_store

"""
# ----------------------------------------------------
vector_store = init_vector_store()
query = "Email id to inform about sick leave"
retrived_context = vector_store.similarity_search(query, k=3)

# parse the retrieved context into a string
context = "\n".join([doc.page_content for doc in retrived_context])
    
print(context)
"""