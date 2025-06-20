import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader 
from langchain_huggingface import HuggingFaceEmbeddings

"""
Workflow:
1. Initilize and setup Pinecone
2. Chunk documents
3. Generate embeddings
3. Index the Documents
"""

# get environment variables
load_dotenv()
EMBDDING_MODEL_DIM = 384 # dimension of the embeddings from https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

def index_docs(documents: list[Document]):
    ## Initilize and setup Pinecone
    
    index_name = os.getenv("PINECONE_INDEX_NAME")
    #index_name = "kifrag-knowledge-base"
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    #pinecone_api_key = "pcsk_6vvBn6_HSv8eEXBkCPs63reaGPUag5dAaYYT9WKZ9DvZWk1AHUMGgG3DBC8DV6STdiNG6U"
    
    if not pinecone_api_key or not index_name:
        raise EnvironmentError("Missing PINECONE_API_KEY or PINECONE_INDEX_NAME in environment variables.")

    # initialize Pinecone
    pinecone = Pinecone(api_key=pinecone_api_key)

    # create a new index if doesnot exsit
    if index_name not in [i["name"] for i in pinecone.list_indexes()]:
        pinecone.create_index(
            name=index_name,
            dimension=EMBDDING_MODEL_DIM,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    # initialize the index and connect to a serverless index
    index = pinecone.Index(index_name)


    ## Chunk document
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    docs = splitter.split_documents(documents)

    ## Generate embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-V2")
    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    ## Index documents
    added_docs = vector_store.add_documents(docs)

    return added_docs # return list of indexed documents

if __name__ == "__main__":
    # test the function
    # load a document
    loader = PyPDFLoader("test.pdf")
    documents = loader.load()

    # index the document
    if index_docs(documents):
        print("Document has been indexed successfully")
    else:
        print("Document has not been indexed")