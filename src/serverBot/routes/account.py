from fastapi import Query
from fastapi.responses import JSONResponse
from src.modules.accounts.accountsRepository import AccountRepository
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/account/balance", tags=['Account'])
async def balance(tg_id: str = Query(None)):
    try:
        with DB.getSession() as session:
            accountBalanceOverview = await AccountRepository.getAccountOverview(session, tg_id)
            print(accountBalanceOverview)
            
            return JSONResponse(
                content={
                    "success": True,
                    **accountBalanceOverview
                }
            )
            return JSONResponse(content=balance_data)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
