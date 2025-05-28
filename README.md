# KIFrag: Conversational AI Agent to query from the knowledge base

## Project:
**KIFarg**: Conversational AI assistant to ask anything from organizational knowledge base with propiatory and open source data. A modular, full-stack AI-powered chat agent featuring Retrieval-Augmented Generation (RAG).  
This project is organized as a microservices architecture with a frontend, API gateway, agent service, and supporting services.

### Project idea: 
Conversational AI agentic assistant that semantically searches and retrieves knowledge from internal & proprietary (knowledge base) and external (web search) content.

### Client/audience: 
Users are employees who are  involved in research-intensive activities in their daily workflow.

### User interaction:
Users interact with the agentic assistant via a chat interface

## Features

- **Retrieval-Augmented Generation (RAG)** for improved contextual responses
- Microservices-based architecture for scalability and maintainability
- REST API Gateway for unified access to services
- Modular, extensible codebase
- Modern frontend for chat interactions

## Project Structure

```
.
├── agent service      # Core RAG agent logic and orchestration
├── api-gateway        # API gateway exposing unified REST endpoints
├── frontend           # Web UI for chat and management
├── services           # Supporting services (data, retrieval, etc.)
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Node.js, npm/yarn (for frontend and possibly gateway)
- Python (for agent and certain services, if applicable)
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/DashankaNadeeshanDeSilva/KIFrag_RAG_Chat_Agent.git
   cd KIFrag_RAG_Chat_Agent
   ```

2. **Setup each service:**
   - Follow the instructions in each subdirectory (`agent service`, `api-gateway`, `frontend`, `services`) for dependencies and setup.

3. **Run the system:**
   - You may use Docker Compose or run services individually as per their documentation.

### Example (API Gateway):

```sh
cd api-gateway
npm install
npm start
```

### Example (Frontend):

```sh
cd frontend
npm install
npm run dev
```

## Usage

- Open the frontend in your browser to interact with the chat agent.
- Use the API gateway endpoints to integrate with other applications or services.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your proposed changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Maintainer: [Dashanka Nadeeshan De Silva](https://github.com/DashankaNadeeshanDeSilva)
