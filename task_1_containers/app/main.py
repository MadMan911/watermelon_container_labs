from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start app")
    yield
    print("exit app")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "hello, itmo :)"}
