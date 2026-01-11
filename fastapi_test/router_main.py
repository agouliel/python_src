from fastapi import APIRouter, Request, Depends
import json
#from database import SessionLocal
from dependencies import get_db
from dependencies import get_async_db
import service as TechnaminService
import models as technamin_models
from sqlalchemy.future import select as select_future
from sqlalchemy import select as select_normal

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.post("/post")
async def post(request: Request):
    #print(request) # <starlette.requests.Request object at 0x1081e1c70>
    #print(request.body()) # RuntimeWarning: coroutine 'Request.body' was never awaited
    body = await request.body()
    print(body) # binary
    return {"success": True}

@router.post("/update")
async def update(request: Request, db=Depends(get_db)):
    # Test using:
    # curl -X POST http://127.0.0.1:8000/update -H "Content-Type: application/json" -d '{"ticket_id":"1","bets":"8"}'
    
    # https://stackoverflow.com/questions/77696337/a-formdata-field-called-local-kw-is-added-automatically-as-a-mandatory-argument
    # If we use Depends(SessionLocal):
    # SessionLocal expects local_kw as an optional parameter.
    # And FastAPI is trying to get the value for this parameter from Query parameters.
    # To avoid this, you can create a function and use this new function as a dependency.
    # https://fastapi.tiangolo.com/tutorial/query-params/
    # When you declare other function parameters that are not part of the path parameters,
    # they are automatically interpreted as "query" parameters.
    # (they go after the ? in a URL, separated by & characters)
    
    body = await request.body()
    data = json.loads(body)
    # or: data = await request.json()
    print('UPDATE', data)
    TechnaminService.update_bet(data, db)
    return {"success": True}

@router.post('/update_async')
async def update_async(request: Request, db=Depends(get_async_db)):
    body = await request.body()
    data = json.loads(body)
    print('UPDATE async', data)
    await TechnaminService.update_bet_async(data, db)
    # without await, the above gives the following warning:
    # RuntimeWarning: coroutine 'update_bet_async' was never awaited
    # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
    return {'success': True}

# https://fastapi.tiangolo.com/tutorial/body
@router.post('/update_async_with_model_body')
async def update_async_with_model_body(item: technamin_models.TechnaminBetJunkPydantic, db=Depends(get_async_db)):
    await TechnaminService.update_bet_async_with_pydantic(item, db)
    return {'success': True}

# ++++++++++++++++++++++ SELECT METHODS ++++++++++++++++++++++

@router.post('/select_with_body')
async def select_with_body(request: Request, db=Depends(get_db)):
    # Test using:
    # curl http://127.0.0.1:8000/select_with_body -H "Content-Type: application/json" -d '{"ticket_id":"1"}'
    body = await request.body()
    data = json.loads(body)
    # if we don't use async def and await, we get the below error:
    # TypeError: the JSON object must be str, bytes or bytearray, not coroutine
    ticket_id = data['ticket_id']

    ticket = (
        db.query(technamin_models.TechnaminBetJunk)
        .filter(technamin_models.TechnaminBetJunk.ticket_id == ticket_id)
        .first()
    )
    print(ticket)
    return {'success': True}

@router.get('/select_with_path_param/{ticket_id}')
async def select_with_path_param(ticket_id, db=Depends(get_async_db)):
    # Test using:
    # curl http://127.0.0.1:8000/select_with_path_param/1

    # AttributeError: 'AsyncSession' object has no attribute 'query'
    # so we have to use select
    # (2.0 style querying)
    q = select_future(technamin_models.TechnaminBetJunk).where(technamin_models.TechnaminBetJunk.ticket_id == ticket_id)
    
    # https://stackoverflow.com/questions/68360687/sqlalchemy-asyncio-orm-how-to-query-the-database
    # https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html
    #ticket = await db.execute(q).first() # AttributeError: 'coroutine' object has no attribute 'first'
    result = await db.execute(q)
    ticket = result.scalars().first()

    return ticket.as_dict()

@router.get('/select_with_stream')
async def select_with_stream(session=Depends(get_async_db)):
    # Test using:
    # curl http://127.0.0.1:8000/select_with_stream

    q = select_normal(technamin_models.Transactions)
    
    result = await session.stream(q)
    transactions = [transaction async for transaction in result]
    #print(transactions[0]) # TypeError: Object of type Decimal is not JSON serializable
    return {'success': True}

# FastAPI book, page 79
def user_dep(name: str, password: str):
    # in the book it's: def user_dep(name: str = Params, password: str = Params) but it doesn't work
    valid = True if password else False
    return {'name': name, 'valid': valid}

@router.get('/user')
def get_user(user: dict = Depends(user_dep)) -> dict:
    # test it like this: http://localhost:8000/user?name=alex&password=alex
    return user

@router.get('/user2')
def get_user2(user: user_dep = Depends()) -> dict: # dep function used as type
    return user
