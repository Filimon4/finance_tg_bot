from fastapi import Query, Request
from fastapi.responses import JSONResponse
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/operations/get_all", tags=['Operations'])
async def getAll(tg_id: str = Query(None), page: int = Query(1), limit: int = Query(100)):
    try:
        with DB.getSession() as session:
            return JSONResponse(
                status_code=200,
                content={"operations": None, "success": True},
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.post("/api/operations/create", tags=['Operations'])
async def createOperation(tg_id: str = Query(None)):
    pass

@app.delete("/api/operations/create", tags=['Operations'])
async def deleteOperation(tg_id: str = Query(None)):
    pass

@app.patch("/api/operations/update_operation", tags=['Operations'])
async def updateOperation(tg_id: str = Query(None)):
    pass
