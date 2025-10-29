from sentence_transformers import SentenceTransformer
from app.utils.logger import logger
from app.utils.constants import EMBEDDING_MODEL
import numpy as np


# =============================================================
# 🧠 Embedding Helper Class
# =============================================================
class EmbeddingHelper:
    """handles semantic embeddings for text vectors used in RAG, search, and AI reasoning."""

    def __init__(self):
        self.model = None
        self.model_name = EMBEDDING_MODEL
        self._load_model()

    # ---------------------------------------------------------
    def _load_model(self):
        """load the embedding model safely and efficiently"""
        try:
            logger.info(f"🧠 loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("✅ embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"❌ failed to load embedding model: {e}")
            self.model = None

    # ---------------------------------------------------------
    def get_vector(self, text: str) -> list | None:
        """
        generate a normalized embedding for a single text input.
        returns a list of floats or None on failure.
        """
        if not text or not isinstance(text, str):
            logger.warning("⚠️ empty or invalid text provided for embedding.")
            return None

        if not self.model:
            logger.warning("⚠️ embedding model not initialized; retrying load...")
            self._load_model()
            if not self.model:
                return None

        try:
            embedding = self.model.encode(
                text,
                normalize_embeddings=True,
                show_progress_bar=False
            )
            return embedding.tolist()
        except Exception as e:
            logger.error(f"❌ embedding generation failed: {e}")
            return None

    # ---------------------------------------------------------
    def get_batch_vectors(self, texts: list[str]) -> list[list[float]]:
        """
        generate embeddings for a list of texts.
        returns a list of vector lists (each normalized).
        """
        if not texts or not isinstance(texts, list):
            logger.warning("⚠️ invalid or empty batch input for embeddings.")
            return []

        if not self.model:
            self._load_model()

        try:
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                show_progress_bar=True,
                batch_size=8,
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"❌ batch embedding generation failed: {e}")
            return []

    # ---------------------------------------------------------
    def cosine_similarity(self, vec_a: list, vec_b: list) -> float:
        """compute cosine similarity between two vectors."""
        try:
            if not vec_a or not vec_b:
                return 0.0
            a = np.array(vec_a)
            b = np.array(vec_b)
            sim = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
            return float(sim)
        except Exception as e:
            logger.error(f"❌ cosine similarity computation failed: {e}")
            return 0.0


# =============================================================
# 🔹 Singleton Instance
# =============================================================
embedding_helper = EmbeddingHelper()
