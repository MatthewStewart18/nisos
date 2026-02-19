# Nisos Studio Simple Frontend

This frontend allows you to interact with the LangGraph agent via a web interface.

## How to Run

1.  Navigate to the `nisos-studio` directory:
    ```bash
    cd nisos-studio
    ```

2.  Ensure you have the required dependencies installed (already in the project's environment):
    ```bash
    pip install starlette uvicorn
    ```

3.  Run the application:
    ```bash
    PYTHONPATH=. python src/agent/app.py
    ```

4.  Open your browser and navigate to:
    `http://localhost:8000`

## Features

-   **Real-time Streaming**: See the graph state update live as nodes are executed.
-   **Profile Information**: Displays user full name, username, biography, and profile picture.
-   **Threat Assessment**: Shows threat detected status and confidence level.
-   **Flagged Content**: Lists IDs of posts that triggered safety concerns.
-   **Executive Summary**: Displays the final AI-generated summary and rationale.

## Mock Social Media API

The agent expects a social media API to be running at the URL you provide. 
Example: `http://localhost:3001/users/alex_rivers`
