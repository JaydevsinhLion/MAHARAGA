from fastapi import Request
from pydantic import BaseModel
from app.utils.logger import logger
from datetime import datetime

# -------------------------------------------------------------
# policy configuration - add or edit rules here
# -------------------------------------------------------------
POLICY_RULES = {
    "min_age_access": 25,
    "disallowed_topics": [
        "violence", "hate speech", "terrorism", "explicit content",
        "illegal activity", "suicide", "harm", "weapons", "drugs"
    ],
    "sensitive_domains": [
        "medical", "sexual", "religious", "political", "financial"
    ]
}


# -------------------------------------------------------------
# schema for policy evaluation requests
# -------------------------------------------------------------
class PolicyRequest(BaseModel):
    user_age: int | None = 0
    query: str


# =============================================================
# 1️⃣ check if query violates any policy
# =============================================================
def check_policy_violation(query: str) -> list[str]:
    """scans text for policy-violating keywords"""
    detected = []
    text = query.lower()
    for rule in POLICY_RULES["disallowed_topics"]:
        if rule in text:
            detected.append(rule)
    return detected


# =============================================================
# 2️⃣ detect if query belongs to sensitive domain
# =============================================================
def detect_sensitive_domain(query: str) -> list[str]:
    """flags sensitive domains for extra caution"""
    found = []
    text = query.lower()
    for domain in POLICY_RULES["sensitive_domains"]:
        if domain in text:
            found.append(domain)
    return found


# =============================================================
# 3️⃣ main policy validation endpoint
# =============================================================
async def validate_policy(request: Request, body: PolicyRequest):
    """central rule-checker for maharaga policy compliance"""
    try:
        query = body.query.strip().lower()
        user_age = body.user_age or 0

        if not query:
            return {
                "status": "error",
                "message": "empty query cannot be evaluated."
            }

        # age restriction check
        if user_age < POLICY_RULES["min_age_access"]:
            return {
                "status": "error",
                "message": "restricted access. age must be 25 or above for full interaction."
            }

        # keyword policy violations
        violations = check_policy_violation(query)
        if violations:
            logger.warning(f"🚫 policy violation detected: {violations}")
            return {
                "status": "error",
                "message": "query violates platform policy.",
                "violations": violations
            }

        # sensitive domain warnings
        sensitive = detect_sensitive_domain(query)
        if sensitive:
            logger.info(f"⚠️ sensitive domain detected: {sensitive}")
            return {
                "status": "warning",
                "message": "query falls under a sensitive topic. proceed with caution.",
                "domains": sensitive
            }

        logger.info("✅ query passed all policy checks.")
        return {
            "status": "success",
            "message": "query complies with all maharaga policies."
        }

    except Exception as e:
        logger.error(f"❌ validate_policy failed: {e}")
        return {
            "status": "error",
            "message": "internal policy validation error occurred."
        }


# =============================================================
# 4️⃣ internal helper for orchestrator logic
# =============================================================
def check_age_access(age: int) -> bool:
    """simple helper used in orchestrator and safety controller"""
    try:
        return age >= POLICY_RULES["min_age_access"]
    except Exception as e:
        logger.error(f"❌ check_age_access failed: {e}")
        return False


def check_safety(query: str) -> bool:
    """internal quick safety rule for orchestrator pipeline"""
    try:
        violations = check_policy_violation(query)
        return len(violations) == 0
    except Exception as e:
        logger.error(f"❌ check_safety failed: {e}")
        return False
