from fastapi import FastAPI
from app.routes import api_routes


def create_app():
    app = FastAPI(
        title="MAHARAGA API",
        description="Hybrid AI System — Multi-Domain Conversational Intelligence Engine",
        version="1.0.0",
    )
    app.include_router(api_routes.router)
    return app
