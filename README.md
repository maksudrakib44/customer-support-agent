# AI Support Agent

FastAPI-based customer support agent for two fictional test stores: **NorthDock** and **MarineX Parts**. The project includes a mock backend, OpenAI tool-calling agent, Swagger APIs, and a Streamlit test console.

This repo uses only fake store names, fake products, and fake URLs for local testing.

## Features

| Feature | Description |
| --- | --- |
| AI chat | Handles customer messages with OpenAI tool calling. |
| Order status | Looks up mock order delivery status. |
| Stock check | Checks product inventory and restock dates. |
| Product search | Searches mock products by store. |
| Shipping estimate | Returns mock delivery methods and costs. |
| Human handover | Creates a fake support ticket. |
| Case management | Closes or reopens a support case. |
| RAG hook | Calls `/api/context` and injects retrieved context into the agent prompt. |
| Streamlit console | Provides an easy UI for testing all endpoints. |

## Important RAG Note

The project currently has a RAG-style hook, not a real vector database implementation.

- Main app calls `backend_client.get_context(...)`.
- Mock backend serves `/api/context` using keyword matching over dummy data.
- No embeddings or vector DB are currently used.

For production RAG, implement semantic retrieval in the backend using embeddings and a vector store such as Qdrant, Chroma, FAISS, or Pinecone. Keep order, stock, and shipping data API-backed because those are real-time transactional values.

## Tech Stack

| Component | Technology |
| --- | --- |
| API | FastAPI |
| AI | OpenAI Chat Completions with tool calling |
| HTTP client | httpx |
| Config | Pydantic Settings, python-dotenv |
| Mock backend | FastAPI |
| Test UI | Streamlit |
| Docs | Swagger UI |

## Folder Structure

```text
customer_support/
  app/
    case/
    chat/
    core/
      agent.py              # Agent loop and tool dispatch
      agent_tools.py        # Tool handlers
      backend_client.py     # Backend API client
      common_utils.py
      prompts.py
      tool_definitions.py   # OpenAI tool schemas
    human/
    order/
    search/
    shipping/
    stock/
  frontend/
    streamlit_app.py        # Local test console
  mock_backend/
    dummy_data.py           # Fake orders/products/context
    main.py                 # Mock backend API
  config.py
  main.py                   # Main FastAPI app
  requirements.txt
  docker-compose.yml
  Dockerfile
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create `.env` from `.env.example` and update values:

```env
OPENAI_API_KEY=your_openai_api_key_here
BACKEND_BASE_URL=http://127.0.0.1:8001
API_KEY=test123
LOG_LEVEL=INFO
```

## Run Locally

Terminal 1: mock backend

```powershell
.\venv\Scripts\activate
uvicorn mock_backend.main:app --reload --port 8001
```

Terminal 2: main API

```powershell
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

Terminal 3: Streamlit test console

```powershell
.\venv\Scripts\activate
streamlit run frontend\streamlit_app.py --server.port 8501
```

Open:

```text
Main API:       http://127.0.0.1:8000
Swagger UI:     http://127.0.0.1:8000/docs
Mock Swagger:   http://127.0.0.1:8001/docs
Streamlit UI:   http://127.0.0.1:8501
```

## Sample Test Data

Orders:

```text
ORD-1001 / john@example.com
ORD-1002 / maria@example.com
ORD-1003 / test@example.com
```

Products:

```text
NDX-115
MX-SKIT-01
ND-PROP-13-19
MX-OIL-10W30
MX-FILTER-115
```

Sites:

```text
northdock
marinexparts
```

## API Endpoints

| Endpoint | Method | Description |
| --- | --- | --- |
| `/health` | GET | Main API health check |
| `/chat/message` | POST | Agent chat endpoint |
| `/api/order/status` | GET | Order status |
| `/api/product/stock` | GET | Stock check |
| `/api/product/search` | GET | Product search |
| `/api/shipping/estimate` | GET | Shipping estimate |
| `/api/human/forward` | POST | Forward to human |
| `/api/case/status` | POST | Update case status |

Chat request:

```json
{
  "message": "Do you have NDX-115 in stock?",
  "email": "john@example.com",
  "site": "northdock"
}
```

Order status query:

```text
/api/order/status?order_number=ORD-1001&email=john@example.com
```

Stock query:

```text
/api/product/stock?sku=NDX-115
```

Product search query:

```text
/api/product/search?query=propeller&site=northdock
```

Shipping query:

```text
/api/shipping/estimate?product_ids=prod-001&product_ids=prod-003&postal_code=2100&country=DK
```

## Streamlit Console

The Streamlit app is the easiest way to test the project without building a frontend. It includes tabs for:

- Chat
- Order
- Stock
- Search
- Shipping
- Human and case actions
- Mock context and conversation history

The console defaults to:

```text
Main API URL: http://127.0.0.1:8000
Mock API URL: http://127.0.0.1:8001
```

## Docker

Build and run:

```powershell
docker-compose up --build
```

For local Docker networking, `.env.example` uses:

```env
BACKEND_BASE_URL=http://mock_backend:8001
```

For local non-Docker development, use:

```env
BACKEND_BASE_URL=http://127.0.0.1:8001
```

## Development Notes

- Agent logic lives in `app/core/agent.py`.
- Tool schemas live in `app/core/tool_definitions.py`.
- Tool handlers live in `app/core/agent_tools.py`.
- Backend calls live in `app/core/backend_client.py`.
- Mock data lives in `mock_backend/dummy_data.py`.
- Streamlit frontend lives in `frontend/streamlit_app.py`.

When adding a new tool:

1. Add the OpenAI schema in `app/core/tool_definitions.py`.
2. Add the handler in `app/core/agent_tools.py`.
3. Register the handler in `Agent.tool_handlers`.
4. Add or update backend/mock backend endpoint support if needed.
