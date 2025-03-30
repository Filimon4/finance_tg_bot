from fastapi import Query
from fastapi.responses import JSONResponse
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/categories/overview", tags=['Categories'])
async def balance(tg_id: str = Query(None)):
    session = DB.getSession()
    try:
        overview = CashAccountRepository.getOverview(session, tg_id)

        return JSONResponse(
            status_code=200,
            content={"overview": overview},
        )
    except Exception as e:
        print(e)
        session.close()
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.get("/api/categories/create", tags=['Categories'])
async def createCategory(tg_id: str = Query(None)):
    pass

@app.patch("/api/categories/update", tags=['Categories'])
async def createCategory(tg_id: str = Query(None), cat_id: str = Query(None)):
    pass

@app.delete("/api/categories/delete", tags=['Categories'])
async def createCategory(tg_id: str = Query(None), cat_id: str = Query(None)):
    pass
