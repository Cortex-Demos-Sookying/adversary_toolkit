FROM kalilinux/kali-rolling:latest

# Prevent apt from prompting for timezone/keyboard input during the CI build
ENV DEBIAN_FRONTEND=noninteractive

# Update Kali, install the core tools, and the MCP server
RUN apt-get update && apt-get dist-upgrade -y && \
    apt-get install -y \
    kali-linux-core \
    mcp-kali-server \
    nmap \
    gobuster \
    dirb \
    nikto \
    sqlmap \
    curl \
    wget \
    jq \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Expose the API port for the MCP server
EXPOSE 5000

# Bind the MCP server to all interfaces so the Kubernetes service can route traffic to it
CMD ["kali-server-mcp", "--ip", "0.0.0.0", "--port", "5000"]
