from fastapi import FastAPI
import uvicorn
import router_main

app = FastAPI()

app.include_router(router_main.router)

def main():
    port = 8000
    host = '0.0.0.0'
    print(f"[main]: Starting server on port {port}")
    uvicorn.run("main:app", host=host, port=port, reload=True, lifespan="on")

if __name__ == "__main__":
    main()