"""
Single-process entrypoint (sketch).

Runs both the gRPC server and the HTTP server on the same event loop.
"""
import asyncio
import logging

import uvicorn

from config import settings
from grpc_server import serve as serve_grpc
from http_server import app as http_app

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s")


async def main():
    config = uvicorn.Config(http_app, host="0.0.0.0", port=settings.http_port, log_level="info")
    server = uvicorn.Server(config)

    await asyncio.gather(
        serve_grpc(host="0.0.0.0", port=settings.grpc_port),
        server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
