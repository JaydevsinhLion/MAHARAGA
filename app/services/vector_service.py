"""
VectorService — semantic vector storage, retrieval, and management
for the MAHARAGA RAG engine.
"""

import time
import numpy as np
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sentence_transformers import SentenceTransformer

from app.utils.logger import logger
from app.utils.constants import QDRANT_URL, QDRANT_COLLECTION, EMBEDDING_MODEL


# =============================================================
# 🧩 VectorService Class
# =============================================================
class VectorService:
    """Handles vector embeddings, storage, and retrieval for semantic search."""

    def __init__(self):
        """Initialize Qdrant and the embedding model safely"""
        self.qdrant = None
        self.model = None
        start_time = time.time()

        try:
            logger.info("🧠 initializing vector service...")
            self.model = SentenceTransformer(EMBEDDING_MODEL)
            logger.info(f"✅ embedding model loaded: {EMBEDDING_MODEL}")

            self.qdrant = QdrantClient(url=QDRANT_URL, timeout=5.0)
            logger.info(f"📡 connected to qdrant at {QDRANT_URL}")

            self._ensure_collection()
            elapsed = round(time.time() - start_time, 2)
            logger.info(f"⚙️ vector service ready in {elapsed}s")

        except Exception as e:
            logger.error(f"❌ failed to initialize vector service: {e}")
            self.qdrant, self.model = None, None

    # ---------------------------------------------------------
    def _ensure_collection(self):
        """Ensure collection exists, or create one if missing."""
        try:
            collections = self.qdrant.get_collections().collections
            existing = [c.name for c in collections]

            if QDRANT_COLLECTION not in existing:
                logger.info(f"📦 creating new collection: {QDRANT_COLLECTION}")

                # Detect embedding dimension dynamically
                sample_vec = np.random.rand(768).astype(np.float32)
                self.qdrant.recreate_collection(
                    collection_name=QDRANT_COLLECTION,
                    vectors_config=qmodels.VectorParams(
                        size=len(sample_vec),
                        distance=qmodels.Distance.COSINE
                    ),
                )
                logger.info("✅ qdrant collection created successfully.")
            else:
                logger.info(f"📁 existing collection found: {QDRANT_COLLECTION}")
        except Exception as e:
            logger.error(f"❌ collection check/create failed: {e}")

    # ---------------------------------------------------------
    def embed_text(self, text: str) -> List[float] | None:
        """Generate normalized embedding vector."""
        try:
            if not self.model:
                raise ValueError("embedding model not initialized")

            vector = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
            return vector.tolist()
        except Exception as e:
            logger.error(f"❌ embedding failed: {e}")
            return None

    # ---------------------------------------------------------
    def add_document(self, doc_id: str, text: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add a document with an embedding to Qdrant."""
        if not self.qdrant:
            logger.warning("⚠️ qdrant not available — document not stored.")
            return {"status": "warning", "message": "qdrant not connected."}

        try:
            vector = self.embed_text(text)
            if not vector:
                return {"status": "error", "message": "embedding failed."}

            payload = metadata or {}
            payload["text"] = text

            self.qdrant.upsert(
                collection_name=QDRANT_COLLECTION,
                points=[
                    qmodels.PointStruct(
                        id=doc_id,
                        vector=vector,
                        payload=payload
                    )
                ],
            )
            logger.info(f"📥 vector document added id={doc_id}")
            return {"status": "success", "message": "document embedded successfully."}
        except Exception as e:
            logger.error(f"❌ add_document failed: {e}")
            return {"status": "error", "message": str(e)}

    # ---------------------------------------------------------
    def search_similar(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Retrieve semantically similar items from Qdrant."""
        if not self.qdrant:
            logger.warning("⚠️ qdrant unavailable, returning empty search results.")
            return []

        try:
            vector = self.embed_text(query)
            if not vector:
                return []

            results = self.qdrant.search(
                collection_name=QDRANT_COLLECTION,
                query_vector=vector,
                limit=limit,
            )

            formatted = [
                {
                    "text": r.payload.get("text", ""),
                    "score": round(float(r.score), 4),
                }
                for r in results
                if r.payload
            ]

            logger.info(f"🔎 {len(formatted)} results found for semantic query.")
            return formatted
        except Exception as e:
            logger.error(f"❌ search_similar failed: {e}")
            return []

    # ---------------------------------------------------------
    def clear_collection(self):
        """Delete all documents from the current collection."""
        try:
            if not self.qdrant:
                logger.warning("⚠️ qdrant unavailable, cannot clear collection.")
                return
            self.qdrant.delete_collection(QDRANT_COLLECTION)
            logger.warning(f"🧹 cleared qdrant collection: {QDRANT_COLLECTION}")
        except Exception as e:
            logger.error(f"❌ clear_collection failed: {e}")


# =============================================================
# ⚙️ Global shared instance (singleton)
# =============================================================
try:
    vector_service = VectorService()
except Exception as e:
    logger.error(f"❌ failed to initialize global vector service: {e}")
    vector_service = None


# =============================================================
# 🔹 Helper for external modules (rag_service, orchestrator)
# =============================================================
def retrieve_context(query: str, intent: str | None = None, k: int = 3):
    """
    lightweight wrapper around vector_service.search_similar()
    so other modules can import a consistent interface.
    """
    try:
        if not vector_service:
            logger.warning("⚠️ vector service not initialized — no retrieval possible.")
            return []

        results = vector_service.search_similar(query, limit=k)
        if not results:
            logger.info(f"ℹ️ no similar context found for: '{query[:50]}...'")
            return []
        return results
    except Exception as e:
        logger.error(f"❌ retrieve_context failed: {e}")
        return []
