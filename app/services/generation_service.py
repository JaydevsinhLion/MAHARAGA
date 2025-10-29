import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from app.utils.logger import logger
from app.utils.constants import MODEL_NAME, MAX_TOKENS


# =============================================================
# 🧩 maharaga generation service
# =============================================================
class MaharagaModel:
    """handles text generation for maharaga system"""

    def __init__(self):
        """initialize tokenizer and model safely"""
        try:
            logger.info(f"🧠 loading maharaga model: {MODEL_NAME} ...")
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(self.device)
            logger.info("✅ model loaded successfully")
        except Exception as e:
            logger.error(f"❌ model loading failed: {e}")
            self.tokenizer, self.model, self.device = None, None, "cpu"

    # ---------------------------------------------------------
    # core generation function
    # ---------------------------------------------------------
    def generate_text(self, prompt: str) -> str:
        """generate a text continuation for the given prompt"""
        if not self.model or not self.tokenizer:
            logger.error("⚠️ model not initialized.")
            return "system error: model not available."

        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_TOKENS,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            cleaned = response[len(prompt):].strip() or response.strip()
            return cleaned.lower()
        except torch.cuda.OutOfMemoryError:
            logger.error("❌ gpu memory overflow during generation.")
            return "unable to process request due to limited gpu memory."
        except Exception as e:
            logger.error(f"❌ text generation failed: {e}")
            return "internal error occurred during text generation."
