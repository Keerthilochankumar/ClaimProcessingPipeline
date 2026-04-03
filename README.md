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
SILICONFLOW_API_KEY=sk-""
SILICONFLOW_MODEL=""

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


## 'SAMPLE OUTPUT'

```json
{
  "status": "success",
  "data": {
    "claim_id": "CLM-2024-789456",
    "document_classification": {
      "claim_forms": [
        1,
        8,
        13,
        15,
        16
      ],
      "cheque_or_bank_details": [
        2
      ],
      "identity_document": [
        3
      ],
      "discharge_summary": [
        4,
        17,
        18
      ],
      "prescription": [
        5
      ],
      "investigation_report": [
        6,
        11,
        12
      ],
      "cash_receipt": [
        7
      ],
      "itemized_bill": [
        9,
        10
      ],
      "other": [
        14
      ]
    },
    "identity_information": {
      "patient_name": "John Michael Smith",
      "date_of_birth": "1985-03-15",
      "gender": "Male",
      "id_number": "ID-987-654-321",
      "policy_number": "POL-987654321",
      "insurance_provider": "HealthCare Insurance Company",
      "contact_number": "+1-555-0123",
      "address": "456 Oak Street, Apt 12B, Springfield, IL 62701"
    },
    "discharge_summary": {
      "patient_name": "John Michael Smith",
      "admission_date": "2025-01-20",
      "discharge_date": "2025-01-25",
      "diagnosis": "Community Acquired Pneumonia (CAP)",
      "procedures": [],
      "treating_physician": "Dr. Sarah Johnson, MD",
      "department": "Gastroenterology Department",
      "follow_up_instructions": "Outpatient clinic in 1 week"
    },
    "itemized_bill": {
      "items": [
        {
          "description": "Room Charges-Semi-Private (5 days)",
          "quantity": 5,
          "unit_price": 200,
          "amount": 1000
        },
        {
          "description": "Admission Fee",
          "quantity": 1,
          "unit_price": 150,
          "amount": 150
        },
        {
          "description": "Emergency Room Services",
          "quantity": 1,
          "unit_price": 500,
          "amount": 500
        },
        {
          "description": "Physician Consultation-Dr. Sarah Johnson",
          "quantity": 5,
          "unit_price": 150,
          "amount": 750
        },
        {
          "description": "Chest X-Ray",
          "quantity": 2,
          "unit_price": 120,
          "amount": 240
        },
        {
          "description": "CT Scan-Chest",
          "quantity": 1,
          "unit_price": 800,
          "amount": 800
        },
        {
          "description": "Complete Blood Count (CBC)",
          "quantity": 3,
          "unit_price": 45,
          "amount": 135
        },
        {
          "description": "Blood Culture Test",
          "quantity": 2,
          "unit_price": 80,
          "amount": 160
        },
        {
          "description": "Arterial Blood Gas Analysis",
          "quantity": 1,
          "unit_price": 95,
          "amount": 95
        },
        {
          "description": "IV Fluids-Normal Saline",
          "quantity": 10,
          "unit_price": 25,
          "amount": 250
        },
        {
          "description": "Injection-Ceftriaxone 1g",
          "quantity": 5,
          "unit_price": 30,
          "amount": 150
        },
        {
          "description": "Injection-Paracetamol",
          "quantity": 6,
          "unit_price": 8,
          "amount": 48
        },
        {
          "description": "Nebulization Treatment",
          "quantity": 4,
          "unit_price": 35,
          "amount": 140
        },
        {
          "description": "Oxygen Therapy (per hour)",
          "quantity": 48,
          "unit_price": 5,
          "amount": 240
        },
        {
          "description": "Nursing Care (per day)",
          "quantity": 5,
          "unit_price": 100,
          "amount": 500
        },
        {
          "description": "ICU Monitoring Equipment",
          "quantity": 2,
          "unit_price": 200,
          "amount": 400
        },
        {
          "description": "Physiotherapy Session",
          "quantity": 3,
          "unit_price": 60,
          "amount": 180
        },
        {
          "description": "Medical Supplies & Consumables",
          "quantity": 1,
          "unit_price": 250,
          "amount": 250
        },
        {
          "description": "Laboratory Processing Fee",
          "quantity": 1,
          "unit_price": 75,
          "amount": 75
        },
        {
          "description": "Pharmacy Dispensing Fee",
          "quantity": 1,
          "unit_price": 50,
          "amount": 50
        }
      ],
      "subtotal": 6113,
      "tax": 305.65,
      "total_amount": 6418.65,
      "currency": "USD"
    }
  }
}
