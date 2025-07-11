# PydanticAI MCP Run Python

he MCP Run Python package is an MCP server that allows agents to execute Python code in a secure, sandboxed environment. It uses Pyodide to run Python code in a JavaScript environment with Deno, isolating execution from the host system.

Features
- Secure Execution: Run Python code in a sandboxed WebAssembly environment
- Package Management: Automatically detects and installs required dependencies
- Complete Results: Captures standard output, standard error, and return values
- Asynchronous Support: Runs async code properly
- Error Handling: Provides detailed error reports for debugging

The MCP Run Python server is distributed as a JSR package and can be run directly using deno run:
```bash
deno run \
  -N -R=node_modules -W=node_modules --node-modules-dir=auto \
  jsr:@pydantic/mcp-run-python [stdio|sse|warmup]
```
where:
- -N -R=node_modules -W=node_modules (alias of --allow-net --allow-read=node_modules --allow-write=node_modules) allows network access and read+write access to ./node_modules. These are required so Pyodide can download and cache the Python standard library and packages
- --node-modules-dir=auto tells deno to use a local node_modules directory
- stdio runs the server with the Stdio MCP transport — suitable for running the process as a subprocess locally
- sse runs the server with the SSE MCP transport — running the server as an HTTP server to connect locally or remotely
- warmup will run a minimal Python script to download and cache the Python standard library. This is also useful to check the server is running correctly.

Usage of jsr:@pydantic/mcp-run-python with PydanticAI is described in the client documentation

## Direct Usage

As well as using this server with PydanticAI, it can be connected to other MCP clients. For clarity, in this example we connect directly using the Python MCP client.

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

code = """
import numpy
a = numpy.array([1, 2, 3])
print(a)
a
"""
server_params = StdioServerParameters(
    command='deno',
    args=[
        'run',
        '-N',
        '-R=node_modules',
        '-W=node_modules',
        '--node-modules-dir=auto',
        'jsr:@pydantic/mcp-run-python',
        'stdio',
    ],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print(len(tools.tools))
            #> 1
            print(repr(tools.tools[0].name))
            #> 'run_python_code'
            print(repr(tools.tools[0].inputSchema))
            """
            {'type': 'object', 'properties': {'python_code': {'type': 'string', 'description': 'Python code to run'}}, 'required': ['python_code'], 'additionalProperties': False, '$schema': 'http://json-schema.org/draft-07/schema#'}
            """
            result = await session.call_tool('run_python_code', {'python_code': code})
            print(result.content[0].text)
            """
            <status>success</status>
            <dependencies>["numpy"]</dependencies>
            <output>
            [1 2 3]
            </output>
            <return_value>
            [
              1,
              2,
              3
            ]
            </return_value>
            """
```
If an exception occurs, status will be install-error or run-error and return_value will be replaced by error which will include the traceback and exception message.

## Dependencies

Dependencies are installed when code is run.

Dependencies can be defined in one of two ways:

Inferred from imports
If there's no metadata, dependencies are inferred from imports in the code, as shown in the example above.

Inline script metadata
As introduced in PEP 723, explained here, and popularized by uv — dependencies can be defined in a comment at the top of the file.

This allows use of dependencies that aren't imported in the code, and is more explicit.

```python
from mcp import ClientSession
from mcp.client.stdio import stdio_client

# using `server_params` from the above example.
from mcp_run_python import server_params

code = """\
# /// script
# dependencies = ["pydantic", "email-validator"]
# ///
import pydantic

class Model(pydantic.BaseModel):
    email: pydantic.EmailStr

print(Model(email='hello@pydantic.dev'))
"""


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool('run_python_code', {'python_code': code})
            print(result.content[0].text)
            """
            <status>success</status>
            <dependencies>["pydantic","email-validator"]</dependencies>
            <output>
            email='hello@pydantic.dev'
            </output>
            """
```
It also allows versions to be pinned for non-binary packages (Pyodide only supports a single version for the binary packages it supports, like pydantic and numpy).

E.g. you could set the dependencies to
```python
# /// script
# dependencies = ["rich<13"]
# ///
```

