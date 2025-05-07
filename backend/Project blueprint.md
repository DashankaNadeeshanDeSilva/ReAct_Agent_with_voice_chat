## Project:
**KIFarg**: Conversational AI assistant to ask anything from organizational knowldge base with propiatory and open source data.

### Project idea: 
Conversational AI agentic assistant that semantically search and retive knowledge from internal & propiatory (knowledge base) and external (web search) content.

### Client/audience: 
Users are employees who involved with research intense activities in their daily workflow.

### User interation:
USers are interact with the agentic assistant via chat interface

### Key features:
* In the core of the system, there exsits a ReAct agent that is connected with tools (which are web search and knowledge retrival) who can think and provide responses to the user query.

* Knowledge retrival: Users can perform semantic search/knowledge retrival and ask questions across content including internal documents, research papers (internal and external like from internet), reports, technical manuals and more. methods: similarity search with vector embeddings and Context awere quesry expansion.

* Organizational and domain specific content are stored in knowledge base (indexed in vector db), uploaded by users (and by admin via admin dashboard) and search in web (internet) via agent's web seach tool depending on requiurement (priority goes to internal knowldgebase search).

*  The users/admin can modify and update (add and remove) content from knowledge base to add new content and remove outdated content (user can add or remove the content added in the current session).

### Impact: 

Reduce research time and help users to find more contextually and semantically relevant and rich knowledge and content with less efforts compared to manual reading and researching.
### Overall architetcure:
The entire system follows microservices architecture where each main component is a mircoservice e.g. AI agent service (core ReAct Agent for AI logic with tools) and frontend service (chat interface)

### Main components for Minimum Viable product:
* Chat interface (Frontend service): Javacript based interactive frontend where users can chat and also upload documents to perform knowldeg retival from uploaded, already exsiting internal and external (websearch) content. The users should be able to add or remove documnets uploaded. **Technologies**: Javascript and html
* API gateway: Performs routing requests and responses between services. **Technologies**: FastApI
* Agent service: Core AI logic which runs a ReAct Agent with tools (RAG for knowldge retival from vector db and web-serach). Agent is connected to LLM via API and tools are implmented within. **Technologies**: Langchain/Langgarph and API connections.
* Document indexing service: Onece content or document (research paper, report or any documnet) uploaded (by user or admin), the content is indexed to the vector database.
* Vector database: Setup seperately with pinecone. 

### Deployment:
Each microservice is dockerized (with docker) and run in cloud environment. Complete deployment is run via CI/CD pipeline with Jenkins (for internal servers) or Github actions (for AWS cloud env).


**Additional**
* Deep understanding of LLMs, their context windows, and model behavior, and limitations (including practical limitations such as API call limits),
* Deep understanding of state-of-the-art embedding (e.g. contextual embeddings), retrieval (e.g. hybrid search), and chunking techniques.
* Experience and knowldge about advanced prompt engineering techniques (e.g. zero shot prompting, CoT, etc.)