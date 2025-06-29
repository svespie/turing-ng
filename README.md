# turing-ng

**Turing-ng** is a modular harness for red teaming, adversarial testing, and security evaluation of large language models (LLMs). The framework is designed for offensive security professionals, ML engineers, and researchers interested in automating prompt injection, jailbreak, and agentic attack scenarios against both local and cloud-hosted LLMs.

## Setup
### 1. Clone the Repository
``` bash
git clone https://github.com/svespie/turing-ng.git
```

### 2. Environment Configuration
Copy the example environment file and fill in your values as needed:

``` bash
cd turing-ng
cp .env.example .env
chmod 600 .env
```

Edit `.env` to supply any required API keys or configuration options.

### 3. Virtual Environment Setup
Choose either a standard python virtual environment _**OR**_ a [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) environment (recommended).

Python Virtual Environment
``` bash
python -m venv venv-trap
source venv-trap/bin/activate
```

Conda Environment
``` bash
conda create -n trap python=3.11
conda activate trap
```

### 4. Install Requirements
``` bash
pip install -r requirements.txt
```

## Inspiration
The architecture and user interface of turing-ng are heavily inspired by [recon-ng](https://github.com/lanmaster53/recon-ng), the modular OSINT framework by Tim Tomes and contributors. This project is a from-scratch reimagining for LLM red teaming, not a fork or direct code derivative.