# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json (if available)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the app for production
RUN npm run build

# Expose the port the app runs on (default Vite preview port)
EXPOSE 4173

# Start the app using Vite preview
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]
