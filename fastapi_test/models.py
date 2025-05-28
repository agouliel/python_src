from sqlalchemy import (
    Column,
    Float,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Enum as SqlEnum,
    Numeric,
)
import enums as technamin_enums
from database import Base

from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/body
class TechnaminBetJunkPydantic(BaseModel):
    ticket_id: str
    bets: int


class TechnaminBetJunk(Base):
    __tablename__ = "technamin_bet_junk"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer) #, ForeignKey("users.id"))
    ticket_id = Column(String)
    currency = Column(String)
    amount = Column(Float)
    amount_type = Column(SqlEnum(technamin_enums.AmountType))
    ticket_type = Column(String)  # TODO
    category = Column(String)
    rate = Column(String)
    created_at = Column(String)
    ip = Column(String)
    location = Column(String)
    device = Column(String)
    agent = Column(String)
    payout_bets = Column(Integer)
    payout_value = Column(Float)
    payout_return = Column(Float)
    payout_unit_stake = Column(Float)
    status = Column(
        SqlEnum(technamin_enums.BetStatus), default=technamin_enums.BetStatus.PENDING
    )
    final_payout = Column(Float, nullable=True, default=0)
    cashout_amount = Column(Float, nullable=True, default=0)
    settled_at = Column(DateTime, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# taken from finance/models.py
class Transactions(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product = Column(SqlEnum(technamin_enums.CASINO_PRODUCTS))
    transaction_reason = Column(SqlEnum(technamin_enums.CASINO_TRANSACTION_REASONS))
    amount = Column(Numeric(20, 2))
    currency = Column(String)
    amount_in_eur = Column(Numeric(20, 2))
    balance_before = Column(Numeric(20, 2))
    balance_after = Column(Numeric(20, 2))
    virtual_sport_balance_before = Column(Numeric(20, 2))
    virtual_sport_balance_after = Column(Numeric(20, 2))
    virtual_casino_balance_before = Column(Numeric(20, 2))
    virtual_casino_balance_after = Column(Numeric(20, 2))
    datetime_created = Column(DateTime)
    transaction_money_type = Column(SqlEnum(technamin_enums.TRANSACTION_MONEY_TYPE))
    external_transaction_id = Column(String, nullable=True)