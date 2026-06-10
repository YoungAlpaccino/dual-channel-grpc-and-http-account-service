"""
Sample gRPC client for smoke tests (sketch).
"""
import asyncio
import grpc

try:
    import account_pb2 as pb
    import account_pb2_grpc as pb_grpc
except ImportError:
    pb = pb_grpc = None


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as ch:
        stub = pb_grpc.AccountServiceStub(ch)

        await stub.Upsert(pb.UpsertRequest(
            account_ref="acc-1", display="demo", value_a=1.0, value_b=2.0,
        ))
        got = await stub.Get(pb.GetRequest(account_ref="acc-1"))
        print("get:", got)

        async for ev in stub.StreamFeed(pb.FeedRequest(account_ref="acc-1", since_ms=0)):
            print("feed:", ev.kind, ev.at)


if __name__ == "__main__":
    asyncio.run(main())
