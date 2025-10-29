"""
rag_service — retrieval-augmented generation utility
handles context retrieval, prompt assembly, and fallback logic
"""

from typing import List, Dict, Optional
from app.utils.logger import logger
from app.services.vector_service import vector_service
from app.utils.constants import (
    RAG_TOP_K,
    CONTEXT_SEPARATOR,
    MAX_CONTEXT_CHARS,
    MAX_PROMPT_CHARS,
    SYSTEM_INSTRUCTIONS,
)


# =============================================================
# 🔹 text cleaning helpers
# =============================================================
def _sanitize_text(text: str) -> str:
    """normalize and clean unicode / whitespace"""
    if not text:
        return ""
    try:
        text = text.encode("utf-8", "ignore").decode("utf-8")
        text = text.replace("\u200b", "").replace("\n", " ").replace("\r", " ")
        return " ".join(text.split())
    except Exception as e:
        logger.warning(f"⚠️ text sanitation failed: {e}")
        return text or ""


def _dedup_texts(items: List[str]) -> List[str]:
    """remove duplicates and near-identical lines"""
    seen, cleaned = set(), []
    for t in items:
        s = _sanitize_text(t)
        if s and s not in seen:
            seen.add(s)
            cleaned.append(s)
    return cleaned


def _truncate_block(text: str, limit: int) -> str:
    """truncate long blocks gracefully while preserving structure"""
    if not text:
        return ""
    if len(text) <= limit:
        return text
    trimmed = text[: limit - 3].rstrip() + "..."
    return trimmed


# =============================================================
# 🔹 context builder
# =============================================================
def build_contextual_prompt(query: str, context_docs: Optional[List[Dict]] = None) -> str:
    """
    build a fully structured prompt for the generation model.
    includes:
      • system behavior instructions
      • joined, deduped contextual docs
      • explicit question / answer cues
    """
    try:
        q = _sanitize_text(query)
        contexts = [(_sanitize_text(d.get("text", "")) or "") for d in (context_docs or [])]
        contexts = _dedup_texts([c for c in contexts if c])

        joined_context = CONTEXT_SEPARATOR.join(contexts)
        joined_context = _truncate_block(joined_context, MAX_CONTEXT_CHARS)

        prompt = (
            f"<<system>> {SYSTEM_INSTRUCTIONS.lower().strip()}\n"
            f"<<context>>\n{joined_context}\n"
            f"{CONTEXT_SEPARATOR}"
            f"<<question>> {q.lower()}\n"
            f"<<answer>> respond precisely using only the context above. "
            f"if the context is missing or insufficient, say 'insufficient context'."
        )

        prompt = _truncate_block(prompt, MAX_PROMPT_CHARS)
        return prompt

    except Exception as e:
        logger.error(f"❌ build_contextual_prompt failed: {e}")
        return (
            f"<<system>> {SYSTEM_INSTRUCTIONS.lower().strip()}\n"
            f"<<question>> {_sanitize_text(query)}\n"
            f"<<answer>>"
        )


# =============================================================
# 🔹 rag pipeline: retrieve + assemble + return
# =============================================================
def assemble_rag_prompt(query: str, intent: Optional[str] = None, k: Optional[int] = None) -> dict:
    """
    1️⃣ retrieves top-k semantic matches
    2️⃣ builds contextual prompt
    3️⃣ returns structured payload (prompt + docs)
    """
    try:
        k = k or RAG_TOP_K
        if not vector_service:
            raise RuntimeError("vector service unavailable")

        retrieved = vector_service.search_similar(query, limit=k) or []
        prompt = build_contextual_prompt(query, retrieved)

        return {
            "status": "success",
            "prompt": prompt,
            "context_docs": retrieved,
            "count": len(retrieved),
            "message": "contextual prompt assembled successfully.",
        }

    except Exception as e:
        logger.error(f"❌ assemble_rag_prompt failed: {e}")
        return {
            "status": "error",
            "prompt": build_contextual_prompt(query, []),
            "context_docs": [],
            "count": 0,
            "message": "failed to assemble rag prompt.",
        }


# =============================================================
# 🔹 simplified retrieval for external modules
# =============================================================
def get_context_only(query: str, intent: Optional[str] = None, k: Optional[int] = None) -> List[Dict]:
    """quick helper for controllers that only need retrieved docs"""
    try:
        k = k or RAG_TOP_K
        if not vector_service:
            logger.warning("⚠️ vector service not initialized — returning empty context.")
            return []
        docs = vector_service.search_similar(query, limit=k)
        logger.info(f"🔍 retrieved {len(docs)} docs for preview context.")
        return docs
    except Exception as e:
        logger.error(f"❌ get_context_only failed: {e}")
        return []
