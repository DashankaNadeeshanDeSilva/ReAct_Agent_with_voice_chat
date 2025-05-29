FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the rest of the application code into the container
COPY . .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "api_gateway_app:app", "--host", "0.0.0.0", "--port", "8000"]