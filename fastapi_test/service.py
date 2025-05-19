import models as technamin_models

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