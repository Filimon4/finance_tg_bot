from fastapi import Query, Request
from fastapi.responses import JSONResponse
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository
from ..index import app

@app.get('/api/notifies/get_all', tags=['Notifies'])
async def getAllNotifies():
  pass

@app.get('/api/notifies/get_one', tags=['Notifies'])
async def getOneNotify():
  pass

@app.post('/api/notifies/create', tags=['Notifies'])
async def createNotify():
  pass

@app.patch('/api/notifies/update', tags=['Notifies'])
async def updateNotify():
  pass

@app.delete('/api/notifies/delete', tags=['Notifies'])
async def deleteNotify():
  pass
