from fastapi import Query
from fastapi.responses import JSONResponse
from src.modules.accounts.accountsRepository import AccountCreateDTO, AccountRepository
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/account/balance", tags=['Account'])
def balance(tg_id: str = Query(None)):
    try:
        with DB.getSession() as session:
            accountBalanceOverview = AccountRepository.getAccountOverview(session, tg_id)
            print(accountBalanceOverview)
            
            return JSONResponse(
                content={
                    "success": True,
                    **accountBalanceOverview
                }
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.post("/api/account", tags=['Account'])
def createAccount(data: AccountCreateDTO):
    try:
        with DB.get_session() as session:
            account = AccountRepository.create(session, data.id)
            if not account: raise Exception('failed to create account')
            return JSONResponse(
                status_code=200,
                content={"success": True, "account": {
                    'id': account.id,
                    'created_at': str(account.created_at),
                }}
            )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/account", tags=['Account'])
def getAccount(id: int = Query(None)):
    try:
        with DB.get_session() as session:
            account = AccountRepository.getUserById(session, id)
            if not account: raise Exception('failed to get account')
            return JSONResponse(
                status_code=200,
                content={"success": True, "account": {
                    'id': account.id,
                    'created_at': str(account.created_at),
                }}
            )

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.delete('/api/account', tags=['Account'])
def deleteAccount(id: int = Query(None)):
    try:
        with DB.get_session() as session:
            deleted = AccountRepository.delete(session, id)
            if not deleted: raise Exception('Failed to delete')
            return JSONResponse(
                status_code=200,
                content={"success": True}
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    