from fastapi import FastAPI
import model
from fastapi import APIRouter, Header, HTTPException

app = FastAPI()


@app.get('/')
def root():
    return {'Hello': 'World'}


@app.get('/batch')
async def batch(string: str):
    return await model.batch(string)


@app.get('/element')
async def element(string: str):
    return await model.element(string)
