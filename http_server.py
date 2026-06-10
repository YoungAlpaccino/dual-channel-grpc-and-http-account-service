"""
FastAPI HTTP mirror (sketch).

Same operations, same service layer. The HTTP side just adds JSON
serialisation and a couple of dashboards-friendly endpoints.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from database import get_db, init_db
from schemas import UpsertRequest, UpsertReply, AccountView
from service import AccountService

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(title="account-service-http", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
_svc = AccountService()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/accounts/{ref}", response_model=AccountView)
async def get_account(ref: str, db=Depends(get_db)):
    row = await _svc.get(db, ref)
    if row is None:
        raise HTTPException(404, "no such account")
    return AccountView.from_row(row)


@app.post("/accounts/upsert", response_model=UpsertReply)
async def upsert_account(req: UpsertRequest, db=Depends(get_db)):
    row = await _svc.upsert(
        db,
        account_ref=req.account_ref,
        display=req.display,
        value_a=req.value_a,
        value_b=req.value_b,
    )
    return UpsertReply(ok=True, account_ref=row.account_ref)
