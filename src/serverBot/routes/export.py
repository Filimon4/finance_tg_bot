from fastapi import HTTPException, Query, Request
from fastapi.responses import JSONResponse
from src.db.models.CashAccount import CashAccount
from src.db.models.Operations import Operations
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationCreateDTO, OperationUpdateDTO, OperationsRepository

from ..index import app


@app.get("/api/export/export_request", tags=['Export'])
def export_request():
  try:
    print('export_request')
  except Exception as e:
    return JSONResponse(
      status_code=500,
      content={'success': False}
    )