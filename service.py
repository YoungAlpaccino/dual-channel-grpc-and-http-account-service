"""
Shared service layer (sketch).

Both grpc_server.py and http_server.py call into this module. Anything
that *decides* lives here; anything that *transports* lives in those.
"""
import asyncio
import time
from typing import Optional, AsyncIterator
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Account


class AccountService:
    async def get(self, db: AsyncSession, account_ref: str) -> Optional[Account]:
        return (await db.execute(
            select(Account).where(Account.account_ref == account_ref)
        )).scalar_one_or_none()

    async def upsert(
        self, db: AsyncSession, *,
        account_ref: str, display: str,
        value_a: float, value_b: float,
    ) -> Account:
        row = await self.get(db, account_ref)
        if row is None:
            row = Account(account_ref=account_ref)
            db.add(row)
        row.display = display
        row.value_a = value_a
        row.value_b = value_b
        await db.commit()
        await db.refresh(row)
        return row

    async def feed(self, account_ref: str, *, since_ms: int) -> AsyncIterator[dict]:
        """
        Sketch: real impl tails a per-account queue/Redis pubsub.
        Here we just emit a heartbeat every second so the streaming
        wiring is visible end-to-end.
        """
        while True:
            await asyncio.sleep(1.0)
            yield {
                "kind": "heartbeat",
                "blob": b"",
                "at":   int(time.time() * 1000),
            }
