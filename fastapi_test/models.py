from sqlalchemy import (
    Column,
    Float,
    DateTime,
    #ForeignKey,
    Integer,
    String,
    Enum as SqlEnum,
)
import enums as technamin_enums
from database import Base


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