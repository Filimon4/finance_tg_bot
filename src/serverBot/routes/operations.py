import datetime
from fastapi import HTTPException, Query, Request
from fastapi.responses import JSONResponse
from src.db.models.CashAccount import CashAccount
from src.db.models.Operations import Operations
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationCreateDTO, OperationUpdateDTO, OperationsRepository

from ..index import app

@app.get("/api/operations/cash_account_operations", tags=['Operations'])
async def getCategoryOperations(cash_account_id: int = Query(None), page: int = Query(1), limit: int = Query(100)):
    try:
        with DB.getSession() as session:
            operations = OperationsRepository.getOperationsByCashAccount(session, cash_account_id, page, limit)
            operations_data = [{
                'id': op.id,
                'cash_account_id': op.cash_account_id,
                'to_cash_account_id': op.to_cash_account_id,
                'category_id': op.category_id,
                'amount': float(op.amount),
                'description': op.description,
                'type': op.type.name,
                'created_at': str(op.created_at),
            } for op in operations['operations']]
            return JSONResponse(
                status_code=200,
                content={
                    "operations": operations_data, 
                    "success": True,
                    "page": page,
                    "limit": limit,
                    "total": operations['total']
                },
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.get("/api/operations/operations", tags=['Operations'])
async def getOperations(tg_id: int = Query(None), page: int = Query(1), limit: int = Query(100)):
    try:
        with DB.getSession() as session:
            
            return JSONResponse(
                status_code=200,
                content={"success": True}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.post("/api/operations", tags=['Operations'])
async def createOperation(data: OperationCreateDTO):
    try:
        with DB.getSession() as session:
            if data.to_cash_account_id == data.cash_account_id: 
                raise Exception('to_cash_account_id equls cash_account_id')
            
            operation = OperationsRepository.create(session, data)
            print(operation)
            operation_data = {
                'id': operation.id,
                'cash_account_id': operation.cash_account_id, 
                'to_cash_account_id': operation.to_cash_account_id,
                'category_id': operation.category_id,
                'amount': float(operation.amount),
                'description': operation.description,
                'type': operation.type.name
            }
            return JSONResponse(
                status_code=200,
                content={"operation": operation_data, "success": True},
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.delete("/api/operations", tags=['Operations'])
async def deleteOperation(oper_id: int = Query(None)):
    try:
        with DB.getSession() as session:
            deleted = OperationsRepository.delete(session, oper_id)
            if not deleted: raise Exception('Failed to delete')
            
            return JSONResponse(
                status_code=200,
                content={"success": True}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False}
        )

@app.patch("/api/operations", tags=['Operations'])
async def updateOperation(data: OperationUpdateDTO):
    try:
        with DB.getSession() as session:
            updated_operation = OperationsRepository.update(session, data)
            if not updated_operation: raise Exception('Failed to update')

            operation_data = {
                'id': updated_operation.id,
                'cash_account_id': updated_operation.cash_account_id, 
                'to_cash_account_id': updated_operation.to_cash_account_id,
                'category_id': updated_operation.category_id,
                'amount': float(updated_operation.amount),
                'description': updated_operation.description,
                'type': updated_operation.type.name
            }

            return JSONResponse(
                status_code=200,
                content={"success": True, "operation": operation_data}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
