FROM python:3.11-slim

# System deps (optional but nice: curl for debugging)
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# App dir
WORKDIR /app

# Install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY server.py .

# Expose HTTP port
EXPOSE 8000

# Optional: set an auth token at runtime with -e MCP_AUTH_TOKEN=...
# Start with Uvicorn using FastMCP's ASGI app for robustness if preferred:
# (either run server.py directly OR run as ASGI app—both are fine)
# Here we just run the script; it calls mcp.run(transport="http", ...)
CMD ["python", "server.py"]
