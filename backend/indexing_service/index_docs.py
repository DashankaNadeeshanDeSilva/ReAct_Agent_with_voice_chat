import os
from pinecode import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader



"""
1. Define the VectorStore
2. Define the Document Loader
3. Index the Documents
"""

# get environment variables
os.environ["PINECONE_API_KEY"] = os.getenv("PINECONE_API_KEY")

# initialize Pinecone
pinecone = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = os.getenv("PINECONE_INDEX_NAME")

# create a new index if doesnot exsit
if index_name not in [i["name"] for i in pinecone.list_indexes()]:
    pinecone.create_index(
        index_name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# initialize the index and connect to the index
index = pinecone.Index(index_name=index_name)

# load the documents



