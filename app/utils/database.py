import os
import time
from pymongo import MongoClient, errors as mongo_errors
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from dotenv import load_dotenv
from app.utils.logger import logger

# =============================================================
# 🔹 Load environment variables
# =============================================================
load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:123@localhost:5432/maharaga_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/maharaga")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# =============================================================
# 🔹 Global connection placeholders
# =============================================================
postgres_engine = None
mongo_client = None
mongo_db = None
qdrant_client = None


# =============================================================
# 🔸 Helper: retry logic
# =============================================================
def _retry_connection(func, retries=3, delay=2, name="service"):
    """generic retry handler for transient connection issues"""
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            logger.warning(f"⚠️ {name} connection attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(delay * attempt)
            else:
                logger.error(f"❌ {name} connection permanently failed after {retries} attempts.")
                return None


# =============================================================
# 🐘 PostgreSQL connection
# =============================================================
def connect_postgres():
    """create SQLAlchemy connection to PostgreSQL"""
    global postgres_engine
    try:
        postgres_engine = create_engine(
            POSTGRES_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            connect_args={"connect_timeout": 5},
        )

        # validate connection
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        logger.info("🟢 connected to PostgreSQL successfully.")
        return postgres_engine
    except SQLAlchemyError as e:
        logger.error(f"❌ PostgreSQL connection failed: {e}")
        return None


# =============================================================
# 🍃 MongoDB connection
# =============================================================
def connect_mongo():
    """connect to MongoDB and return the database instance"""
    global mongo_client, mongo_db
    try:
        mongo_client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=4000,
            maxPoolSize=50,
            connectTimeoutMS=3000,
        )
        # validate connection
        mongo_client.admin.command("ping")
        mongo_db = mongo_client.get_default_database()
        db_name = mongo_db.name or MONGO_URI.rsplit("/", 1)[-1]
        logger.info(f"🍃 connected to MongoDB database: {db_name}")
        return mongo_db
    except mongo_errors.PyMongoError as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        return None


# =============================================================
# 📦 Qdrant Vector DB connection
# =============================================================
def connect_qdrant():
    """connect to Qdrant vector database"""
    global qdrant_client
    try:
        qdrant_client = QdrantClient(url=QDRANT_URL, timeout=5.0)
        # quick ping check
        collections = qdrant_client.get_collections()
        if collections and "collections" in collections:
            logger.info(f"📦 connected to Qdrant successfully ({len(collections['collections'])} collections found).")
        else:
            logger.info("📦 connected to Qdrant (no collections yet).")
        return qdrant_client
    except UnexpectedResponse as e:
        logger.error(f"❌ Qdrant API response error: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ Qdrant connection failed: {e}")
        return None


# =============================================================
# 🔗 Combined setup call
# =============================================================
def connect_databases():
    """initialize all database connections (with retries)"""
    logger.info("🔗 initializing database connections...")
    _retry_connection(connect_postgres, name="PostgreSQL")
    _retry_connection(connect_mongo, name="MongoDB")
    _retry_connection(connect_qdrant, name="Qdrant")
    logger.info("✅ all database connection checks complete.")


# =============================================================
# 🧩 Accessor helpers
# =============================================================
def get_postgres_engine():
    """return SQLAlchemy engine, reconnecting if needed"""
    global postgres_engine
    if postgres_engine is None:
        postgres_engine = _retry_connection(connect_postgres, name="PostgreSQL")
    return postgres_engine


def get_mongo_db():
    """return the Mongo database instance, reconnecting if needed"""
    global mongo_db
    if mongo_db is None:
        mongo_db = _retry_connection(connect_mongo, name="MongoDB")
    return mongo_db


def get_qdrant_client():
    """return Qdrant client instance, reconnecting if needed"""
    global qdrant_client
    if qdrant_client is None:
        qdrant_client = _retry_connection(connect_qdrant, name="Qdrant")
    return qdrant_client
