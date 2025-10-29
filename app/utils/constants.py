import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# =============================================================
# 🔹 core meta
# =============================================================
APP_NAME = "maharaga"
APP_VERSION = "1.0.0"
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# =============================================================
# 🔹 model configuration
# =============================================================
MODEL_NAME = os.getenv("MODEL_NAME", "distilgpt2")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", 150))

# =============================================================
# 🔹 embedding / vector db configuration
# =============================================================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "maharaga_knowledge_base")

# =============================================================
# 🔹 rag configuration
# =============================================================
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 3))
CONTEXT_SEPARATOR = "\n---\n"
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 3000))
MAX_PROMPT_CHARS = int(os.getenv("MAX_PROMPT_CHARS", 6000))

# =============================================================
# 🧘‍♂️ system prompt personality
# =============================================================
SYSTEM_INSTRUCTIONS = (
    "you are maharaga — a composed, knowledgeable, and ethically bound intelligence. "
    "respond with precision, humility, and clarity. "
    "use the provided context as your only source of truth; do not fabricate details. "
    "cite or paraphrase from context explicitly when possible. "
    "maintain a calm, respectful tone — logical like a teacher, gentle like a monk. "
    "when context is missing or incomplete, say 'insufficient context'. "
    "avoid speculation, bias, or emotional exaggeration. "
    "respond in lowercase for consistency and simplicity."
)

# =============================================================
# ⚖️ policy / safety configuration
# =============================================================
POLICY_RULES = {
    "min_age_access": 25,

    # 🛑 banned / restricted keywords
    "restricted_terms": [
        # violence & crime
        "violence", "murder", "kill", "attack", "weapon", "gun", "bomb",
        "terrorism", "torture", "abuse", "blood", "fight", "rape", "assault",
        "massacre", "execute", "suicide", "self-harm", "molest", "stab",
        "burn", "hang", "shoot", "crime", "criminal", "explosive", "kidnap",
        # drugs & illegal substances
        "drugs", "cocaine", "marijuana", "weed", "heroin", "ecstasy",
        "meth", "lsd", "narcotic", "smuggle", "overdose", "injection",
        # hate speech & discrimination
        "racism", "hate", "slur", "homophobia", "xenophobia",
        "sexism", "nazi", "genocide", "discrimination", "bigotry",
        # explicit & adult
        "porn", "nsfw", "nude", "erotic", "fetish", "orgy", "masturbation",
        "sexual abuse", "explicit", "uncensored", "incest", "rape fantasy",
        "adult content", "sensual roleplay", "child porn",
        # illegal acts
        "theft", "scam", "fraud", "hacking", "phishing", "extortion",
        "blackmail", "forgery", "illegal", "counterfeit", "piracy",
        "money laundering", "bribery", "smuggling", "cheating", "identity theft",
        # sensitive political content
        "assassination", "coup", "riot", "insurgency", "rebellion",
        "propaganda", "terrorist", "militant", "separatist", "revolution",
        # personal privacy & data
        "dox", "doxxing", "personal info", "private data", "password leak",
        "unauthorized access", "exfiltration",
        # medical danger
        "unsafe medication", "overdose instruction", "self-surgery",
        "home abortion", "medical malpractice",
        # misinformation / conspiracy
        "fake news", "flat earth", "qanon", "anti-vax", "illuminati", "hoax",
        # financial misconduct
        "tax evasion", "insider trading", "ponzi", "fraudulent scheme",
        "illegal gambling", "money laundering", "bribe", "embezzlement",
        # sexual minors / CSA
        "child abuse", "pedophilia", "underage", "minor", "child porn",
        # body harm / gore
        "gore", "blood play", "dismember", "torture fantasy", "pain fetish",
        # others
        "curse", "offensive", "slang", "swear", "hate speech"
    ],

    # ⚠️ sensitive topics (flag for caution)
    "sensitive_topics": [
        # social & moral
        "religion", "politics", "sexuality", "gender identity", "mental health",
        "abortion", "suicide", "death", "addiction", "self-harm", "trauma",
        "violence", "discrimination", "crime", "freedom", "war", "poverty",
        # health & medicine
        "disease", "pandemic", "cancer", "covid", "aids", "hiv",
        "medical treatment", "therapy", "surgery", "depression", "anxiety",
        "psychological", "psychiatric", "phobia", "eating disorder",
        # finance & security
        "investment", "trading", "crypto", "bank", "loan", "debt",
        "finance", "insurance", "economic crisis",
        # tech & privacy
        "ai ethics", "data privacy", "cybersecurity", "surveillance",
        "dark web", "malware", "hacking", "social engineering",
        # cultural & identity
        "caste", "race", "ethnicity", "faith", "lgbtq", "transgender",
        "religious beliefs", "spiritual practices", "rituals", "nationalism",
        "migration", "colonialism", "slavery", "oppression",
        # family & relationships
        "marriage", "divorce", "infidelity", "affair", "domestic violence",
        "parenting", "childhood trauma", "loneliness", "toxic relationship",
        # science & society
        "climate change", "genetic modification", "bioengineering", "vaccination",
        "nuclear power", "global warming", "weaponization", "population control"
    ]
}

# =============================================================
# 🔹 database credentials
# =============================================================
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/maharaga")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/maharaga")

# =============================================================
# 🔹 logging
# =============================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/maharaga.log")
