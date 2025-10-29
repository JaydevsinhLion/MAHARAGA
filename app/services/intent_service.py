from app.utils.logger import logger

# =============================================================
# 🧩 massive intent dictionary — v2.0 (extended coverage)
# =============================================================
INTENT_KEYWORDS = {
    # core technical & development
    "code": [
        "python", "javascript", "typescript", "react", "nextjs", "node", "api", "program",
        "function", "loop", "class", "variable", "bug", "error", "debug", "html", "css",
        "java", "cpp", "c++", "c#", "swift", "flutter", "kotlin", "sql", "database",
        "mongodb", "postgres", "mysql", "backend", "frontend", "framework", "library",
        "deploy", "render", "docker", "kubernetes", "pipeline", "git", "github", "vscode",
        "compiler", "algorithm", "data structure", "exception", "package", "npm", "pip"
    ],

    # devops + cloud + infrastructure
    "devops": [
        "aws", "azure", "gcp", "server", "deployment", "ssh", "linux", "ubuntu",
        "container", "dockerfile", "k8s", "kubernetes", "ci/cd", "load balancer", "nginx",
        "apache", "virtual machine", "instance", "dns", "route 53", "ssl", "firewall",
        "network", "proxy", "port", "configuration", "bash", "shell", "terminal", "cli"
    ],

    # mathematics & logic
    "math": [
        "solve", "calculate", "add", "subtract", "multiply", "divide", "integrate",
        "derivative", "algebra", "geometry", "calculus", "matrix", "vector", "probability",
        "statistic", "mean", "median", "mode", "equation", "inequality", "trigonometry",
        "logarithm", "root", "square root", "theorem", "formula", "simplify"
    ],

    # ai / ml / data science
    "ai_ml": [
        "machine learning", "deep learning", "neural network", "training", "dataset",
        "tensor", "pytorch", "tensorflow", "huggingface", "openai", "gpt", "bert", "llm",
        "model", "tokenizer", "accuracy", "loss", "epoch", "ai", "artificial intelligence",
        "predict", "classify", "nlp", "regression", "clustering", "vision", "image recognition"
    ],

    # science & academic
    "science": [
        "atom", "cell", "molecule", "energy", "reaction", "photosynthesis", "gravity",
        "evolution", "physics", "chemistry", "biology", "organism", "dna", "gene", "microbe",
        "planet", "solar system", "cosmos", "astronomy", "experiment", "quantum", "mechanics",
        "lab", "force", "mass", "velocity", "magnetism", "electricity"
    ],

    # health + medicine
    "health": [
        "medicine", "treatment", "disease", "symptom", "infection", "pain", "diagnosis",
        "doctor", "therapy", "nutrition", "diet", "exercise", "yoga", "mental health",
        "fitness", "cure", "remedy", "pill", "virus", "vaccine", "hospital", "surgery"
    ],

    # finance, economy & crypto
    "finance": [
        "money", "tax", "bank", "loan", "investment", "stock", "market", "interest", "savings",
        "profit", "revenue", "income", "trading", "portfolio", "bitcoin", "ethereum", "crypto",
        "blockchain", "token", "wallet", "mutual fund", "forex", "gold", "debt", "credit",
        "insurance", "inflation", "budget", "salary", "expense", "roi", "nft"
    ],

    # philosophy, mythology, religion
    "philosophy": [
        "life", "truth", "karma", "moksha", "dharma", "enlightenment", "purpose", "meaning",
        "soul", "ethics", "logic", "mind", "being", "nirvana", "duality", "reality",
        "wisdom", "self", "knowledge", "illusion", "scripture", "vedas", "upanishads",
        "buddhism", "stoicism", "existentialism", "bhagavad gita", "geeta", "arjuna", "krishna"
    ],

    "mythology": [
        "vishnu", "shiva", "brahma", "indra", "ram", "hanuman", "mahabharata", "ramayana",
        "kali", "durga", "parvati", "ganesha", "ravana", "pandava", "kurukshetra", "avatar",
        "zeus", "poseidon", "hera", "odin", "thor", "loki", "athena", "apollo", "ra", "anubis"
    ],

    # human relationship, psychology & emotion
    "relationship": [
        "love", "marriage", "relationship", "breakup", "trust", "feelings", "partner",
        "emotion", "sex", "intimacy", "understanding", "friendship", "dating", "connection",
        "boundaries", "argument", "reconcile", "commitment", "compatibility", "flirt", "couple"
    ],

    "psychology": [
        "behavior", "thought", "mindset", "stress", "emotion", "motivation", "depression",
        "therapy", "memory", "subconscious", "personality", "habit", "trauma", "anxiety",
        "counseling", "consciousness", "self-awareness", "inner child"
    ],

    # arts, design, and creativity
    "art_design": [
        "painting", "drawing", "sketch", "design", "figma", "adobe", "illustrator", "poster",
        "logo", "ui", "ux", "composition", "color palette", "typography", "photo", "edit",
        "animation", "graphic", "illustration", "aesthetic", "moodboard"
    ],

    # culture, social, communication
    "social": [
        "society", "culture", "festival", "india", "world", "media", "twitter", "instagram",
        "facebook", "trend", "meme", "influencer", "politics", "community", "freedom",
        "rights", "equality", "justice", "law", "gender", "tradition", "religion", "heritage"
    ],

    # law, governance, and politics
    "law": [
        "constitution", "rights", "justice", "court", "lawyer", "judge", "petition",
        "case", "verdict", "legal", "crime", "act", "contract", "ipc", "bail", "law firm",
        "advocate", "litigation", "arbitration", "government", "policy", "regulation"
    ],

    # education & learning
    "education": [
        "learn", "study", "exam", "homework", "assignment", "degree", "course", "subject",
        "school", "college", "university", "teacher", "student", "tuition", "textbook",
        "notes", "quiz", "knowledge", "revision", "research", "marks", "gpa"
    ],

    # technology, os, computing
    "computing": [
        "os", "windows", "mac", "linux", "android", "ios", "update", "system", "file", "storage",
        "cpu", "ram", "hardware", "software", "version", "install", "driver", "boot", "bios",
        "network", "wifi", "bluetooth", "laptop", "mobile", "tablet", "app", "device"
    ],

    # art of war / strategy / history
    "strategy": [
        "battle", "war", "army", "strategy", "tactics", "leadership", "victory", "enemy",
        "defense", "weapon", "planning", "political strategy", "business strategy",
        "sun tzu", "art of war", "negotiation", "power", "influence"
    ],

    # business, marketing, branding
    "business": [
        "startup", "brand", "marketing", "sales", "customer", "growth", "analytics",
        "strategy", "lead", "revenue", "profit", "kpi", "campaign", "seo", "sem", "smm",
        "google ads", "facebook ads", "branding", "pitch", "investor", "funding", "b2b", "b2c"
    ],

    # lifestyle & personal development
    "self_growth": [
        "motivation", "discipline", "success", "failure", "focus", "goals", "habits",
        "productivity", "self improvement", "routine", "growth", "confidence", "mindfulness",
        "inspiration", "balance", "consistency", "vision", "purpose", "patience"
    ],

    # entertainment, movies, games, sports
    "entertainment": [
        "movie", "music", "song", "film", "series", "netflix", "anime", "manga", "game",
        "sports", "football", "cricket", "basketball", "tennis", "guitar", "dance", "sing",
        "playstation", "xbox", "nintendo", "marvel", "dc", "superhero", "bollywood", "hollywood"
    ],

    # geography & history
    "history": [
        "ancient", "medieval", "king", "emperor", "dynasty", "freedom", "revolution",
        "war", "civilization", "timeline", "period", "british", "independence", "empire",
        "gandhi", "nehru", "world war", "mughal", "roman", "greek", "egypt", "china", "japan"
    ],

    # general fallback
    "general": []
}


# =============================================================
# 🧠 detect query intent
# =============================================================
def detect_intent(query: str) -> str:
    """detects the most likely intent from a massive keyword dataset"""
    try:
        text = query.lower().strip()
        if not text:
            return "unknown"

        matched_intents = []

        for intent, keywords in INTENT_KEYWORDS.items():
            for word in keywords:
                if word in text:
                    matched_intents.append(intent)
                    break

        if not matched_intents:
            return "general"

        # priority order (if multiple matches)
        priority = ["ai_ml", "code", "math", "philosophy", "relationship", "health"]
        for p in priority:
            if p in matched_intents:
                logger.info(f"🧭 detected intent: {p}")
                return p

        # fallback to first detected
        result = matched_intents[0]
        logger.info(f"🧭 detected intent: {result}")
        return result

    except Exception as e:
        logger.error(f"❌ detect_intent failed: {e}")
        return "unknown"
