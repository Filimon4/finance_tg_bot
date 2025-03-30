from fastapi import Query
from fastapi.responses import JSONResponse
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/account/balance", tags=['Account'])
async def balance(tg_id: str = Query(None)):
    session = DB.getSession()
    try:
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
