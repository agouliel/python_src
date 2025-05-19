from enum import Enum


class AmountType(Enum):
    MAIN = "main"
    FREE_BET = "free_bet"
    BONUS = "bonus"


class BetStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    WIN = "win"
    LOSS = "loss"
    DRAW = "draw"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    PARTIAL_CASHOUT = "partial_cashout"
    CASHOUT = "cashout"


class SelectionStatus(Enum):
    OPEN = "open"
    WIN = "win"
    LOSS = "loss"
    WIN_VOID = "win-void"
    LOSS_VOID = "loss-void"
    VOID = "void"
    REFUND = "refund"
    DEAD_HEAT = "dead_heat"
