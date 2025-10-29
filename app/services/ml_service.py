"""
maharaga ml service
-------------------
handles model training, fine-tuning, and persistence (.pkl saving).
automatically creates missing folders/files and integrates with
maharaga's embedding + generation subsystems.
"""

import os
import joblib
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
)
from app.utils.logger import logger
from app.utils.constants import MODEL_NAME
from app.utils.embeddings import embedding_helper

# =============================================================
# 🔹 constants and auto-path creation
# =============================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../"))
MODEL_ROOT = os.path.join(ROOT_DIR, "models")
TRAINED_MODEL_DIR = os.path.join(MODEL_ROOT, "trained")
TRAINED_METADATA_FILE = os.path.join(TRAINED_MODEL_DIR, "metadata.pkl")
TRAINING_OUTPUT = os.path.join(ROOT_DIR, "training_output")
LOG_DIR = os.path.join(ROOT_DIR, "logs")

# ensure directories exist
for folder in [MODEL_ROOT, TRAINED_MODEL_DIR, TRAINING_OUTPUT, LOG_DIR]:
    os.makedirs(folder, exist_ok=True)
logger.info("📁 verified or created all required directories for maharaga ml service.")


# =============================================================
# 🔹 maharaga ml service
# =============================================================
class MaharagaMLService:
    """self-managing ml service for maharaga ai system."""

    def __init__(self):
        self.model_name = MODEL_NAME
        self.model = None
        self.tokenizer = None
        logger.info(f"🧠 initializing maharaga ml service using base model: {self.model_name}")
        self._load_or_initialize()

    # ---------------------------------------------------------
    def _load_or_initialize(self):
        """load fine-tuned model if available; else load base transformer."""
        try:
            if os.path.exists(os.path.join(TRAINED_MODEL_DIR, "config.json")):
                self.model = AutoModelForCausalLM.from_pretrained(TRAINED_MODEL_DIR)
                self.tokenizer = AutoTokenizer.from_pretrained(TRAINED_MODEL_DIR)
                logger.info("✅ fine-tuned model loaded from disk.")
            else:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
                logger.info("📦 base pretrained model loaded (no fine-tuned version found).")
        except Exception as e:
            logger.error(f"❌ model initialization failed: {e}")
            self.model, self.tokenizer = None, None

    # ---------------------------------------------------------
    def _safe_create_file(self, path: str):
        """ensure file exists (empty if not)"""
        try:
            if not os.path.exists(path):
                with open(path, "w", encoding="utf-8") as f:
                    f.write("")
                logger.info(f"📄 created missing file: {path}")
        except Exception as e:
            logger.warning(f"⚠️ could not create file {path}: {e}")

    # ---------------------------------------------------------
    def train_from_csv(self, csv_path: str, text_column: str = "text", epochs: int = 1):
        """fine-tunes model using csv file; auto-creates folder if missing."""
        try:
            if not os.path.exists(csv_path):
                logger.warning(f"⚠️ csv file not found at {csv_path}, creating placeholder.")
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)
                self._safe_create_file(csv_path)
                return {
                    "status": "error",
                    "message": f"csv file not found; placeholder created at {csv_path}",
                }

            df = pd.read_csv(csv_path)
            if text_column not in df.columns:
                logger.error(f"❌ column '{text_column}' not found in csv.")
                return {"status": "error", "message": f"missing column '{text_column}'"}

            texts = df[text_column].astype(str).tolist()
            if len(texts) == 0:
                return {"status": "error", "message": "csv file is empty."}

            dataset = Dataset.from_dict({"text": texts})
            logger.info(f"📚 loaded {len(dataset)} samples from {csv_path}")

            def tokenize(batch):
                return self.tokenizer(batch["text"], truncation=True, padding=True)

            dataset = dataset.map(tokenize, batched=True, num_proc=2)

            training_args = TrainingArguments(
                output_dir=TRAINING_OUTPUT,
                num_train_epochs=epochs,
                per_device_train_batch_size=2,
                save_total_limit=1,
                logging_dir=LOG_DIR,
                logging_steps=10,
                learning_rate=5e-5,
                overwrite_output_dir=True,
            )

            trainer = Trainer(model=self.model, args=training_args, train_dataset=dataset)

            logger.info("⚙️ starting fine-tuning process...")
            trainer.train()
            logger.info("✅ fine-tuning completed successfully.")
            self.save_model()
            return {"status": "success", "message": "model fine-tuned and saved."}

        except Exception as e:
            logger.error(f"❌ training failed: {e}")
            return {"status": "error", "message": str(e)}

    # ---------------------------------------------------------
    def train_from_text(self, texts: list[str], epochs: int = 1):
        """fine-tunes the model directly from a list of texts."""
        try:
            if not texts or not isinstance(texts, list):
                return {"status": "error", "message": "no valid text data provided."}

            dataset = Dataset.from_dict({"text": texts})
            def tokenize(batch):
                return self.tokenizer(batch["text"], truncation=True, padding=True)
            dataset = dataset.map(tokenize, batched=True)

            training_args = TrainingArguments(
                output_dir=TRAINING_OUTPUT,
                num_train_epochs=epochs,
                per_device_train_batch_size=2,
                save_total_limit=1,
                logging_steps=10,
                learning_rate=5e-5,
            )

            trainer = Trainer(model=self.model, args=training_args, train_dataset=dataset)
            logger.info("⚙️ fine-tuning with in-memory data...")
            trainer.train()
            self.save_model()
            logger.info("✅ fine-tuning complete.")
            return {"status": "success", "message": "in-memory fine-tuning completed."}
        except Exception as e:
            logger.error(f"❌ fine-tuning from text failed: {e}")
            return {"status": "error", "message": str(e)}

    # ---------------------------------------------------------
    def save_model(self):
        """save model weights, tokenizer, and metadata safely."""
        try:
            os.makedirs(TRAINED_MODEL_DIR, exist_ok=True)
            self.model.save_pretrained(TRAINED_MODEL_DIR)
            self.tokenizer.save_pretrained(TRAINED_MODEL_DIR)
            metadata = {"base_model": self.model_name, "trained_dir": TRAINED_MODEL_DIR}
            joblib.dump(metadata, TRAINED_METADATA_FILE)
            logger.info(f"💾 saved model and tokenizer to {TRAINED_MODEL_DIR}")
            return {"status": "success", "message": "model saved successfully."}
        except Exception as e:
            logger.error(f"❌ model save failed: {e}")
            return {"status": "error", "message": str(e)}

    # ---------------------------------------------------------
    def generate_text(self, prompt: str, max_length: int = 150) -> str:
        """generate text safely using the fine-tuned or base model."""
        try:
            if not self.model or not self.tokenizer:
                self._load_or_initialize()
            if not prompt or not isinstance(prompt, str):
                return "error: invalid prompt"
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_length=max_length)
            text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info("🧩 text generated successfully.")
            return text.strip()
        except Exception as e:
            logger.error(f"❌ generation failed: {e}")
            return "error: generation failed"

    # ---------------------------------------------------------
    def encode_text(self, text: str):
        """create embedding vector using sentence-transformer."""
        try:
            if not text.strip():
                return None
            return embedding_helper.get_vector(text)
        except Exception as e:
            logger.error(f"❌ embedding generation failed: {e}")
            return None
