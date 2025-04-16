from asyncio.log import logger
from fastapi import Query
from fastapi.responses import JSONResponse
from src.modules.accounts.accountsRepository import AccountCreateDTO, AccountRepository
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/account/balance_six_month", tags=['Account'])
def balanceSixM(tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            sixMonthOverview = AccountRepository.getAccountSixMonthOverview(session, tg_id)

            sixMonthOverviewJson = [
                {
                    "month": month_year.split('-')[1],  # только месяц "04"
                    "year": month_year.split('-')[0],   # только год "2025"
                    "month_year": month_year,           # полная дата "2025-04"
                    "balance": float(balance) if balance is not None else 0.0
                }
                for month_year, balance in sixMonthOverview
            ]

            return JSONResponse(
                status_code=200,
                content={"success": True, "data": sixMonthOverviewJson}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/account/balance", tags=['Account'])
def balance(tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            accountBalanceOverview = AccountRepository.getAccountOverview(session, tg_id)
            
            return JSONResponse(
                content={
                    "success": True,
                    **accountBalanceOverview
                }
            )
    except Exception as e:
        logger.error(f"{str(e)}")
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
        logger.error(f"{str(e)}")
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
        logger.error(f"{str(e)}")
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
        logger.error(f"{str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    