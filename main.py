from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# Serve static files from the 'static' directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Store connected WebSocket clients
connected_clients = set()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    connected_clients.add(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = f"Client {client_id}: {data}"
            for client in connected_clients:
                await client.send_text(message)
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        
@app.get("/")
async def read_root():
    # Read the index.html file and return its content
    with open(Path(__file__).parent / "static" / "index.html") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)