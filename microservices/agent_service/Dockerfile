# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8001

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "agent_service_app:app", "--host", "0.0.0.0", "--port", "8001"]