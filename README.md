# Distributed Real-Time Collaborative Editor

A production-grade distributed real-time collaborative document editor built using FastAPI, WebSockets, Redis Pub/Sub, PostgreSQL, Docker, and Conflict-Free Replicated Data Types (CRDT). This system enables multiple users to simultaneously edit documents with real-time synchronization, persistent version history, and horizontally scalable distributed backend architecture.

This project demonstrates advanced backend engineering, distributed systems design, event-driven architecture, and real-time state synchronization similar to systems used in Google Docs, Notion, and Figma.

---

# Live Demo

Live Deployment: https://your-live-link  
Demo Video: https://your-demo-video  

---

# Table of Contents

- System Overview
- Full System Architecture
- Component Architecture
- Detailed Interaction Flow
- Distributed Synchronization Architecture
- Database Architecture
- CRDT Conflict Resolution
- Scalability Design
- Fault Tolerance Design
- Technology Stack
- Folder Structure
- Setup Instructions
- Running the System
- Verifying Database Persistence
- Engineering Concepts Demonstrated

---

# System Overview

This system enables multiple users to edit shared documents simultaneously with low-latency synchronization and persistent storage.

Core capabilities:

- Real-time collaborative editing
- Conflict-free synchronization using CRDT
- Distributed synchronization using Redis Pub/Sub
- Persistent storage using PostgreSQL
- Document version history tracking
- Snapshot-based persistence optimization
- Horizontally scalable backend architecture
- Fault-tolerant distributed system design
- Containerized infrastructure using Docker

---

# Full System Architecture

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

---

# Component Architecture

## 1. Client Layer

Responsible for user interaction.

Components:

- Browser UI
- WebSocket Client
- Text Editor

Responsibilities:

- Capture user input
- Send updates to backend
- Receive synchronized updates
- Display real-time document state

---

## 2. Backend Layer (FastAPI)

Central distributed coordination layer.

Core modules:

- WebSocket Manager
- Connection Manager
- CRDT Manager
- Document Service
- Snapshot Manager

Responsibilities:

- Manage WebSocket connections
- Process edit events
- Maintain in-memory CRDT state
- Broadcast updates to clients
- Persist document versions

---

## 3. Synchronization Layer (Redis Pub/Sub)

Distributed message broker.

Responsibilities:

- Synchronize multiple backend nodes
- Broadcast document updates across instances
- Maintain distributed consistency

Enables horizontal scaling.

---

## 4. Persistence Layer (PostgreSQL)

Persistent storage system.

Stores:

- Latest document state
- Version history
- Document snapshots

Enables fault recovery.

---

# Detailed Interaction Flow

## Step 1: Client connects

User opens editor in browser.

Connection established:


Backend registers connection.

---

## Step 2: Document loading

Backend loads document from database:


Document loaded into CRDT memory.

Backend sends initial state to client.

---

## Step 3: User edits document

User types text:

