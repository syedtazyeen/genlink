from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
from starlette.exceptions import HTTPException
from app.lib.exceptions import http_exception_handler, validation_exception_handler, global_exception_handler
from app.core.logger import logger
from app.core  import DefaultByAliasFalseRouter
from app.core.config import get_config
import app.routes as routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize and clean up resources for the FastAPI app.
    """
    settings = get_config()
    logger.info(f"Connecting to MongoDB...")

    app.mongodb_client = None

    try:
        app.mongodb_client = AsyncIOMotorClient(settings.DATABASE_URL)
        app.mongodb = app.mongodb_client[settings.DATABASE_NAME]
        logger.info("Connected to MongoDB successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise RuntimeError("MongoDB connection failed") from e

    try:
        yield
    finally:
        if app.mongodb_client:
            logger.info("Shutting down MongoDB connection...")
            app.mongodb_client.close()
            logger.info("MongoDB connection closed")

# Initialize app
app = FastAPI(
    title="GenLink API",
    description="Backend API for the GenLink platform",
    version="1.0.0",
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
    route_class=DefaultByAliasFalseRouter,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
routers.__init__(app)

@app.get("/",tags=["Root"])
def read_root():
    return {"message": "Welcome to GenLink API", "status": "ok"}


# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)