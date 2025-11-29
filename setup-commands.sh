#!/bin/bash

# --- 1. Automated System Setup (Requires Sudo) ---
echo "[*] Configuring system for AFL++..."

# Set core_pattern to 'core' to prevent external crash handlers from interfering
# 'sudo' is used here; you will be prompted for your password once.
echo core | sudo tee /proc/sys/kernel/core_pattern > /dev/null

# Set CPU scaling governor to 'performance' for all cores
# This uses a loop to safely apply it to all available CPUs
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor > /dev/null

echo "[+] System configuration complete."

# --- 2. Environment Variables ---
export PYTHONPATH="/home/bhavyesh/Desktop/6223/src"
export AFL_PYTHON_MODULE="afl_python_mutator"
export AFL_CUSTOM_MUTATOR_ONLY=1

# --- 3. Run Fuzzer ---
echo "[*] Starting Fuzzer for 15 minutes..."
timeout 15m afl-fuzz -i ./llm-fuzz/seeds/ -o out -- ./fuzzgoat/fuzzgoat @@