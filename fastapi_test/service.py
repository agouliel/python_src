import models as technamin_models
from sqlalchemy.future import select

def update_bet(data, db):
    ticket_id = data['ticket_id']

    ticket = (
        db.query(technamin_models.TechnaminBetJunk)
        .filter(technamin_models.TechnaminBetJunk.ticket_id == ticket_id)
        .first()
    )
    if ticket is None:
        return 'Ticket not found'
    
    # update
    ticket.payout_bets = data["bets"]
    db.commit()
    return

async def update_bet_async(data, db):
    ticket_id = data['ticket_id']

    # AttributeError: 'AsyncSession' object has no attribute 'query'
    # so we have to use select
    q = select(technamin_models.TechnaminBetJunk).where(technamin_models.TechnaminBetJunk.ticket_id == ticket_id)
    
    # https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
    #ticket = await db.execute(q).first() # AttributeError: 'coroutine' object has no attribute 'first'
    result = await db.execute(q)
    ticket = result.scalars().first()

    if ticket is None:
        return 'Ticket not found'
    
    ticket.payout_bets = int(data['bets'])
    await db.commit()
    return