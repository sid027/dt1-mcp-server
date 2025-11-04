# MCP Server

## MCP Server Configuration for Claude Desktop

### Locally
```
{
    "mcpServers": {
        "weather": {
          "command": "uv",
          "args": ["run", "--directory", "/Users/singhsiddhartha/Projects/mcp-server-python/", "python3", "service.py"],
          "env": {
            "SSL_VERIFY": "false"
          }
        }
    }
}
```

### Remotely
```
{
    "mcpServers": {
        "weather": {
          "command": "uv",
          "args": ["run", "--directory", "/Users/singhsiddhartha/Projects/mcp-server-python/", "python3", "service.py"],
          "env": {
            "SSL_VERIFY": "false"
          }
        },
        "weather-remote": {
          "command": "npx",
          "args": [
            "mcp-remote",
            "http://34.65.149.151:8000/mcp",
            "--allow-http"
          ],
          "env": {
            "MCP_ACCEPT": "application/json, text/event-stream"
          }
        }
    }
}
```
