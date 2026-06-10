"""
Async gRPC server (sketch).

Every RPC is a tiny adapter: parse the request, hand it to the shared
service layer, marshal the reply. Business logic lives nowhere in this file.
"""
import asyncio
import logging
import grpc

from service import AccountService
from database import SessionFactory

# generated stubs (run generate_proto.py)
try:
    import account_pb2 as pb
    import account_pb2_grpc as pb_grpc
except ImportError:  # before codegen, keep file importable
    pb = pb_grpc = None

logger = logging.getLogger(__name__)


class AccountServicer(pb_grpc.AccountServiceServicer if pb_grpc else object):
    def __init__(self):
        self._svc = AccountService()

    async def Get(self, request, context):
        async with SessionFactory() as db:
            row = await self._svc.get(db, request.account_ref)
        if row is None:
            await context.abort(grpc.StatusCode.NOT_FOUND, "no such account")
        return pb.Account(
            account_ref=row.account_ref,
            display=row.display,
            value_a=row.value_a,
            value_b=row.value_b,
            updated_at=int(row.updated_at.timestamp() * 1000),
        )

    async def Upsert(self, request, context):
        async with SessionFactory() as db:
            row = await self._svc.upsert(
                db,
                account_ref=request.account_ref,
                display=request.display,
                value_a=request.value_a,
                value_b=request.value_b,
            )
        return pb.UpsertReply(ok=True, account_ref=row.account_ref)

    async def StreamFeed(self, request, context):
        async for ev in self._svc.feed(request.account_ref, since_ms=request.since_ms):
            yield pb.FeedEvent(kind=ev["kind"], blob=ev["blob"], at=ev["at"])


async def serve(host: str = "0.0.0.0", port: int = 50051):
    server = grpc.aio.server()
    pb_grpc.add_AccountServiceServicer_to_server(AccountServicer(), server)
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    logger.info("grpc server on %s:%s", host, port)
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
