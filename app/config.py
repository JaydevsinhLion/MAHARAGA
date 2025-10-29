from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "MAHARAGA")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")

print(f"⚙️ Environment: {ENVIRONMENT}")
