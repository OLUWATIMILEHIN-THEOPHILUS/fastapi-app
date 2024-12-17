from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

@app.get("/")
def home():
    return {"data": "Home Page"}
