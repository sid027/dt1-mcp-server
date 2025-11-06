# MCP Server

## MCP Server Configuration for Claude Desktop

### Locally (Mac)
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

(Windows)
```
{
	"mcpServers": {
                "weather": {
                        "command": "uv",
                        "args": ["--directory", "C:\\Users\\sid\\Projects\\dt1-mcp-server\\", "run", "service.py"],
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
