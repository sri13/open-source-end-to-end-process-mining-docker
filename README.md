# 📘  Open Source End-to-End Process Mining (Dockerized Fork)

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

### 2. Clone the fork
```bash
git clone https://github.com/<your-username>/open-source-end-to-end-process-mining.git
cd open-source-end-to-end-process-mining

### 3. Build the Docker image
```bash
docker build -t open_source_e2e_process_miner .

### 4. Create an output folder

mkdir output

### 5. Run the pipeline

docker run --rm \
  -v "$PWD/output":/app/output \
  open_source_e2e_process_miner

All generated files will appear in:

./output/

📦 Output Files

The pipeline produces:

event_log.csv — flattened event log

process_data.db — SQLite database

process_map.png — PM4PY DFG visualization

process_map_matplotlib.png — fallback matplotlib diagram


🏗️ Project Structure

open-source-end-to-end-process-mining/
│
├── process_mining.py
├── requirements.txt
├── Dockerfile
├── sample_data.xlsx
├── output/  (created locally)
└── README.md

📝 Credits

This project is based on the original work by Dr. Nick Blackburn:https://github.com/nickblackbourn/open-source-end-to-end-process-mining

This fork simply adds Docker support and compatibility fixes.


📄 License

This fork inherits the license from the original repository.

