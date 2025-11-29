import os
import time
import threading
import concurrent.futures
import random
import atexit 
from config import TARGET, DURATION_MINUTES, DIRS
import utils
import llm_agent

# --- CONFIG ---
MAX_WORKERS = 8
MUTATION_RATE = 0.5
STOP_EVENT = threading.Event()

def save_file(content, path):
    """Simple file saver handling bytes/str."""
    mode = "wb" if isinstance(content, bytes) else "w"
    with open(path, mode, encoding=None if "b" in mode else "utf-8") as f:
        f.write(content)

def fuzz_worker(wid):
# ... (fuzz_worker function remains the same)
    r = 0
    while not STOP_EVENT.is_set():
        r += 1
        
        # 1. DECIDE: Generate New or Mutate Existing?
        try:
            all_seeds = [f for f in os.listdir(DIRS['seeds']) if f.endswith(".txt")]
            valid_seeds = [f for f in all_seeds if not f.startswith("CRASH_")]
        except FileNotFoundError:
            valid_seeds = []

        do_mutate = (len(valid_seeds) > 0) and (random.random() < MUTATION_RATE)

        if not do_mutate:
            # --- GENERATION PHASE ---
            seed = llm_agent.get_generator_seed(f"W{wid}-{r}", utils.format_history_for_gen())
            if not seed: continue
            seed = seed.strip()
            
            # Run Target
            ret_code = utils.run_target(seed, wid)
            is_crash = (ret_code < 0)
            
            # Update History
            utils.update_history({
                'seed': seed,
                'parent_seed': None,
                'mutator_code': None,
                'seed_crash': 1 if is_crash else 0
            })

            if is_crash:
                # print(f"\n[!] CRASH (Gen) Worker {wid}")
                save_file(seed, f"{DIRS['seeds']}/CRASH_gen_w{wid}_r{r}.txt")
            else:
                # Save non-crashing seeds occasionally to build corpus for mutation
                if random.random() < 0.5:
                    save_file(seed, f"{DIRS['seeds']}/w{wid}_r{r}_gen.txt")

        else:
            # --- MUTATION PHASE ---
            try:
                parent_file = random.choice(valid_seeds)
                with open(f"{DIRS['seeds']}/{parent_file}", "r", encoding="utf-8", errors="ignore") as f:
                    parent_content = f.read()

                # Get Mutator Code from LLM
                code = llm_agent.get_mutator_code(parent_content, utils.format_history_for_mut())
                if not code: continue

                # Run Mutator
                mutated = utils.run_python_mutator(code, parent_content)
                
                if mutated:
                    if isinstance(mutated, str): mutated = mutated.strip()
                    
                    # Run Target
                    ret_code = utils.run_target(mutated, wid)
                    is_crash = (ret_code < 0)

                    # Update History
                    utils.update_history({
                        'seed': mutated,
                        'parent_seed': parent_content,
                        'mutator_code': code,
                        'seed_crash': 1 if is_crash else 0
                    })

                    if is_crash:
                        # print(f"\n[!] CRASH (Mut) Worker {wid}")
                        save_file(mutated, f"{DIRS['seeds']}/CRASH_mut_w{wid}_r{r}.txt")
                        save_file(code, f"{DIRS['mutators']}/CRASH_mut_w{wid}_r{r}.py")
                    else:
                        # save_file(code, f"{DIRS['mutators']}/mut_w{wid}_r{r}.py")
                        pass

            except Exception as e:
                # print(f"Worker error: {e}") # Debug only
                pass



def main():
    if not os.path.isfile(TARGET):
        print(f"[!] Target '{TARGET}' not found.")
        return

    utils.reset_directories()
    print(f"[*] Starting {MAX_WORKERS} threads for {DURATION_MINUTES} mins...")
    
    end_time = time.time() + (DURATION_MINUTES * 60)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as exe:
        # Submit the fuzzing workers
        workers = [exe.submit(fuzz_worker, i) for i in range(MAX_WORKERS)]
        
        try:
            # Main loop waits for timeout or interrupt
            while time.time() < end_time:
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n[!] Keyboard interrupt received.")
        
        finally:
            STOP_EVENT.set()
            print("\n[!] Stopping workers and shutting down thread pool...")
            
            # Wait for workers to finish gracefully
            concurrent.futures.wait(workers, timeout=5) 

if __name__ == "__main__":
    main()
