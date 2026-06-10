"""
Pydantic contracts for the HTTP channel (sketch).
"""
from pydantic import BaseModel


class UpsertRequest(BaseModel):
    account_ref: str
    display: str
    value_a: float
    value_b: float


class UpsertReply(BaseModel):
    ok: bool
    account_ref: str


class AccountView(BaseModel):
    account_ref: str
    display:     str
    value_a:     float
    value_b:     float

    @classmethod
    def from_row(cls, row):
        return cls(
            account_ref=row.account_ref,
            display=row.display,
            value_a=row.value_a,
            value_b=row.value_b,
        )
