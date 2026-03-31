# WeavScope MCP Docs Server

[![MCPize](https://mcpize.com/badge/@mcpize/mcpize?type=hosted)](https://mcpize.com)

MCP documentation server built with [FastMCP 2.0](https://gofastmcp.com) for [WeavScope](https://github.com/mycin/weavscope) - a clean, multi-tenant wrapper for Weaviate.

## Features

- **Comprehensive Documentation**: Access complete WeavScope API reference, configuration guides, and examples
- **Knowledge Base**: Structured documentation resources for all WeavScope components
- **MCP Resources**: Direct access to documentation via MCP resource protocol
- **Interactive Tools**: Query documentation and examples through MCP tools

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

## Quick Start

```bash
make dev        # Install all dependencies
make run        # Start server
```

Server runs at `http://localhost:8080/mcp`

## Available Tools

| Tool | Description |
|------|-------------|
| `get_weavscope_documentation` | Get comprehensive WeavScope documentation |
| `get_weavscope_examples` | Get usage examples |
| `get_api_reference` | Get detailed API reference |
| `get_configuration_guide` | Get configuration guide |

## Available Resources

| Resource | Description |
|----------|-------------|
| `weavscope://docs/overview` | WeavScope overview |
| `weavscope://docs/getting-started` | Getting started guide |
| `weavscope://docs/technical-reference` | Technical reference |
| `weavscope://examples/basic-usage` | Basic usage example |
| `weavscope://examples/advanced-search` | Advanced search examples |

## Development

```bash
make test       # Run tests
make lint       # Check code style
make format     # Auto-format code
```

## Testing

```bash
npx @anthropic-ai/mcp-inspector http://localhost:8080/mcp
```

## Deploy

```bash
mcpize deploy
```

## Project Structure

```
├── src/
│   ├── server/
│   │   ├── __init__.py
│   │   ├── server.py       # MCP server entry point
│   │   ├── tools.py        # MCP tools and resources
│   │   └── py.typed        # PEP 561 marker
│   └── knowledgebase/
│       ├── __init__.py
│       ├── resources.py    # Knowledge base implementation
│       └── py.typed        # PEP 561 marker
├── tests/
│   └── test_tools.py
├── pyproject.toml
├── Makefile
└── Dockerfile
```

## License

MIT
