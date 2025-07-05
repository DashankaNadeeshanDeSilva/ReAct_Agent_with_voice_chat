import pytest
from httpx import AsyncClient
from indexing_service.indexing_service_app import app


@pytest.mark.asyncio
async def test_index_document_api():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create a mock text file
        mock_file = b"Hello, this is a test document." # creates a byte string using the b prefix
        files = {"file": ("test_document.txt", mock_file)} # dictionary suitable for file upload in a POST request

        # Send a POST request to the /index_document/ endpoint
        response = await client.post("/index_document/", files=files)

        # Check the response status code and content
        assert response.status_code == 200
        assert response.json() == {"message": "Document has been indexed successful"}