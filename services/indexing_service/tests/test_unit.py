import pytest
from indexing_service.load_docs import load_documnet
from langchain.schema import Document
from io import BytesIO

def test_load_txt_file():
    # Create a mock text file
    mock_file = BytesIO(b"Hello, this is a test document.")
    mock_filename = "test_document.txt"
    
    # Call the function to load the document
    documents = load_documnet(mock_file.getvalue(), mock_filename)
    
    # Check if the document is loaded correctly
    assert len(documents) == 1
    assert isinstance(documents, list)
    assert isinstance(documents[0], Document)
    assert documents[0].page_content == "Hello, this is a test document." 
    assert "test" in documents[0].page_content      

