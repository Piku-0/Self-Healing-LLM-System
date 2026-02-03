# Self-Healing LLM Gateway

A deterministic control system for non-deterministic Large Language Models (LLMs). This API gateway provides reliability, verification, and self-healing capabilities for AI applications.

## Core Philosophy

**"Trust, but Verify. If Verify fails, Fix."**

This system treats LLM outputs as untrusted by default. It implements a rigorous verification pipeline and an autonomous self-healing loop to ensure response quality, safety, and strict schema adherence.

## Features

- **Semantic Caching**: High-speed vector-based caching (ChromaDB) to reduce latency and costs.
- **Verification Pipeline**: Parallel execution of Instruction, Safety, Logic, and Schema verifiers.
- **Self-Healing**: Autonomous retry strategies (Reflection, Decomposition, Model Switching).
- **Resilience**: Circuit breakers, graceful degradation, and model routing.
- **Observability**: Full traceability of requests, verification results, and healing events.

## Tech Stack

- **Language**: Python 3.11+
- **API Framework**: FastAPI
- **LLM Integration**: Llama 3 / Mistral (via Ollama/vLLM)
- **Validation**: Pydantic V2
- **Vector Store**: ChromaDB
- **Database**: PostgreSQL (Logs/Audit)

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Ollama or vLLM running locally
- Docker (optional, for Postgres/Chroma)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/Piku-0/Self-Healing-LLM-System.git
   cd Self-Healing-LLM-System
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture

The system transitions a user request through the following state machine:

1. **Cache Check**: Return immediately on high-confidence hit.
2. **Generation**: Stream tokens from the primary model.
3. **Verification**: Validate output against safety and logic rules.
4. **Healing**: If validation fails, apply retry strategies until success or exhaustion.
