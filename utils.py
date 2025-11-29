import os
import subprocess
import threading
from collections import deque
from config import TARGET, OUT_DIR, DIRS
# --- ADD THESE IMPORTS ---
import random 
import re
import string
import atexit # <--- NEW IMPORT
# -------------------------


# --- THREAD-SAFE HISTORY ---
history_lock = threading.Lock()
history = deque(maxlen=50)

def reset_directories():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
    for path in DIRS.values():
        os.makedirs(path, exist_ok=True)

def run_target(data, worker_id="main"):
    filename = f"temp_{worker_id}.txt"
    
    # Handle binary vs string data types
    mode = "wb" if isinstance(data, (bytes, bytearray)) else "w"
    encoding = None if "b" in mode else "utf-8"

    try:
        with open(filename, mode, encoding=encoding) as f:
            f.write(data)
    except TypeError:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(data))

    try:
        if not os.path.exists(TARGET): return 0
        proc = subprocess.run([TARGET, filename], capture_output=True, timeout=2)
        return proc.returncode
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 255
    finally:
        if os.path.exists(filename):
            try: os.remove(filename)
            except: pass

def run_python_mutator(py_code, seed_content):
    local_scope = {}
    
    # --- FIX: Define safe execution globals to expose necessary modules ---
    exec_globals = {
        '__builtins__': __builtins__, # Keep standard built-in functions
        'random': random,
        're': re,
        'string': string,
        'bytes': bytes, # Useful for byte manipulation
    }
    # ---------------------------------------------------------------------

    try:
        # Pass the controlled global scope to exec()
        exec(py_code, exec_globals, local_scope)
        if "mutate" not in local_scope: 
            print("[!] Mutator Error: 'mutate' function not found in code.")
            return None
        
        mutated = local_scope["mutate"](seed_content)
        
        if isinstance(mutated, (bytes, bytearray, str)):
            return mutated
        return str(mutated)
    except Exception as e:
        # Keep the debugging line you added
        # print(f"[!] Mutator Execution Error: {e}")
        return None

def update_history(round_data):
    """
    Expects round_data dict with keys: 
    {'seed': str/bytes, 'mutator_code': str/None, 'seed_crash': int}
    """
    with history_lock:
        history.append(round_data)

# In utils.py
def format_history_for_gen():
    with history_lock:
        # Show recent mutators to the Generator (now 3 rounds)
        curr = list(history)[-3:]
    if not curr: return "No previous mutators."
    
    out = []
    for i, e in enumerate(curr):
        code = e.get('mutator_code')
        parent = e.get('parent_seed') # NEW: Get the parent seed

        if not code: continue # Skip generation rounds that had no mutator
        
        crash = "CRASHED" if e.get('seed_crash') else "SAFE"
        
        # Display Parent Seed cleanly
        parent_display = repr(parent) + '...' if parent and len(parent) > 100 else repr(parent)
        
        # Truncate massive code blocks to save tokens
        # if len(code) > 1000: code = code[:1000] + "...(truncated)"
        
        # NEW OUTPUT FORMAT: Added the parent seed line
        out.append(f"--- Round {i} ({crash}) ---\n"
                   f"Input to Mutator: {parent_display}\n"
                   f"Mutator Code:\n{code}\n")
        
    return "\n".join(out) if out else "No previous mutators."

def format_history_for_mut():
    with history_lock:
        # Show recent seeds to the Mutator
        curr = list(history)[-4:]
    if not curr: return "No previous seeds."
    
    out = []
    for e in curr:
        seed_display = repr(e.get('seed',''))
        # if len(seed_display) > 200: 
        #     seed_display = seed_display[:200] + "...(truncated)"
            
        crash = "CRASH" if e.get('seed_crash') else "SAFE"
        out.append(f"Seed: {seed_display} -> Result: {crash}")
        
    return "\n".join(out)
