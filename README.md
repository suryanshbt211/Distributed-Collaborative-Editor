# Distributed Real-Time Collaborative Editor

A production-grade distributed real-time collaborative document editor built using FastAPI, WebSockets, Redis Pub/Sub, PostgreSQL, Docker, and Conflict-Free Replicated Data Types (CRDT). This system enables multiple users to simultaneously edit shared documents with low-latency synchronization, persistent version history, and horizontally scalable backend architecture.

This project demonstrates advanced backend engineering, distributed systems design, real-time event-driven architecture, and synchronization mechanisms similar to Google Docs, Notion, and Figma.

---

# Live Demo

Live Deployment: https://your-live-link  
Demo Video: https://your-demo-video  

---

# Table of Contents

- System Overview
- Full System Architecture
- Component Architecture
- Interaction Flow
- Distributed Synchronization Design
- Database Architecture
- CRDT Conflict Resolution
- Scalability Design
- Fault Tolerance
- Technology Stack
- Folder Structure
- Setup Instructions
- Running the System
- Verifying Persistence
- Engineering Concepts Demonstrated

---

# System Overview

This system allows multiple users to edit shared documents simultaneously while maintaining consistent state across all connected clients.

Core capabilities:

- Real-time collaborative editing
- Conflict-free synchronization using CRDT
- Distributed synchronization using Redis Pub/Sub
- Persistent storage using PostgreSQL
- Version history tracking
- Snapshot-based persistence optimization
- Horizontally scalable backend architecture
- Fault-tolerant distributed design
- Containerized deployment using Docker

---

# Full System Architecture

```
                    ┌────────────────────┐
                    │     User A         │
                    │     Browser        │
                    └─────────┬──────────┘
                              │ WebSocket
                              ▼
                     ┌────────────────────┐
                     │   FastAPI Backend │
                     │   Instance #1     │
                     └─────────┬─────────┘
                               │
              ┌────────────────┴───────────────┐
              ▼                                ▼
      ┌───────────────┐               ┌───────────────┐
      │ Redis Pub/Sub │               │ PostgreSQL DB │
      │ Sync Layer    │               │ Persistence   │
      └───────┬───────┘               └───────┬───────┘
              │                               │
              ▼                               │
      ┌───────────────┐                     │
      │ FastAPI Backend│                     │
      │ Instance #2    │                     │
      └─────────┬──────┘                     │
                │                            │
                ▼                            │
         ┌───────────────┐                  │
         │     User B     │                 │
         │     Browser    │                 │
         └───────────────┘                 │
```

---

# Component Architecture

## Client Layer

Handles user interaction and communication with backend.

Responsibilities:

- Send edit operations via WebSocket
- Receive updates from backend
- Render synchronized document state

Components:

- Browser UI
- WebSocket client
- Editor interface

---

## Backend Layer (FastAPI)

Central coordination layer.

Modules:

- WebSocket Manager
- Connection Manager
- CRDT Manager
- Document Service
- Snapshot Manager

Responsibilities:

- Handle WebSocket connections
- Process edit events
- Maintain in-memory document state
- Broadcast updates
- Persist document versions

---

## Redis Synchronization Layer

Responsible for distributed messaging.

Responsibilities:

- Synchronize backend instances
- Broadcast updates across nodes
- Maintain distributed state consistency

---

## Persistence Layer (PostgreSQL)

Stores document state and version history.

Responsibilities:

- Store current document content
- Maintain version history
- Support rollback and recovery

---

# Interaction Flow

Step 1: Client connects

```
Browser → WebSocket → FastAPI Backend
```

Backend registers connection.

---

Step 2: Document loads

```
FastAPI → PostgreSQL → Load document
```

Backend loads document into CRDT memory.

Backend sends initial state to client.

---

Step 3: User edits document

```
Browser → WebSocket → FastAPI Backend
```

Backend updates CRDT state.

CRDT ensures conflict-free synchronization.

---

Step 4: Distributed broadcast

```
FastAPI → Redis Pub/Sub → Other backend nodes → Clients
```

Ensures all clients receive update.

---

Step 5: Persistence

```
FastAPI → PostgreSQL → Save snapshot
```

Ensures persistent state.

---

# Distributed Synchronization Design

Redis enables backend synchronization.

```
Backend Instance A
        │
        ▼
    Redis Pub/Sub
        │
        ▼
Backend Instance B
        │
        ▼
    Client B
```

Ensures horizontal scalability.

---

# Database Architecture

Documents Table:

```
documents
---------
id
content
version
```

Stores latest state.

---

Document Versions Table:

```
document_versions
-----------------
id
document_id
content
version_number
```

Stores version history.

---

# CRDT Conflict Resolution

CRDT ensures conflict-free editing.

Example:

User A writes:

```
Hello
```

User B writes simultaneously:

```
World
```

Final state:

```
Hello World
```

No conflicts occur.

---

# Scalability Design

Supports multiple backend nodes:

```
Load Balancer
      │
 ┌────┴────┐
 │ Backend │
 │ Backend │
 └────┬────┘
      │
     Redis
      │
 PostgreSQL
```

Enables large-scale concurrent users.

---

# Fault Tolerance

If backend crashes:

```
Restart → Load state from PostgreSQL
```

Ensures persistence.

---

# Technology Stack

Backend:

- FastAPI
- Python
- AsyncIO
- WebSockets

Distributed Systems:

- Redis Pub/Sub

Database:

- PostgreSQL

Infrastructure:

- Docker
- Docker Compose

Synchronization:

- CRDT

Frontend:

- HTML
- JavaScript

---

# Folder Structure

```
collab-platform/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── websocket_manager.py
│   │   ├── crdt.py
│   │   ├── crdt_manager.py
│   │   ├── document_service.py
│   │   ├── snapshot_manager.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── redis_client.py
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml
├── test.html
└── README.md
```

---

# Setup Instructions

Prerequisites:

- Docker
- Docker Compose
- Git

---

Clone repository:

```
git clone https://github.com/yourusername/distributed-collaborative-editor.git

cd distributed-collaborative-editor
```

---

Run system:

```
docker compose up --build
```

---

Open editor:

```
http://localhost:8000
```

---

# Verify Persistence

Connect to database:

```
docker exec -it collab_postgres psql -U collab_user -d collab_db
```

Run:

```
SELECT * FROM documents;

SELECT * FROM document_versions;
```

---

# Engineering Concepts Demonstrated

- Distributed systems
- Real-time synchronization
- Event-driven architecture
- WebSocket communication
- CRDT conflict resolution
- Distributed messaging
- Persistent storage design
- Horizontal scaling
- Containerized deployment
- Production-grade backend engineering

---

# Author

Suryansh Talukdar

GitHub: https://github.com/suryanshbt211

---

# License

MIT License
