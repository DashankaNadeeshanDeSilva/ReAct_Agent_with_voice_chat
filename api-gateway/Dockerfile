From python:3.10
# Set the working directory
WORKDIR /app
# Copy the requirements file into the container
COPY requirements.txt .
# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Copy the rest of the application code into the container
COPY . .
# Expose the port the app runs on
EXPOSE 8001
# Run the application
CMD ["uvicorn", "api_gateway_app:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]