"""
Maharaga Backend Initialization
-------------------------------
FastAPI factory function that bootstraps the entire system —
loads configuration, initializes databases, embeddings, and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import (
    APP_NAME,
    APP_VERSION,
    ENVIRONMENT,
    initialize_system,
    shutdown_system,
)
from app.utils import logger, connect_databases, embedding_helper
from app.routes import api_routes, admin_routes, auth_routes


# =============================================================
# 🔹 app factory
# =============================================================
def create_app() -> FastAPI:
    """creates and configures the Maharaga FastAPI application."""
    logger.info(f"🚀 launching {APP_NAME} v{APP_VERSION} [{ENVIRONMENT}]...")

    app = FastAPI(
        title=f"{APP_NAME} API",
        description="⚡ Hybrid AI System — Multi-Domain Conversational Intelligence Engine",
        version=APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ---------------------------------------------------------
    # 🔸 middleware setup
    # ---------------------------------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO: restrict this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------------------------------------
    # 🔸 startup event
    # ---------------------------------------------------------
    @app.on_event("startup")
    async def on_startup():
        """initialize db + ai subsystems safely on startup"""
        try:
            logger.info("⚙️ system startup sequence initiated...")
            initialize_system()
            connect_databases()
            if embedding_helper.model:
                logger.info("🧠 embedding subsystem active.")
            logger.info("✅ system startup complete — all systems go.")
        except Exception as e:
            logger.error(f"❌ startup failure: {e}")
            raise RuntimeError("Startup initialization failed.") from e

    # ---------------------------------------------------------
    # 🔸 shutdown event
    # ---------------------------------------------------------
    @app.on_event("shutdown")
    async def on_shutdown():
        """graceful shutdown for db + ai services"""
        try:
            logger.info("🧹 initiating graceful shutdown...")
            shutdown_system()
            logger.info("✅ system shutdown complete.")
        except Exception as e:
            logger.error(f"❌ error during shutdown: {e}")

    # ---------------------------------------------------------
    # 🔸 route registration
    # ---------------------------------------------------------
    app.include_router(api_routes.router, prefix="/api/v1", tags=["api"])
    app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["admin"])
    app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["auth"])

    # ---------------------------------------------------------
    # 🔸 root endpoint
    # ---------------------------------------------------------
    @app.get("/", tags=["root"])
    async def root():
        """root route — simple health indicator"""
        return {
            "status": "ok",
            "message": f"🧠 {APP_NAME} backend is operational.",
            "environment": ENVIRONMENT,
            "version": APP_VERSION,
        }

    logger.info("✅ FastAPI app factory initialized successfully.")
    return app
