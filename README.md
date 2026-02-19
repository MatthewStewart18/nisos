# Risk Assesment

Risk assesment is a project featuring a LangGraph-based agent (`nisos-agent`) and a mock API for fetching social media profiles (for risk assesment).

## Getting Started (Local Hosting)

To run the project locally with Docker Compose, navigate to the `nisos-studio` directory and ensure your API keys are configured.

### Prerequisites

Create a `.env` file in the `nisos-studio/` directory with the following keys:

```text
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=nisos-studio
GEMINI_API_KEY=your_gemini_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
```

### Run with Docker

```bash
cd nisos-studio
docker compose up
```

### Services

- **Frontend / Agent**: [http://localhost:8000](http://localhost:8000)
- **Mockoon API**: [http://localhost:3001](http://localhost:3001)

### User Management

Users are managed at the following path structure:
`users/user_name`

## Documentation

For more detailed information, see [nisos-studio/README.md](./nisos-studio/README.md).
