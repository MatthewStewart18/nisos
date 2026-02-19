# Nisos Studio - Local Hosting

This project includes a LangGraph agent (`nisos-agent`) and a mock server (`mockoon`).

## Prerequisites

Before running the services, ensure you have a `.env` file in the `nisos-studio/` directory with the following API keys:

```text
# nisos-studio/.env
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=your-project-name
GEMINI_API_KEY=your-gemini-api-key
LANGSMITH_API_KEY=your-langsmith-api-key
```

## Running Locally

To start the services using Docker Compose, run:

```bash
docker compose up
```

### Services

- **Frontend / Agent**: [http://localhost:8000](http://localhost:8000)
- **Mockoon API**: [http://localhost:3001](http://localhost:3001)

### User Management

Users are managed at the following path structure:
`users/user_name`

## Project Structure

- `src/agent/`: Core agent logic.
- `mockoon-data.json`: Configuration for the Mockoon mock API.
- `docker-compose.yml`: Docker configuration for local development.
