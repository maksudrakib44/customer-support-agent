## AI Support Agent – Complete Documentation

## 📖 Project Overview

This is a **production-ready AI customer support agent** built for **NorthDock** and **MarineX Parts**, two fictional test stores. It uses OpenAI's GPT-4o to autonomously handle first-line customer inquiries via a chat popup or contact form. The agent is **stateless** and relies on a backend API for all data (orders, stock, products, shipping, and conversation history). If the AI cannot answer a query, it forwards the conversation to a mock support system.

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **AI‑powered chat** | Handles customer questions naturally, using 7 specialised tools. |
| **Order status** | Retrieves real‑time delivery/shipping information. |
| **Stock availability** | Checks product inventory and restock dates. |
| **Product search** | Searches across both `northdock` and `marinexparts`. |
| **Shipping estimates** | Provides delivery time and cost estimates. |
| **Human handover** | Escalates complex queries to OSS with ticket creation. |
| **Case management** | Automatically closes resolved cases and reopens when customers return. |
| **RAG (Retrieval‑Augmented Generation)** | Learns from past conversations and articles. |
| **Stateless design** | No internal database; all data fetched via backend APIs. |

---

## 🧱 Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.11+ |
| **Web Framework** | FastAPI |
| **AI Model** | OpenAI GPT‑4o (Chat Completions API) |
| **HTTP Client** | httpx (async) |
| **Configuration** | python‑dotenv, Pydantic Settings |
| **Containerisation** | Docker & Docker Compose |
| **Testing** | Swagger UI (auto‑generated), curl |

---

## 📂 Folder Structure

```
customer_support/
├── app/
│   ├── core/                    # Shared logic
│   │   ├── agent.py             # Main ReAct agent
│   │   ├── prompts.py           # System prompt
│   │   ├── backend_client.py    # HTTP client to backend
│   │   ├── common_utils.py      # Helpers (ID generation, formatting)
│   │   └── tools/               # 7 tool definitions + handlers
│   │       ├── definitions.py   # OpenAI tool schemas
│   │       ├── order.py
│   │       ├── stock.py
│   │       ├── search.py
│   │       ├── shipping.py
│   │       ├── human.py
│   │       └── case.py
│   ├── chat/                    # Chat endpoint
│   │   ├── request.py
│   │   ├── router.py
│   │   └── service.py
│   ├── order/                   # Order status endpoint
│   ├── stock/                   # Stock check endpoint
│   ├── search/                  # Product search endpoint
│   ├── shipping/                # Shipping estimate endpoint
│   ├── human/                   # Forward‑to‑human endpoint
│   └── case/                    # Case management endpoint
├── mock_backend/                # Mock server for development
│   ├── main.py
│   └── dummy_data.py
├── config.py                    # Root configuration
├── main.py                      # FastAPI entry point
├── .env                         # Environment variables (not committed)
├── .env.example                 # Template for environment variables
├── Dockerfile                   # AI service container
├── Dockerfile.mock_backend      # Mock backend container
├── docker-compose.yml           # Orchestrates both services
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🔧 Prerequisites

- **Python 3.11+** (if running locally)
- **Docker** and **Docker Compose** (optional but recommended)
- An **OpenAI API key** with access to `gpt-4o`
- **Backend API** (provided by your backend team) – a mock is included for development

---

## ⚙️ Installation & Setup

### Option 1: Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd customer_support
   ```

2. **Create a `.env` file** from the template:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your **OpenAI API key** and a shared `API_KEY` (e.g., `test123`).

3. **Build and start the containers**
   ```bash
   docker-compose up --build
   ```
   This starts:
   - **Mock Backend** at `http://localhost:8001`
   - **AI Service** at `http://localhost:8000`

4. **Verify** that both services are running:
   - Visit `http://localhost:8000/health` → should return `{"status":"ok"}`
   - Visit `http://localhost:8001/` → should show the mock backend info.

---

### Option 2: Running Locally (without Docker)

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create `.env`** (same as above).

4. **Open two terminals**:
   - **Terminal 1** – Mock Backend:
     ```bash
     uvicorn mock_backend.main:app --host 0.0.0.0 --port 8001
     ```
   - **Terminal 2** – AI Service:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8000
     ```

5. **Access Swagger UI** at `http://localhost:8000/docs` to explore and test endpoints.

---

## 🔑 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required) | – |
| `BACKEND_BASE_URL` | Base URL of the backend API | `http://mock_backend:8001` |
| `API_KEY` | Shared secret for authenticating requests | – |
| `LOG_LEVEL` | Logging level (`DEBUG`, `INFO`, etc.) | `INFO` |
| `REQUEST_TIMEOUT` | HTTP request timeout (seconds) | `30` |

---

## 📡 API Endpoints

All endpoints require the `Authorization: Bearer <API_KEY>` header (except health/root).

### Main Chat Endpoint

**`POST /chat/message`**  
**Request body:**
```json
{
  "message": "Where is my order?",
  "email": "john@example.com",
  "site": "northdock"
}
```
**Response:**
```json
{
  "answer": "Your order ORD-001 has been shipped...",
  "conversation_id": "conv_john@example.com_1234567890"
}
```

---

### Supporting Endpoints (for testing)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/order/status` | GET | Get order status (params: `order_number`, `email`) |
| `/api/product/stock` | GET | Check stock (param: `sku`) |
| `/api/product/search` | GET | Search products (params: `query`, `site`) |
| `/api/shipping/estimate` | GET | Estimate shipping (params: `product_ids[]`, `postal_code`, `country`) |
| `/api/human/forward` | POST | Forward to human (body: `conversation_id`, `customer_email`, `question`, `ai_attempt`) |
| `/api/case/status` | POST | Update case status (body: `conversation_id`, `status`, `resolution_summary`) |

All supporting endpoints are **proxy endpoints** that forward calls to the backend API. They are useful for testing the AI’s tool integration.

---

## 🧪 Testing the AI

### Using Swagger UI
1. Open `http://localhost:8000/docs`.
2. Authorize by clicking the **“Authorize”** button and entering `Bearer test123` (or your `API_KEY`).
3. Expand the `POST /chat/message` endpoint, click **“Try it out”**, enter a message, and execute.

### Using cURL
```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Authorization: Bearer test123" \
  -H "Content-Type: application/json" \
  -d '{"message":"Where is my order?","email":"john@example.com","site":"northdock"}'
```

### Using PowerShell (Windows)
```powershell
$body = @{message="Where is my order?"; email="john@example.com"; site="northdock"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat/message" -Method Post -Headers @{Authorization="Bearer test123"} -Body $body -ContentType "application/json"
```

---


## 🐳 Docker Deployment

To deploy in production:

1. Set up environment variables on your host/server.
2. Build and run:
   ```bash
   docker-compose up -d --build
   ```
3. Optionally, remove the mock backend and point `BACKEND_BASE_URL` to your real backend.

For advanced deployments (e.g., Kubernetes), use the provided `Dockerfile` and adjust the environment accordingly.

---

## 🧑‍💻 Developer Notes

- **Agent logic** resides in `app/core/agent.py` – this is the core ReAct loop.
- **Adding a new tool**: Define its schema in `app/core/tool_definitions.py`, add the handler in `app/core/agent_tools.py`, and register it in the `tool_handlers` dict in `agent.py`.
- **Adding a new endpoint**: Create a new folder under `app/` with `request.py`, `router.py`, and `service.py`. Import the router in `main.py`.
- **Mock data** is stored in `mock_backend/dummy_data.py` – update it to match your real data structure.
- **Streamlit test console** runs from `frontend/streamlit_app.py` after the main API and mock backend are running.

---
