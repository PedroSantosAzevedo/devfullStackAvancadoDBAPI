import random
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
from models.location import *
from models.locationArea import *    

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "This is the other service"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"response": "pong"})


#@app.get("/randomLocation")
async def get_random_location():
    location = random.randint(1,10)
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location/{location}")
        if response.status_code == 200:
            data = response.json()
            loc =  Location(**data)
            return JSONResponse(content=loc.model_dump_json())
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.get("/randomArea/{area_id}")
async def get_random_area(area_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://pokeapi.co/api/v2/location-area/{area_id}")
        if response.status_code == 200:
            data = response.json()
            loc =  LocationArea(**data)
            return JSONResponse(content=loc.model_dump_json())
        else:
            return JSONResponse(content={"error": "Location not found"}, status_code=404)

@app.get("/randomLocationTest")
async def get_random_location_test():
    return await get_random_location()