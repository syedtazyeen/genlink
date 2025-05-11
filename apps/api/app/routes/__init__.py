""" Routers. """

from fastapi import FastAPI
from .auth import router as auth_router

def __init__(app: FastAPI):
    """Registers all routers."""
    app.include_router(auth_router)