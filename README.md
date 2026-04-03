# Claim Processing Pipeline

## Overview
The **Claim Processing Pipeline** is an intelligent, automated backend service designed to process and extract critical data from medical claim PDF documents. Built with **FastAPI** and **LangGraph**, it orchestrates a team of specialized AI agents that collaboratively segregate, extract, and aggregate data, providing a structured final output.

## Architecture & Workflow
The data processing lifecycle is managed using a directed state graph to handle PDF documents optimally. The pipeline consists of the following components:

1. **Segregator Agent**: Ingests the initial PDF document and segregates/classifies the pages based on their content type (e.g., ID cards, discharge summaries, bills).
2. **Specialized Extraction Agents**: Relevant pages are routed to their respective expert agents:
   - **ID Agent** (`id_agent`): Extracts patient, member, and provider identification details.
   - **Discharge Agent** (`discharge_agent`): Pulls critical medical information and history from discharge summaries.
   - **Bill Agent** (`bill_agent`): Parses complex itemized billing information.
3. **Aggregator Node**: Collects the structured JSON data extracted by the individual agents and compiles it into a unified, coherent final response.

## Tech Stack
- **Web Framework**: FastAPI, Uvicorn
- **AI Orchestration**: LangGraph, LangChain
- **LLM Integration**: ChatOpenAI implementation (compatible with OpenRouter)
- **PDF Processing**: PyMuPDF
- **Data Validation**: Pydantic
- **Package Management**: `uv`

## Setup & Installation

### Prerequisites
- Python 3.12+

### Installation Steps
1. **Clone the repository** and navigate to the project root.
2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
3. **Install the dependencies**:
   This project uses `uv` for fast dependency management. You can install the dependencies via:
   ```bash
   uv sync
   ```
   *Alternatively, install via pip using the project file definition:*
   ```bash
   pip install -e .
   ```

## Configuration
Create a `.env` file in the root directory and configure your LLM settings. Depending on your configuration (e.g., using OpenRouter), add the necessary API keys:

```env
OPENROUTER_API_KEY="your-api-key"
OPENROUTER_MODEL="your-chosen-model"

## Running the Application
To start the FastAPI development server, run:

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`. You can also access the interactive API docs at `http://127.0.0.1:8000/docs`.

## API Endpoints

### `POST /api/process`
Ingests and processes a medical claim document.
- **Content-Type**: `multipart/form-data`
- **Parameters**:
  - `claim_id` (string): A unique identifier for the claim.
  - `file` (file): The uploaded PDF claim file (Max size: 40MB).
- **Response**: A JSON object containing the `status` and the aggregated extraction `data`.

### `GET /`
Health check endpoint.
- **Response**: `{"Hello": "World"}`
