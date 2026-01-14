# Use Python 3.9 image so environment matches your venv
FROM python:3.9-slim

# Install Graphviz (system package) for process visualizations
RUN apt-get update && \
    apt-get install -y graphviz && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project
COPY . .

# Default command: run your pipeline
CMD ["python", "process_mining.py"]
