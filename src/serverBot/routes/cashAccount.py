from fastapi import HTTPException, Query
from fastapi.responses import JSONResponse
from sqlalchemy import Result, Select, func, select
from src.modules.finance.types import OperationType
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountCreate, CashAccountRepository
from src.db.models.CashAccount import CashAccount
from src.db.models.Operations import Operations
from src.db.index import DB
from pydantic import BaseModel
from ..index import app
from sqlalchemy.orm import Session

@app.get("/api/cash_accounts/get_all", tags=['Cash Account'], description='Получить список всех кассовых счетов')
async def getCashAccounts(skip: int = 0, limit: int = 100):
    try:
        with DB.getSession() as session: #type: Session
            accounts = CashAccountRepository.getAll(session, skip, limit)
            account_data = [
                {
                    "id": acc.id,
                    "name": acc.name,
                    "created_at": acc.created_at,
                    "account_id": acc.account_id,
                    "currency_id": acc.currency_id,
                }
                for acc in accounts
            ]
            return JSONResponse(
                status_code=200,  # Исправлено с 500 на 200 (успешный запрос)
                content={"success": True, "accounts": account_data}
            )
    except Exception as e:
        print(f"Error in getCashAccounts: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
            

@app.get("/api/cash_accounts/get_one", tags=['Cash Account'], description='Получить кассовый счет по ID')
async def getCashAccount(id: int):
    try:
        with DB.getSession() as session:
            account = CashAccountRepository.get(session, id)
            if not account:
                raise HTTPException(status_code=404, detail="Cash account not found")
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "account": {
                        "id": account.id,
                        "name": account.name,
                        "created_at": account.created_at,
                        "account_id": account.account_id,
                        "currency_id": account.currency_id,
                    }
                }
            )
    except HTTPException:
        raise  # Пробрасываем HTTPException как есть (для 404)
    except Exception as e:
        print(f"Error in get_cash_account: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.get("/api/cash_accounts/overview", tags=['Cash Account'], description='Получить сводку по всем счетам')
async def getCashAccountsOverview(tg_id: int = Query(None)):
    try:
      with DB.getSession() as session:
        total_accounts = CashAccountRepository.getOverview(session, tg_id)
        return JSONResponse(
            status_code=200,
            content={"total_accounts": total_accounts},
        )
    except Exception as e:
      print(f"Error in get_cash_account: {e}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    

@app.get("/api/cash_accounts/{id}/overview", tags=['Cash Account'], description='Получить сводку по конкретному счету')
async def getSingleCashAccountOverview(id: int):
    try:
      with DB.getSession() as session:
        accountData = CashAccountRepository.getCashAccountOverview(session, id)
        if not accountData:
            raise HTTPException(status_code=404, detail="Cash account not found")
        
        return JSONResponse(
            status_code=200,
            content={
              "account_id": accountData.account.id,
              "account_name": accountData.account.name,
              "total_income": accountData.total_income,
              "total_expense": accountData.total_expense,
              "current_balance": accountData.total_income - accountData.total_expense
            }
        )
    except Exception as e:
      print(f"Error in get_cash_account: {e}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )


@app.post("/api/cash_accounts/create", tags=['Cash Account'], description='Создать новый кассовый счет')
async def creatCashAccount(account_data: CashAccountCreate):
    try:
      with DB.getSession() as session:
        new_account = CashAccount(
          name=account_data.name,
          account_id=account_data.account_id,
          currency_id=account_data.currency_id
        )
        session.add(new_account)
        session.refresh(new_account)
        print(new_account)
        return new_account
    except Exception as e:
      print(f"Error in get_cash_account: {e}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )

@app.delete("/api/cash_accounts/delete/{id}", tags=['Cash Account'], description='Удалить кассовый счет')
async def delete_cash_account(id: int):
    try:
      with DB.getSession() as session:
        account = session.query(CashAccount).filter(CashAccount.id == id).first()
        if not account:
            raise HTTPException(status_code=404, detail="Cash account not found")

        session.delete(account)
        return JSONResponse(
          status_code=200,
          content={"success": True, "message": "Cash account deleted successfully"}
        )
    except Exception as e:
      print(f"Error in get_cash_account: {e}")
      return JSONResponse(
          status_code=500,
          content={"success": False, "error": str(e)}
      )
    
