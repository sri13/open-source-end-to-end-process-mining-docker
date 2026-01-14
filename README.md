# 🧠 Open Source End-to-End Process Mining (Dockerized Fork)

This repository is a **Docker-enabled fork** of Nick Blackburn’s excellent open-source process mining project.  
The original project provides a complete pipeline:

**Excel → SQLite → Event Log → Process Map → Analytics**

However, the upstream code currently requires **Python 3.9** due to `pm4py` and `graphviz` compatibility issues.  
To make the project easier to run on any machine — Windows, macOS, or Linux — this fork adds a **fully containerized Docker workflow**.

---

## 🚀 Why This Fork Exists

- Python 3.12 breaks `pm4py` and Graphviz bindings  
- Many users struggle with dependency installation in the long run  
- Docker provides a **zero‑setup**, reproducible environment  
- The entire pipeline now runs with a single command

This fork keeps the original code intact while adding a production‑ready Docker setup.

---

## 🐳 Run the Pipeline with Docker (Recommended)

### 1. Clone the fork
```bash
git clone https://github.com/sri13/open-source-end-to-end-process-mining-docker.git
cd open-source-end-to-end-process-mining-docker

****WIP****
### 2. Clone the fork
```bash
