from fastapi import Query, Request
from fastapi.responses import JSONResponse

from src.modules.accounts.accountsRepository import AccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.db import DB

from .index import app

@app.get("/api/cash_accounts/balance")
async def balance(tg_id: str = Query(None)):
    print(tg_id)
    session = DB.getSession()
    cashAccount = await CashAccountRepository.get(session, tg_id)
    operationStat = await OperationsRepository.getOperationsStat(session, cashAccount.id) 
    # print(mainCashAccount.id)
    return JSONResponse(
        content={"total": "500000", "income": "120000", "expense": "40000"}
    )


@app.get("/api/cash_accounts/get_all")
async def balance(req: Request):
    return JSONResponse(
        content={"total": "500000", "income": "120000", "expense": "40000"}
    )
