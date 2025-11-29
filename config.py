import os
import sys

# --- CONFIGURATION ---
TARGET = "./fuzzgoat/fuzzgoat"
DURATION_MINUTES = 1  # Run for 30 minutes
MODEL = "gemini-2.5-flash-lite"
OUT_DIR = "llm-fuzz"

# Output Directories
DIRS = {
    "seeds": f"{OUT_DIR}/seeds", 
    "mutators": f"{OUT_DIR}/mutators"
}

# API Key Validation
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY: 
    sys.exit("Error: Set GEMINI_API_KEY environment variable.")
