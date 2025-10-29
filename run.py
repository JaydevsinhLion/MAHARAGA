"""
Maharaga Run Script
-------------------
Entry point for launching the Maharaga backend server.
Supports both development (reload) and production (optimized) modes.
"""

import uvicorn
from app import create_app
from app.config import ENVIRONMENT, APP_NAME, APP_VERSION
from app.utils.logger import logger

# =============================================================
# 🔹 create FastAPI app
# =============================================================
app = create_app()

# =============================================================
# 🔹 run with environment-based configuration
# =============================================================
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000

    logger.info("──────────────────────────────────────────────")
    logger.info(f"🚀 launching {APP_NAME} v{APP_VERSION}")
    logger.info(f"🌍 environment: {ENVIRONMENT}")
    logger.info(f"🔗 running at: http://{host}:{port}")
    logger.info("──────────────────────────────────────────────")

    # switch reload mode dynamically
    reload_mode = ENVIRONMENT in ["development", "local"]

    uvicorn.run(
        "run:app",
        host=host,
        port=port,
        reload=reload_mode,
        workers=1 if reload_mode else 4,
        log_level="info",
    )
