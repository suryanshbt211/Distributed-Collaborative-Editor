from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
import json

from .websocket_manager import manager
from .document_service import DocumentService
from .crdt_manager import crdt_manager
from .snapshot_manager import snapshot_manager


app = FastAPI()


# Startup event: start Redis listener and Snapshot manager
@app.on_event("startup")
async def startup_event():

    await manager.start_listener()

    await snapshot_manager.start()

    print("Redis listener started")
    print("Snapshot manager started")
    print("Application startup complete")


@app.get("/")
async def root():

    return {
        "status": "running",
        "system": "collab-platform"
    }


# Main WebSocket endpoint
@app.websocket("/ws/{document_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    document_id: str
):

    # Connect client
    await manager.connect(document_id, websocket)

    # Load document from database
    document = await DocumentService.get_or_create_document(document_id)

    # Load document into CRDT memory
    crdt_doc = crdt_manager.get_document(document_id)
    crdt_doc.load_text(document.content)

    # Send initial state to client
    await websocket.send_text(
        json.dumps({
            "type": "init",
            "content": document.content
        })
    )

    try:

        while True:

            raw = await websocket.receive_text()

            data = json.loads(raw)

            message_type = data.get("type")


            # Handle edit event
            if message_type == "edit":

                content = data.get("content", "")

                # Update CRDT memory
                crdt_doc.load_text(content)

                new_content = crdt_doc.get_text()

                # Mark document dirty for snapshot (IMPORTANT CHANGE)
                snapshot_manager.mark_dirty(document_id)

                # Broadcast to all clients
                await manager.broadcast_json(
                    document_id,
                    {
                        "type": "edit",
                        "content": new_content
                    }
                )


            # Handle cursor presence
            elif message_type == "cursor":

                position = data.get("position", 0)

                await manager.broadcast_json(
                    document_id,
                    {
                        "type": "cursor",
                        "position": position
                    }
                )


            # Handle join presence
            elif message_type == "join":

                user_id = data.get("user_id", "anonymous")

                await manager.broadcast_json(
                    document_id,
                    {
                        "type": "join",
                        "user_id": user_id
                    }
                )


            # Handle ping keepalive
            elif message_type == "ping":

                await websocket.send_text(
                    json.dumps({
                        "type": "pong"
                    })
                )


    except WebSocketDisconnect:

        manager.disconnect(document_id, websocket)

        print(f"Client disconnected from document {document_id}")


# Rollback endpoint
@app.post("/rollback/{document_id}/{version_number}")
async def rollback(
    document_id: str,
    version_number: int
):

    content = await DocumentService.rollback_document(
        document_id,
        version_number
    )

    if content is None:

        raise HTTPException(
            status_code=404,
            detail="Version not found"
        )

    # Reload CRDT state
    crdt_doc = crdt_manager.get_document(document_id)
    crdt_doc.load_text(content)

    # Mark dirty so snapshot saves rollback
    snapshot_manager.mark_dirty(document_id)

    # Broadcast rollback to clients
    await manager.broadcast_json(
        document_id,
        {
            "type": "edit",
            "content": content
        }
    )

    return {
        "status": "success",
        "document_id": document_id,
        "version_restored": version_number
    }
