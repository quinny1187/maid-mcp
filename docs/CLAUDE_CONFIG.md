# Maid MCP Configuration for Claude Desktop

Add this to your Claude Desktop configuration file:

```json
"maid": {
  "command": "node",
  "args": ["C:\\repos\\maid-mcp\\maid-server.js"],
  "cwd": "C:\\repos\\maid-mcp"
}
```

## Configuration Location

The Claude Desktop config file is typically located at:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

## Full Example Config

```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-memory"
      ]
    },
    "antiderp": {
      "command": "node",
      "args": [
        "C:\\repos\\mcp-filesystem-server\\antiderp-mcp-server.js",
        "C:\\repos"
      ],
      "env": {
        "ANTIDERP_API_URL": "http://localhost:3333"
      }
    },
    "time": {
      "command": "uvx",
      "args": ["mcp-server-time", "--local-timezone=America/New_York"]
    },
    "maid": {
      "command": "node",
      "args": ["C:\\repos\\maid-mcp\\maid-server.js"],
      "cwd": "C:\\repos\\maid-mcp"
    }
  }
}
```

## Testing

After adding the configuration:
1. Copy the config to Claude Desktop:
   - Copy `claude_desktop_config.json` from this folder
   - Paste to `%APPDATA%\Claude\claude_desktop_config.json`
2. Restart Claude Desktop
3. Check if the maid tools appear in the tool list
4. Try using: "Use the speak tool to say hello"

## Note

A complete config file is available in this folder: `claude_desktop_config.json`
