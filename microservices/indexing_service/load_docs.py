
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.schema import Document
from tempfile import NamedTemporaryFile
import os
import io


def load_document(content: bytes, filename: str) -> list[Document]:
    file_extension = os.path.splitext(filename)[-1].lower()
    #file_extension = filename.split(".")[-1].lower()

    # create a temporary file
    with NamedTemporaryFile(delete=True, suffix=file_extension) as temp:
        temp.write(content)
        temp.flush() # make sure the file is written to disk
        if file_extension == ".pdf":
            loader = PyPDFLoader(file_path=temp.name)
        elif file_extension == ".docx":
            loader = Docx2txtLoader(file_path=temp.name)
        elif file_extension == ".txt":
            loader = TextLoader(file_path=temp.name)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        # load the document
        docs = loader.load()
        return docs
    

    
