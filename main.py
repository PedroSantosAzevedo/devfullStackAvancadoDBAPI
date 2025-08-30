from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "This is the other service"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"response": "pong"})


@app.get("/abilities")
async def get_abilities():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://pokeapi.co/api/v2/ability/1")
        return JSONResponse(content=response.json())