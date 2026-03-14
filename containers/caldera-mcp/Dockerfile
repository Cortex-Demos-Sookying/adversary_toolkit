FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install core dependencies, Git, Golang (for Sandcat payloads), and Node.js (for UI)
RUN apt-get update && apt-get install -y \
    git curl build-essential golang nodejs npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/caldera

# Clone Caldera and all default submodules (Arsenal, Sandcat, Stockpile, etc.)
RUN git clone https://github.com/mitre/caldera.git --recursive .

# Clone the MCP plugin directly into the plugins directory
RUN git clone https://github.com/mitre/mcp.git plugins/mcp

# Install core Caldera requirements
RUN pip install --no-cache-dir -r requirements.txt

# Mimic the "VARIANT=full" build argument by installing ALL plugin requirements
RUN for req in plugins/*/requirements.txt; do \
        if [ -f "$req" ]; then \
            pip install --no-cache-dir -r "$req" || echo "Skipping $req due to error"; \
        fi; \
    done

# Build the Caldera UI (Magma)
RUN cd plugins/magma && npm install && npm run build

# Expose Web UI (8888), MLflow/MCP (5000), and Agent Comms (7010, 7011, 7012)
EXPOSE 8888 5000 7010 7011 7012

# Start the Caldera server (--insecure allows HTTP logins for your lab)
CMD ["python", "server.py", "--insecure"]
