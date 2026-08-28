# 🧪 Ephemeral AI Code Execution Sandbox
 
![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)
 
A lightweight, secure FastAPI microservice designed to safely execute untrusted, AI-generated Python code in isolated, dynamically provisioned Docker environments.
 
---
 
## 📌 1. The Problem
 
When building AI developer tools or agents that generate raw code, executing that LLM-generated output directly on a host server introduces critical security vulnerabilities. Untrusted code can trigger unauthorized network access, memory leaks, system file manipulation, or compute-draining infinite loops.
 
## 🛡️ 2. The Solution
 
This microservice acts as a secure quarantine gateway. It receives raw Python code via a FastAPI webhook, mounts it to an ephemeral Docker container via system subprocesses, executes the payload under strict resource constraints, and instantly destroys the environment.
 
### Core Security Architecture
 
- **Total Network Isolation:** Containers are launched with the `--network none` flag, completely blocking the executed code from making external API calls, establishing reverse shells, or downloading malicious payloads.
- **Ephemeral Execution:** The `--rm` flag ensures the container is instantly destroyed the millisecond execution finishes. Zero state is retained.
- **Compute Constraints & DoS Protection:** Hardcoded memory limits (`--memory 128m`) and dynamic Python-level timeout limits instantly terminate frozen scripts or intentional infinite loops.
---
 
## 🏗️ 3. Architecture
 
```
[Client] ──► [FastAPI Webhook Gateway]
                    │
                    ├─► 1. Receive raw Python payload
                    ├─► 2. Provision ephemeral container (--network none, --rm, --memory 128m)
                    ├─► 3. Execute under timeout constraint
                    └─► 4. Capture stdout/stderr, destroy container
```
 
---
 
## 🔒 4. API Usage
 
### `POST /sandbox/execute`
 
Accepts raw Python code and executes it in the isolated environment.
 
**1. Standard Payload (Safe Code)**
 
```json
{
  "code": "print('Sandbox is operational.')",
  "timeout_seconds": 3
}
```
 
**Response:** Returns `"status": "success"` and the standard output.
 
**2. Network Attack Payload (Blocked)**
 
```json
{
  "code": "import urllib.request; urllib.request.urlopen('http://google.com')",
  "timeout_seconds": 3
}
```
 
**Response:** Instantly blocked by the Docker network daemon, returning the failure in the `stderr` trace.
 
**3. Compute Drain Payload (Terminated)**
 
```json
{
  "code": "while True: pass",
  "timeout_seconds": 2
}
```
 
**Response:** Process is killed automatically after 2 seconds, returning `"status": "timeout"`.
 
---
 
## ⚙️ 5. Infrastructure & Dependencies
 
This project was optimized to run seamlessly in the default GitHub Codespaces Universal Linux environment, relying on the host machine's native Docker daemon rather than nested virtualization, ensuring maximum stability. Dependency versioning is intentionally unpinned (`fastapi`, `uvicorn`, `pydantic`) to allow optimized binary wheel resolution on deployment.
 
---
 
## 💻 6. Local Development Setup
 
1. Clone the repository and launch a GitHub Codespace (using the default Universal image).
2. Create and activate a clean virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
 
3. Install dependencies:
```bash
pip install -r requirements.txt
```
 
4. Start the API gateway:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
 
5. Navigate to `/docs` in your forwarded port to test the execution payloads via the Swagger UI.
---
 
## 📄 License
 
This project is open-source under the MIT License.
 
---
 
*Architected by Shiven Siwach.*
 