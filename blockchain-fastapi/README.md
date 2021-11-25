# Blockchain + FastAPI

- mine block
- get the entire blockchain
- get the last mined block
- validate the blockchain

# Usage

https://www.youtube.com/watch?v=G5M4bsxR-7E

>>> import blockchain
>>> bc = blockchain.Blockchain()
>>> bc.chain
>>> bc.mine_block("hello")

uvicorn main:app --reload

http://127.0.0.1:8000/docs
