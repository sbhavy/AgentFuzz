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

### 4. API Configuration

Set your Google Gemini API key as an environment variable, in ```learn.sh```

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### Configuration

Before running the learning agent, review config.py to ensure it matches your environment:

   * TARGET: Path to the executable (default: ./fuzzgoat/fuzzgoat).

   * DURATION_MINUTES: Duration of the learning phase (default: 1 minute).

   * MODEL: The LLM model to use (default: gemini-2.5-flash-lite).

   * DIRS: Output paths for seeds and mutators.


### Usage Workflow

#### Step 1: Learning Phase

Run the learning script. This launches the LLM agent to generate initial seeds and Python mutators, validating them against the target.

```bash
# Generates seeds and mutators in the 'llm-fuzz' directory
python3 learn.py
```

#### Step 2: Consolidate Mutators

Once the learning phase is complete, aggregate the successful mutators into a single corpus file (llm_corpus.py) that AFL++ can utilize.

```bash
python3 consolidate.py
```


#### Step 3: Run AFL++ Fuzzing

Execute the setup script to configure the system (CPU settings, core patterns) and launch the AFL++ fuzzer using the generated assets.

Note: You may need to update the PYTHONPATH in setup-commands.sh to match your local directory structure before running.

```bash
# Make the script executable
chmod +x setup-commands.sh

# Run the system configuration and fuzzer (requires sudo for system settings)
./setup-commands.sh
```

### Directory Structure

 *   learn.py: Main driver for the LLM learning loop.

  *  consolidate.py: Combines discovered mutators into a single Python module.

   * llm_corpus.py: The generated corpus of mutators used by the AFL++ bridge.

   * afl_python_mutator.py: The Python bridge connecting AFL++ to the LLM corpus.

   * setup-commands.sh: Automates system config and starts the fuzzing session.
