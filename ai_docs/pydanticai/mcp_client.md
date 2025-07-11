# PydanticAI MCP Client

PydanticAI can act as an MCP client, connecting to MCP servers to use their tools.

Install
You need to either install pydantic-ai, orpydantic-ai-slim with the mcp optional group:
```bash
uv add "pydantic-ai-slim[mcp]"
```

Usage
PydanticAI comes with the following way to connect to MCP servers:
- MCPServerStdio which runs the server as a subprocess and connects to it using the stdio transport. mcp-run-python is used as the MCP server in the examples.

## MCP "stdio" Server
The transport offered by MCP is the stdio transport where the server is run as a subprocess and communicates with the client over stdin and stdout. In this case, you'd use the MCPServerStdio class.

**Note**: When using MCPServerStdio servers, the agent.run_mcp_servers() context manager is responsible for starting and stopping the server.

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

server = MCPServerStdio(  
    'deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio',
    ]
)
agent = Agent('openai:gpt-4o', mcp_servers=[server])


async def main():
    async with agent.run_mcp_servers():
        result = await agent.run('How many days between 2000-01-01 and 2025-03-18?')
    print(result.output)
    #> There are 9,208 days between January 1, 2000, and March 18, 2025.
```
