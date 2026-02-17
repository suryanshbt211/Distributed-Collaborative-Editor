# Distributed Real-Time Collaborative Editor

A distributed, low-latency collaborative document editor built using FastAPI, WebSockets, Redis Pub/Sub, PostgreSQL, Docker, and CRDT-based synchronization. This system enables multiple users to edit the same document simultaneously with real-time updates, persistent version history, and horizontally scalable backend architecture.

---

## Demo

- Live Demo: https://your-demo-link  
- Demo Video: https://your-video-link  

---

## Overview

This project implements a Google Docs–style collaborative editing system using an event-driven distributed backend. Multiple users can connect concurrently, edit shared documents, and see changes reflected instantly across all connected clients.

The system ensures:

- Real-time synchronization
- Conflict-free editing using CRDT
- Persistent storage using PostgreSQL
- Version history tracking and rollback support
- Distributed scalability using Redis Pub/Sub
- Fault-tolerant backend architecture
- Containerized deployment using Docker

---

## Key Features

- Real-time collaborative editing using WebSockets
- Conflict-free synchronization using CRDT (Conflict-Free Replicated Data Type)
- Distributed Pub/Sub messaging using Redis
- Persistent storage using PostgreSQL
- Version history and rollback support
- Snapshot-based persistence optimization
- Horizontally scalable architecture
- Containerized deployment using Docker
- Event-driven asynchronous backend

---

## System Architecture

