from fastapi import Query, Request
from fastapi.responses import JSONResponse
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/operations/get_all", tags=['Operations'])
async def balance(tg_id: str = Query(None)):
    session = DB.getSession()
    try:
        print(tg_id)
        session.begin()
        operations = await OperationsRepository.get_paginate_operations(session)
        session.close()
        operations_data = [
            {
                "id": op.id,
                "amount": float(op.amount),
                "type": op.type.value if hasattr(op.type, 'value') else str(op.type),
                "description": op.description,
                "created_at": op.created_at.isoformat(),
                "cash_account_id": op.cash_account_id,
                "to_cash_account_id": op.to_cash_account_id,
                "category_id": op.category_id
            }
            for op in operations
        ]
        return JSONResponse(
            status_code=200,
            content={"operations": operations_data, "success": True},
        )
    except Exception as e:
        print(e)
        session.close()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.get("/api/operations/get_operation", tags=['Operations'])
async def createOperation(tg_id: str = Query(None), oper_id = Query(None)):
    pass
    
@app.post("/api/operations/create", tags=['Operations'])
async def createOperation(tg_id: str = Query(None)):
    pass

@app.delete("/api/operations/create", tags=['Operations'])
async def deleteOperation(tg_id: str = Query(None)):
    pass

@app.patch("/api/operations/update_operation", tags=['Operations'])
async def updateOperation(tg_id: str = Query(None)):
    pass
