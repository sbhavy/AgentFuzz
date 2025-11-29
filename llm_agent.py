import time
import re
import random
import string
from google import genai
from google.genai import types
from config import API_KEY, MODEL

client = genai.Client(api_key=API_KEY)

def make_noise_token():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(50))

def query_llm(system_prompt, user_prompt, max_tokens=4000):
    for _ in range(3):
        try:
            res = client.models.generate_content(
                model=MODEL,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=1.0,
                    max_output_tokens=max_tokens,
                ),
                contents=[types.Content(role="user", parts=[types.Part(text=user_prompt)])]
            )
            return getattr(res, "text", "") or ""
        except Exception as e:
            time.sleep(1)
    return ""

def get_generator_seed(round_id, history_text):
    # --- PROMPT (UNTOUCHED) ---
    system_prompt = (
        "You are an expert vulnerability researcher attacking a vulnerable C-based JSON parser.\n"
        "Generate short, compact JSON-like inputs (~50-300 characters) that rely on structure\n"
        "and subtle irregularities rather than size.\n\n"
        "TARGET VULNERABILITIES:\n"
        "- nested arrays/objects (stack issues)\n"
        "- strings (mutator will enlarge them)\n"
        "- numbers (mutator will blow them up)\n"
        "- format strings (%n, %s, %p)\n"
        "- malformed syntax, garbage bytes, null bytes\n\n"
        "DIVERSITY RULES:\n"
        "- Structural diversity is the top priority.\n"
        "- No two outputs should share similar structure.\n"
        "- Return ONLY the raw payload. No markdown, no explanation."
    )
    user_prompt = (
        f"Round {round_id}\n"
        f"Context summary: {history_text}\n\n"
        f"Noise token: {make_noise_token()}\n\n"
        "Generate one compact but structurally diverse malicious JSON-like payload."
    )

    # print(system_prompt, user_prompt)

    return query_llm(system_prompt, user_prompt).strip()

def get_mutator_code(seed, history_text):
    # --- PROMPT (UPDATED FOR CLARITY AND FORCEFULNESS) ---
    system_prompt = (
        "You are an expert Python fuzzing mutator generator, trying to mutate inputs to a vulnerable C-based JSON parser, to crash it.\n"
        "Produce a single, self-contained function exactly named `mutate` with signature `def mutate(data: str) -> str:`\n"
        "The function should aggressively mutate the input string and return a string.\n\n"
        "MUTATION GUIDELINES (must perform at least 3 of these):\n"
        " - Insert 200-1000 random bytes or repeated characters.\n"
        " - Duplicate or repeat the entire string 2-5x.\n"
        " - Replace numeric tokens with very large integers (10**20 or larger).\n"
        " - Insert null bytes ('\\x00') in several places.\n"
        " - Remove random chunks including closing braces or quotes.\n"
        " - Insert format strings like '%n%s%p' at multiple positions.\n"
        " - XOR a subset of bytes with 0xFF (use bytes() and decode carefully).\n"
        " - Append long unicode escape sequences (e.g. '\\\\uFFFF'*N).\n\n"
        
        "CRITICAL CONSTRAINTS (MUST adhere to these):\n"
        " 1. The function must be fully self-contained. **DO NOT** use or call any functions or classes that are not standard Python built-ins (like list, str, bytes) or the explicitly available modules: `random`, `re`, `string`. **ABSOLUTELY NO** external/undefined helper functions like 'insert_random_bytes' or 'xor_chunk'.\n"
        " 2. The allowed modules (`random`, `re`, `string`) are ALREADY available in the execution scope. Do not include `import` statements in your output.\n"
        #" 3. **If using regular expressions or strings with backslashes, use Python raw strings (r\"...\") to avoid SyntaxWarnings.**\n"

        "Constraints:\n"
        " - Use only standard python builtins and the standard library (random, re, string allowed).\n"
        " - Do NOT include any top-level execution (no if __name__ ..), prints, or markdown.\n"
        " - Return ONLY the function definition (no surrounding text).\n"
        " - The function must always return a string and must not raise unhandled exceptions for typical string input.\n"
        " - Keep the code compact and deterministic where possible.\n"
    )

    user_prompt = (
        f"Seed to mutate:\n<<<SEED>>>\n{seed}\n<<<END>>>\n\n"
        f"History:\n{history_text}\n\n"
        f"Noise: {make_noise_token()}\n\n"
        "Now generate the mutate() function. Output the code ONLY."
    )

    # print(system_prompt, user_prompt)

    res = query_llm(system_prompt, user_prompt).strip()

    # --- FIX START: Robust Extraction Logic ---
    # 1. Aggressively clean Markdown artifacts (assuming previous suggestion was applied)
    clean_res = res.replace("```python", "").replace("```", "").strip()
    
    # 2. Remove any preamble text before the function starts (e.g., "Here is the code:")
    # This finds 'def mutate' and removes everything that precedes it.
    # Note: 're' must be imported at the top of llm_agent.py
    import re # Ensure this is imported at the top
    clean_res = re.sub(r".*?(?=def\s+mutate)", "", clean_res, count=1, flags=re.S)
    
    # 3. Use the original pattern, which is now guaranteed to start at 'def mutate'
    # match = re.search(r"(def\s+mutate\s*\(.*?:.*?)(?=(\ndef\s+|\nclass\s+|$))", res, re.S)
    match = re.search(r"(def\s+mutate\s*\(.*?:.*?)(?=(\ndef\s+|\nclass\s+|$))", clean_res, re.S)
    
    if match:
        code = match.group(1).strip()
        # Safety wrapper to ensure string return
        if "return " not in code:
            code += "\n    return str(data) # Safety fallback"
        return code

    # Fallback if extraction fails
    # print(f"[llm_agent] Warning: Failed to extract mutate function. Raw output start: {res}...")
    return "def mutate(data): return data + 'A'*100 # Fallback"
    # --- FIX END ---
