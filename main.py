from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return JSONResponse(content={"message": "This is the other service"})

@app.get("/ping")
def ping():
    return JSONResponse(content={"response": "pong"})
