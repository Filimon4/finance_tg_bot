from asyncio import sleep
from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(
  title='Finnace management server',
  description='Web server for telegram mini app bot',
  version='0.1', 
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/test/balance')
async def balance(req: Request):
  return JSONResponse(content={
      "total": "500000",
      "income": "120000",
      "expense": "40000"
  })

@app.get('/api/test/operation_history')
async def operation_history():
  return [
    {"category": "food", "amount": "1200"}
  ]

@app.get('/api/test/accounts')
async def accounts():
  return [
    {"name": "Account1", "main": "true"}
  ]

@app.get('/api/test/overview')
async def overview():
  return {"test": "test"}
