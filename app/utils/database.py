from pymongo import MongoClient
from sqlalchemy import create_engine
from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# ---------------------------
# Database URLs from .env
# ---------------------------
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:123@localhost:5432/maharaga_db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/maharaga")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# ---------------------------
# Global connection placeholders
# ---------------------------
postgres_engine = None
mongo_client = None
mongo_db = None
qdrant_client = None


# ---------------------------
# PostgreSQL connection
# ---------------------------
def connect_postgres():
    """Create SQLAlchemy connection to PostgreSQL"""
    global postgres_engine
    try:
        postgres_engine = create_engine(POSTGRES_URL)
        conn = postgres_engine.connect()
        print("🟢 Connected to PostgreSQL successfully!")
        conn.close()
        return postgres_engine
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return None


# ---------------------------
# MongoDB connection
# ---------------------------
def connect_mongo():
    """Connect to MongoDB and return the database instance"""
    global mongo_client, mongo_db
    try:
        mongo_client = MongoClient(MONGO_URI)
        mongo_db = mongo_client.get_default_database()
        print("🟢 Connected to MongoDB successfully!")
        return mongo_db
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return None


# ---------------------------
# Qdrant Vector DB connection
# ---------------------------
def connect_qdrant():
    """Connect to Qdrant vector database"""
    global qdrant_client
    try:
        qdrant_client = QdrantClient(url=QDRANT_URL)
        print("🟢 Connected to Qdrant successfully!")
        return qdrant_client
    except Exception as e:
        print(f"❌ Qdrant connection failed: {e}")
        return None


# ---------------------------
# Combined setup call
# ---------------------------
def connect_databases():
    """Initialize all database connections"""
    print("🔗 Initializing database connections...")
    connect_postgres()
    connect_mongo()
    connect_qdrant()
    print("✅ All database connection checks complete.")


# ---------------------------
# Accessor helpers
# ---------------------------
def get_mongo_db():
    """Return the current Mongo database instance"""
    if mongo_db is None:
        return connect_mongo()
    return mongo_db


def get_postgres_engine():
    """Return the SQLAlchemy engine"""
    if postgres_engine is None:
        return connect_postgres()
    return postgres_engine


def get_qdrant_client():
    """Return the Qdrant client"""
    if qdrant_client is None:
        return connect_qdrant()
    return qdrant_client
