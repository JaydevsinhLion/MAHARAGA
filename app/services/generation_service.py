from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class MaharagaModel:
    def __init__(self, model_name: str = "distilgpt2"):
        """Initialize small, local text-generation model"""
        print(f"🧠 Loading Maharaga model: {model_name} ...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print("✅ Model loaded successfully")

    def generate_text(self, query: str, max_length: int = 120) -> str:
        """Generate text reply for given query"""
        inputs = self.tokenizer.encode(query, return_tensors="pt")

        outputs = self.model.generate(
            inputs,
            max_length=max_length,
            num_return_sequences=1,
            do_sample=True,
            top_p=0.95,
            temperature=0.8,
            pad_token_id=self.tokenizer.eos_token_id,
        )

        decoded = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        continuation = decoded[len(query):].strip()

        if not continuation:
            continuation = "Let me reflect on that more deeply..."

        return continuation
