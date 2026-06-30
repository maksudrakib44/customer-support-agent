import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from app.chat.router import router as chat_router
from app.order.router import router as order_router
from app.stock.router import router as stock_router
from app.search.router import router as search_router
from app.shipping.router import router as shipping_router
from app.human.router import router as human_router
from app.case.router import router as case_router
from app.core.backend_client import backend_client

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting AI Support Agent Service...")
    yield
    logger.info("🛑 Shutting down AI Support Agent Service...")
    await backend_client.close()

app = FastAPI(
    title="AI Support Agent",
    description="Intelligent customer support for NorthDock and MarineX Parts",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Include all routers
app.include_router(chat_router)
app.include_router(order_router, prefix="/api")
app.include_router(stock_router, prefix="/api")
app.include_router(search_router, prefix="/api")
app.include_router(shipping_router, prefix="/api")
app.include_router(human_router, prefix="/api")
app.include_router(case_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-support-agent"}

@app.get("/")
async def root():
    return {
        "service": "AI Support Agent",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/chat/message",
            "health": "/health",
            "api": "/api/*"
        }
    }
