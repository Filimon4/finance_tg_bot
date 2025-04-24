from asyncio.log import logger
from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import Result, Select, func, select
from src.modules.finance.types import OperationType
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountCreate, CashAccountRepository, DeleteCashAccount, UpdateCashAccount, UpdateMainAccount
from src.db.models.CashAccount import CashAccount
from src.db.models.Operations import Operations
from src.db.index import DB
from pydantic import BaseModel
from ..index import app
from sqlalchemy.orm import Session

@app.get("/api/cash_accounts/all", tags=['Cash Account'], description='Получить список всех кассовых счетов')
async def getCashAccounts(tg_id: int = Query(None), page: int = 0, limit: int = 100):
    try:
        with DB.get_session() as session:
            accounts = CashAccountRepository.getAll(session, tg_id, page, limit)
            account_data = [
                {
                    "id": acc.id,
                    "name": acc.name,
                    "account_id": acc.account_id,
                    "currency_id": acc.currency_id,
                    "created_at": str(acc.created_at),
                }
                for acc in accounts
            ]
            return JSONResponse(
                status_code=200,
                content={"success": True, "all": account_data}
            )
    except Exception as e:
        logger.error(f"Error in getCashAccounts: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
            
@app.get("/api/cash_accounts/main", tags=['Cash Account'], description='Получить основной счёт')
async def getMainCashAccounts(tg_id: int = Query(None), page: int = 0, limit: int = 100):
    try:
        with DB.get_session() as session:
            account = CashAccountRepository.getMain(session, tg_id)
            if not account: raise Exception("There is not main cash_account")
            account_data = {
                "id": account.id,
                "name": account.name,
                "account_id": account.account_id,
                "currency_id": account.currency_id,
                "created_at": str(account.created_at),
            }
            return JSONResponse(
                status_code=200,
                content={"success": True, "main": account_data}
            )
    except Exception as e:
        logger.error(f"Error in getCashAccounts: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
            

@app.get("/api/cash_accounts/{id}", tags=['Cash Account'], description='Получить кассовый счет по ID')
async def getCashAccount(id: int):
    try:
        with DB.get_session() as session:
            account = CashAccountRepository.get(session, id)
            if not account:
                raise HTTPException(status_code=404, detail="Cash account not found")
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "account": {
                        "id": int(account.id),
                        "name": str(account.name),
                        "created_at": str(account.created_at),
                        "account_id": int(account.account_id),
                        "currency_id": int(account.currency_id),
                    }
                }
            )
    except HTTPException:
        logger.error(f"Error in get_cash_account: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    except Exception as e:
        logger.error(f"Error in get_cash_account: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/api/cash_accounts/{tg_id}/overview", tags=['Cash Account'], description='Получить сводку по всем счетам')
async def getCashAccountsOverview(tg_id: int):
    try:
      with DB.get_session() as session:
        accounts = CashAccountRepository.getAll(session, tg_id)
        accountsOverview = []

        for acc in accounts:
            accountData = CashAccountRepository.getCashAccountOverview(session, acc.id)
            accountsOverview.append({
                "id": acc.id,
                "account_id": accountData['account'].id,
                "account_name": accountData['account'].name,
                "total_income": float(accountData['total_income']),
                "total_expenses": float(accountData['total_expenses']),
                "current_balance": float(accountData['total_income']) - float(accountData['total_expenses'])
            })

        return JSONResponse(
            status_code=200,
            content={"accounts_overview": accountsOverview},
        )
    except HTTPException as e:
       logger.error(e)
       return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    except Exception as e:
      logger.error(f"Error in get_cash_account: {str(e)}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    

@app.get("/api/cash_accounts/{id}/overview", tags=['Cash Account'], description='Получить сводку по конкретному счету')
async def getSingleCashAccountOverview(id: int):
    try:
      with DB.get_session() as session:
        accountData = CashAccountRepository.getCashAccountOverview(session, id)
        if not accountData:
            raise HTTPException(status_code=404, detail="Cash account not found")
        
        accountDataJson = {
            "account_id": accountData['account'].id,
            "account_name": accountData['account'].name,
            "total_income": float(accountData['total_income']),
            "total_expenses": float(accountData['total_expenses']),
            "current_balance": float(accountData['total_income']) - float(accountData['total_expenses'])
        }

        return JSONResponse(
            status_code=200,
            content={'account': accountDataJson}
        )
    except Exception as e:
      logger.error(f"Error in get_cash_account: {str(e)}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )


@app.post("/api/cash_accounts", tags=['Cash Account'], description='Создать новый кассовый счет')
async def createCashAccount(account_data: CashAccountCreate):
    try:
      with DB.get_session() as session:
        new_account = CashAccount(
          name=account_data.name,
          account_id=account_data.account_id,
          currency_id=account_data.currency_id
        )
        session.add(new_account)
        session.commit()
        return JSONResponse(
           status_code=200,
           content={"success": True, "account": {
                    "id": new_account.id,
                    "name": new_account.name,
                    "account_id": new_account.account_id,
                    "currency_id": new_account.currency_id,
                    "created_at": str(new_account.created_at),
                }}
        )
    except Exception as e:
      logger.error(f"Error in get_cash_account: {str(e)}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    

@app.patch("/api/cash_accounts", tags=['Cash Account'], description='Обновить кассовый счет')
async def updateCashAccount(account_data: UpdateCashAccount):
    try:
      with DB.get_session() as session:
        account = session.query(CashAccount).filter(CashAccount.id == account_data.id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Cash account not found")

        account.name = account_data.name
        session.commit()

        return JSONResponse(
          status_code=200,
          content={"success": True, "account": {
                    "id": int(account.id),
                    "name": str(account.name),
                    "account_id": int(account.account_id),
                    "currency_id": int(account.currency_id),
                    "created_at": str(account.created_at),
                }}
        )
    except Exception as e:
      logger.error(f"Error in get_cash_account: {str(e)}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    
@app.patch("/api/cash_accounts/main", tags=['Cash Account'], description='Получить основной счёт')
async def setMainCashAccount(data: UpdateMainAccount, tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            account = CashAccountRepository.getMain(session, tg_id)
            if account:
                if account.id == data.id:
                    account_data = {
                        "id": account.id,
                        "name": account.name,
                        "account_id": account.account_id,
                        "currency_id": account.currency_id,
                        "created_at": str(account.created_at),
                    }
                    return JSONResponse(
                        status_code=200,
                        content={"success": True, "main": account_data}
                    )
            
            newMainAccount = CashAccountRepository.setMain(session, tg_id, data.id)
            account_data = {
                "id": newMainAccount.id,
                "name": newMainAccount.name,
                "account_id": newMainAccount.account_id,
                "currency_id": newMainAccount.currency_id,
                "created_at": str(newMainAccount.created_at),
            }
            return JSONResponse(
                status_code=200,
                content={"success": True, "main": account_data}
            )
    except Exception as e:
        logger.error(f"Error in getCashAccounts: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.delete("/api/cash_accounts", tags=['Cash Account'], description='Удалить кассовый счет')
async def deleteCashAccount(data: DeleteCashAccount):
    try:
      with DB.get_session() as session:
        account = session.query(CashAccount).filter(CashAccount.id == data.id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Cash account not found")

        session.delete(account)
        session.commit()
        return JSONResponse(
          status_code=200,
          content={"success": True, "message": "Cash account deleted successfully"}
        )
    except Exception as e:
      logger.error(f"Error in get_cash_account: {str(e)}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    
