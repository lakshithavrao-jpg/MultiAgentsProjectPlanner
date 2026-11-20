import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)

DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "nexus.db"

OUTPUT_DIR = BASE_DIR / "outputs"

ASSETS_DIR = BASE_DIR / "assets"
AGENTS_ASSETS_DIR = ASSETS_DIR / "agents"

for folder in [
    DATABASE_DIR,
    OUTPUT_DIR,
    AGENTS_ASSETS_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)