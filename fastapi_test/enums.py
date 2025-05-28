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


# taken from finance/enums.py
class TRANSACTION_MONEY_TYPE(str, Enum):
    REAL = "Real"
    VIRTUAL = "Virtual"
    BOTH = "Both"


class CASINO_PRODUCTS(str, Enum):
    PRAXIS = "Praxis"
    CASINO = "Casino"
    SPORT = "Sport"
    PAYMENTS = "Payments"


class CASINO_TRANSACTION_REASONS(str, Enum):
    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    REFUND = "Refund"
    DEBIT = "Debit"
    CREDIT = "Credit"
    ROLLBACK = "Rollback"
    DEPOSIT_BONUS = "Deposit Bonus"
    CAMPAIGN_DEACTIVATION = "Campaign Deactivation"
    AWARD_TO_REAL = "Award virtual to real"
    CASHBACK_BONUS = "Cashback Bonus"
    FREEBET_BONUS = "Freebet Bonus"
    FREE_SPIN_DEBIT = "Free Spin Debit"
    FREE_SPIN_CREDIT = "Free Spin Credit"
    IN_HOUSE_PAYMENT = "In House Payment"
    WITHDRAWAL_CANCELLED = "Withdrawal Cancelled"


class DATE_GROUP(str, Enum):
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    HOUR = "hour"
