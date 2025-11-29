# AgentFuzz

**Dual-LLM Fuzzer for Fuzzgoat**

AgentFuzz is a vulnerability research tool that leverages Large Language Models (LLMs) to automatically generate seed inputs and custom Python mutators for fuzzing. It operates in two phases: a "Learning Phase" to discover effective crash-inducing strategies, and a "Fuzzing Phase" using AFL++ with the consolidated knowledge.

## Prerequisites

* **Operating System:** Linux (Ubuntu/Debian recommended)
* **AFL++:** Must be installed (`afl-gcc`, `afl-fuzz`).
* **Python:** 3.10+

## Installation

### 1. Install AFL++
Ensure AFL++ is installed. If not, follow the official guide or build from source:

```bash
# Example (Ubuntu):
sudo apt-get update
sudo apt-get install -y afl++ 
# Or compile from source if the package is unavailable
```

### 2. Clone and Build Target (Fuzzgoat)

Clone the vulnerable target and compile it using the AFL compiler wrapper to inject instrumentation.


```bash
git clone [https://github.com/fuzzstati0n/fuzzgoat](https://github.com/fuzzstati0n/fuzzgoat)
cd fuzzgoat
make CC=afl-gcc
cd ..
```

### 3. Install Dependencies

Install the required Python packages for the LLM agent.

```bash
pip install -r requirements.txt
```

