from fastapi import Request
from pydantic import BaseModel
from app.utils.logger import logger
import re

# =============================================================
# ⚙️ baseline restricted and adult keyword lists
# =============================================================
RESTRICTED_KEYWORDS = [
    # violence & abuse
    "kill", "murder", "suicide", "rape", "abuse", "violence", "torture",
    "terrorist", "bomb", "attack", "genocide", "massacre", "self-harm",
    "execute", "gun", "weapon", "blood", "stab",
    # illegal / drugs
    "drugs", "marijuana", "cocaine", "heroin", "lsd", "meth", "illegal",
    "narcotic", "smuggle", "trafficking", "cartel",
    # hate speech
    "hate", "racist", "homophobia", "nazi", "discriminate",
    # adult explicit
    "porn", "explicit", "sexual", "fetish", "intercourse", "erotic",
    "nude", "orgasm", "masturbation", "adult content",
]

ADULT_TERMS = [
    "sex", "sexual", "nude", "intimate", "adult", "intercourse",
    "erotic", "sensual", "pleasure", "arousal", "fetish", "foreplay"
]


# =============================================================
# 🧱 schema for safety checks
# =============================================================
class SafetyCheckRequest(BaseModel):
    query: str
    user_age: int | None = None


# =============================================================
# 🔍 keyword-based safety scan
# =============================================================
def scan_for_restricted_keywords(text: str) -> list[str]:
    """
    detects restricted words in text using safe regex boundaries.
    returns a list of detected keywords (case-insensitive)
    """
    detected = []
    lowered = text.lower()

    for word in RESTRICTED_KEYWORDS:
        # regex \b ensures we catch "kill" but not "skill"
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            detected.append(word)
    return list(set(detected))


# =============================================================
# 🔞 check for mature / adult content
# =============================================================
def is_age_restricted(text: str) -> bool:
    """detects adult or mature themes (for 25+ content access)"""
    lowered = text.lower()
    return any(term in lowered for term in ADULT_TERMS)


# =============================================================
# 🧠 main safety check endpoint
# =============================================================
async def safety_check(request: Request, body: SafetyCheckRequest):
    """evaluates a query for safety, maturity, and policy compliance"""
    try:
        query = (body.query or "").strip().lower()
        user_age = int(body.user_age or 0)

        if not query:
            return {
                "status": "error",
                "message": "empty query cannot be processed.",
                "moderation_passed": False
            }

        # 1️⃣ keyword scanning
        detected = scan_for_restricted_keywords(query)
        if detected:
            logger.warning(f"🚫 restricted content detected: {detected}")
            return {
                "status": "error",
                "severity": "high",
                "message": "query blocked due to restricted or unsafe keywords.",
                "detected": detected,
                "moderation_passed": False
            }

        # 2️⃣ adult content check
        if is_age_restricted(query) and user_age < 25:
            logger.info(f"🔞 mature content detected; age restriction applied (age={user_age})")
            return {
                "status": "error",
                "severity": "medium",
                "message": "query blocked. mature content accessible only for 25+ users.",
                "moderation_passed": False
            }

        # 3️⃣ informational flagging (safe query but possible mild topics)
        if any(t in query for t in ["death", "war", "mental health", "crime"]):
            logger.info("⚠️ mild sensitive content detected (info flag).")
            return {
                "status": "warning",
                "severity": "low",
                "message": "query may involve mild sensitive topics; proceed with care.",
                "moderation_passed": True
            }

        # ✅ all checks passed
        logger.info("✅ query passed all safety and moderation checks.")
        return {
            "status": "success",
            "severity": "none",
            "message": "query is safe for processing.",
            "moderation_passed": True
        }

    except Exception as e:
        logger.error(f"❌ safety_check failed: {e}")
        return {
            "status": "error",
            "message": "internal safety system error occurred.",
            "moderation_passed": False
        }


# =============================================================
# 🧩 internal backend utility for controllers
# =============================================================
def check_safety(query: str, user_age: int | None = None) -> bool:
    """
    quick internal version for non-route use.
    returns True if safe, False otherwise.
    """
    try:
        if not query.strip():
            return False

        detected = scan_for_restricted_keywords(query)
        if detected:
            return False

        if is_age_restricted(query) and (user_age or 0) < 25:
            return False

        return True
    except Exception as e:
        logger.error(f"❌ check_safety internal error: {e}")
        return False
