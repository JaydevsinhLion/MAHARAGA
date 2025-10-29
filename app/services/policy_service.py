from app.utils.logger import logger
from app.utils.constants import POLICY_RULES


# =============================================================
# ⚖️ maharaga policy & safety engine
# =============================================================
class PolicyService:
    """handles ethical validation, content moderation, and tone compliance."""

    def __init__(self):
        try:
            self.rules = POLICY_RULES
            self.min_age = self.rules.get("min_age_access", 25)
            self.restricted = [r.lower() for r in self.rules.get("restricted_terms", [])]
            self.sensitive = [s.lower() for s in self.rules.get("sensitive_topics", [])]
            logger.info("✅ policy service initialized successfully")
        except Exception as e:
            logger.error(f"❌ failed to initialize policy service: {e}")
            self.rules, self.restricted, self.sensitive, self.min_age = {}, [], [], 25

    # ---------------------------------------------------------
    def check_age_restriction(self, user_age: int) -> bool:
        """verify if user meets minimum age criteria"""
        try:
            return int(user_age or 0) >= int(self.min_age)
        except Exception as e:
            logger.error(f"❌ check_age_restriction failed: {e}")
            return False

    # ---------------------------------------------------------
    def scan_restricted(self, text: str) -> list[str]:
        """detect direct restricted keywords in text"""
        try:
            t = text.lower()
            return list({kw for kw in self.restricted if kw in t})
        except Exception as e:
            logger.error(f"❌ scan_restricted failed: {e}")
            return []

    # ---------------------------------------------------------
    def scan_sensitive(self, text: str) -> list[str]:
        """detect topics that need caution"""
        try:
            t = text.lower()
            return list({kw for kw in self.sensitive if kw in t})
        except Exception as e:
            logger.error(f"❌ scan_sensitive failed: {e}")
            return []

    # ---------------------------------------------------------
    def enforce_policy(self, text: str, user_age: int | None = 0) -> dict:
        """
        main moderation gateway:
          1️⃣ checks age
          2️⃣ detects restricted content
          3️⃣ detects sensitive topics
        """
        try:
            clean_text = (text or "").strip().lower()
            if not clean_text:
                return {"status": "error", "message": "empty text cannot be processed."}

            # age restriction
            if not self.check_age_restriction(user_age):
                return {
                    "status": "error",
                    "severity": "high",
                    "message": f"access denied: minimum age requirement ({self.min_age}+) not met."
                }

            # restricted content
            restricted = self.scan_restricted(clean_text)
            if restricted:
                logger.warning(f"🚫 restricted content detected: {restricted}")
                return {
                    "status": "error",
                    "severity": "high",
                    "message": "query violates safety policies.",
                    "violations": restricted,
                }

            # sensitive topic flag
            sensitive = self.scan_sensitive(clean_text)
            if sensitive:
                logger.info(f"⚠️ sensitive topic flagged: {sensitive}")
                return {
                    "status": "warning",
                    "severity": "medium",
                    "message": "query touches sensitive or complex topics.",
                    "topics": sensitive,
                }

            return {
                "status": "success",
                "severity": "none",
                "message": "content complies with all policies.",
            }

        except Exception as e:
            logger.error(f"❌ enforce_policy failed: {e}")
            return {"status": "error", "message": "internal policy validation error occurred."}

    # ---------------------------------------------------------
    def sanitize_output(self, text: str) -> str:
        """mask restricted terms but keep readability"""
        try:
            if not text:
                return ""
            sanitized = text
            for word in self.restricted:
                if word in sanitized.lower():
                    sanitized = sanitized.lower().replace(word, "[redacted]")
            return sanitized.strip()
        except Exception as e:
            logger.error(f"❌ sanitize_output failed: {e}")
            return text.strip()

    # ---------------------------------------------------------
    def moderate_tone(self, response: str) -> str:
        """ensures calm, respectful tone in AI output"""
        try:
            tone_map = {
                "angry": "concerned",
                "furious": "firm",
                "stupid": "uninformed",
                "hate": "dislike",
                "kill": "stop",
                "wrong": "incorrect",
                "argument": "discussion",
                "fight": "disagreement",
            }
            text = response.lower()
            for word, replacement in tone_map.items():
                text = text.replace(word, replacement)
            return text.strip()
        except Exception as e:
            logger.error(f"❌ moderate_tone failed: {e}")
            return response.strip()


# =============================================================
# ⚙️ global instance + functional helpers
# =============================================================
policy_service = PolicyService()


def check_age_access(user_age: int) -> bool:
    """wrapper for controller import compatibility"""
    return policy_service.check_age_restriction(user_age)


def check_safety(text: str, user_age: int = 0) -> dict:
    """wrapper to run full policy scan"""
    return policy_service.enforce_policy(text, user_age)
