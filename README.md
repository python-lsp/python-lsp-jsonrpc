# Python JSON RPC Server

A Python 3.6+ server implementation of the [JSON RPC 2.0](http://www.jsonrpc.org/specification) protocol. This library has been pulled out of the [Python LSP Server](https://github.com/python-lsp/python-lsp-server) project.

## Installation

    pip install -U python-lsp-jsonrpc

## Examples

The examples directory contains two examples of running language servers over websockets. `examples/langserver.py` shows how to run a language server in-memory. `examples/langserver_ext.py` shows how to run a subprocess language server, in this case the Python LSP Server.

Start by installing `tornado` and `python-lsp-server`

    pip install python-lsp-server[all] tornado

Then running `python examples/langserver.py` or `python examples/langserver_ext.py` will host a websocket on ``ws://localhost:3000/python``.
