#!/usr/bin/env python
# encoding: utf-8
"""
AFL++ Python Custom Mutator Wrapper
Implements the required AFL++ API functions and dispatches to the llm_mutators_corpus.
"""

import random
import os
import llm_corpus as llm_logic # Imports your file containing mutate_0, mutate_1, etc.
import time

# --- API Functions for AFL++ ---

def init(seed):
    """
    Called once when AFL++ starts up. Used to seed our RNG.
    """
    random.seed(seed)
    print(f"[*] Initializing AFL++ Python Mutator (Seed: {seed})...")

def deinit():
    """
    Called once when AFL++ shuts down.
    """
    pass

def fuzz(buf, add_buf, max_size):
    """
    The main mutation function, which dispatches to llm_mutators_corpus.py.
    
    @type buf: bytearray
    @param buf: The buffer that should be mutated (the input test case).
    
    @type max_size: int
    @param max_size: Maximum size of the mutated output.
    
    @rtype: bytearray
    @return: A new bytearray containing the mutated data.
    """
    
    # 1. Convert input bytearray (binary data) to a Python string, 
    #    as your original C bridge logic expected a string.
    #    We use 'ignore' to handle potentially invalid UTF-8 in the fuzz corpus.
    with open("/tmp/afl_mutator_log.txt", "a") as f:
        f.write(f"[{time.time()}] Mutator called.\n")
    data_str = buf.decode('utf-8', errors='ignore')

    # 2. Call the mutation dispatch logic from your consolidated file.
    #    This is where the random mutator selection happens.
    mutated_str = llm_logic.dispatch_mutate(data_str)

    # 3. Convert the resulting string back into a bytearray (encoded in UTF-8).
    mutated_bytes = mutated_str.encode('utf-8', errors='ignore')
    
    # 4. Enforce max_size limit.
    if len(mutated_bytes) > max_size:
        # If too large, return the original input buffer (safest fallback).
        return buf
    
    # 5. Return the result as a mutable bytearray object.
    return bytearray(mutated_bytes)