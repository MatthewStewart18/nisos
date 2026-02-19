import json
import asyncio
import os
import sys

# Add the project root to sys.path to allow absolute imports from 'src'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from starlette.applications import Starlette
from starlette.responses import HTMLResponse, StreamingResponse
from starlette.routing import Route
from src.agent.nisos_agent import graph

async def run_graph(request):
    try:
        body = await request.json()
        profile_url = body.get("profile_url")
        
        # If it looks like a username, construct the URL using environment config
        if profile_url and not profile_url.startswith("http"):
            base_url = os.getenv("MOCKOON_URL", "http://localhost:3001")
            profile_url = f"{base_url.rstrip('/')}/users/{profile_url}"
            print(f"--- [Server] Resolved username to URL: {profile_url} ---")

        if not profile_url:
            return StreamingResponse(iter([f"data: {json.dumps({'error': 'profile_url is required'})}\n\n"]), media_type="text/event-stream")
    except Exception as e:
        return StreamingResponse(iter([f"data: {json.dumps({'error': str(e)})}\n\n"]), media_type="text/event-stream")

    async def event_generator():
        try:
            input_state = {"profile_url": profile_url}
            
            # Use a dictionary to keep track of the cumulative state
            full_state = {}
            
            async for event in graph.astream(input_state, stream_mode="values"):
                full_state.update(event)
                print(f"--- [Server] Sending state update. Keys: {list(full_state.keys())} ---")
                yield f"data: {json.dumps(full_state)}\n\n"
                await asyncio.sleep(0.2) # Give the network and frontend time to breathe
            
            print("--- [Server] Graph execution complete ---")
        except Exception as e:
            print(f"--- [Server Error] {str(e)} ---")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

async def homepage(request):
    static_html_path = os.path.join(current_dir, "static", "index.html")
    try:
        with open(static_html_path) as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        return HTMLResponse(f"index.html not found at {static_html_path}", status_code=404)

routes = [
    Route("/", homepage),
    Route("/run", run_graph, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    import uvicorn
    # Change to project root so 'src' is importable
    os.chdir(project_root)
    uvicorn.run("src.agent.app:app", host="0.0.0.0", port=8000, reload=True)
