"""
Abstract tables (sketch).
"""
from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = "accounts"
    id          = Column(BigInteger, primary_key=True)
    account_ref = Column(String(64), unique=True, index=True)
    display     = Column(String(128))
    value_a     = Column(Float, default=0.0)
    value_b     = Column(Float, default=0.0)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
