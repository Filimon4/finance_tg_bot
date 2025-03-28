import json
from fastapi import Query, Request
from fastapi.responses import JSONResponse

from src.modules.accounts.accountsRepository import AccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.db import DB

from .index import app

@app.get("/api/account/balance")
async def balance(tg_id: str = Query(None)):
    session = DB.getSession()
    try:
        print(tg_id)
        session.begin()
        cashAccount = await CashAccountRepository.get(session, tg_id)
        session.close()
        balance_data = await OperationsRepository.getOperationsStat(session, cashAccount.id)
        print(balance_data)
        return JSONResponse(content=balance_data)
    except Exception as e:
        print(e)
        session.close()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/api/cash_accounts/overview")
async def balance(req: Request):
    return JSONResponse(
        content={"total": "500000", "income": "120000", "expense": "40000"}
    )

@app.get("/api/operations/get")
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
