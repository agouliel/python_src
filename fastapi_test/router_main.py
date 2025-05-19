from fastapi import APIRouter, Request, Depends
import json
#from database import SessionLocal
from dependencies import get_db
import service as TechnaminService

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
    # SessionLocal expects local_kw as an optional parameter. And FastAPI is trying to get the value for this parameter from Query parameters.
    # To avoid this, you can create a function and use this new function as a dependency.
    
    body = await request.body()
    data = json.loads(body)
    # or: data = await request.json()
    print('UPDATE', data)
    TechnaminService.update_bet(data, db)
    return {"success": True}
