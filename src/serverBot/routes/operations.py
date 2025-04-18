from fastapi import HTTPException, Query, Request
from fastapi.responses import JSONResponse
from src.db.models.CashAccount import CashAccount
from src.db.models.Operations import Operations
from src.db.index import DB
from src.modules.finance.cashAccounts.cashAccountRepository import CashAccountRepository
from src.modules.finance.operations.operationsRepository import OperationCreateDTO, OperationUpdateDTO, OperationsRepository

from ..index import app

@app.get("/api/operations/main_cash_account_operations", tags=['Operations'])
async def getCategoryOperations(tg_id: int = Query(None), page: int = Query(1), limit: int = Query(200)):
    try:
        with DB.get_session() as session:
            mainCashAccount = CashAccountRepository.getMain(session, tg_id)
            if not mainCashAccount: raise Exception('There is not main account')
            operations = OperationsRepository.getOperationsByCashAccount(session, mainCashAccount.id, page, limit)
            operations_data = [{
                'id': op.id,
                'name': op.name,
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
    
@app.get("/api/operations/cash_account_operations", tags=['Operations'])
async def getCategoryOperations(cash_account_id: int = Query(None), page: int = Query(1), limit: int = Query(200)):
    try:
        with DB.get_session() as session:
            operations = OperationsRepository.getOperationsByCashAccount(session, cash_account_id, page, limit)
            operations_data = [{
                'id': op.id,
                'name': op.name,
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
    
@app.get("/api/operations", tags=['Operations'])
async def getOperations(tg_id: int = Query(None), page: int = Query(1), limit: int = Query(200)):
    try:
        with DB.get_session() as session:
            operations = OperationsRepository.getOperations(session, tg_id, page, limit)
            
            operations_json = []
            for operation in operations:
                operation_dict = {
                    "id": operation.id,
                    "name": operation.name,
                    "cash_account_id": operation.cash_account_id,
                    "to_cash_account_id": operation.to_cash_account_id,
                    "category_id": operation.category_id,
                    "account_id": operation.account_id,
                    "amount": float(operation.amount),
                    "description": operation.description,
                    "type": operation.type.name if operation.type else None,
                    "created_at": str(operation.created_at)
                }
                operations_json.append(operation_dict)

            return JSONResponse(
                status_code=200,
                content={"success": True, "operations": operations_json}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.get("/api/operations/{id}", tags=['Operations'])
async def getOperation(id: int):
    try:
        with DB.get_session() as session:
            operation = OperationsRepository.getOperationById(session, id)
            operation_dict = {
                "id": operation.id,
                "name": operation.name,
                "cash_account_id": operation.cash_account_id,
                "to_cash_account_id": operation.to_cash_account_id,
                "category_id": operation.category_id,
                "account_id": operation.account_id,
                "amount": float(operation.amount),
                "description": operation.description,
                "type": operation.type.name if operation.type else None,
                "created_at": str(operation.created_at)
            }
            return JSONResponse(
                status_code=200,
                content={"success": True, "operation": operation_dict}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.post("/api/operations", tags=['Operations'])
async def createOperation(data: OperationCreateDTO):
    try:
        with DB.get_session() as session:
            if data.to_cash_account_id == data.cash_account_id: 
                raise Exception('to_cash_account_id equals cash_account_id')
            
            operation = OperationsRepository.create(session, data)
            operation_data = {
                'id': operation.id,
                'name': operation.name,
                'cash_account_id': operation.cash_account_id, 
                'to_cash_account_id': operation.to_cash_account_id if operation.to_cash_account_id is not None else None,
                'category_id': operation.category_id if operation.category_id is not None else None,
                'amount': float(operation.amount),
                'description': operation.description,
                'type': operation.type.name,
                'created_at': str(operation.created_at),
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
async def deleteOperation(id: int = Query(None)):
    try:
        with DB.get_session() as session:
            deleted = OperationsRepository.delete(session, id)
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
        with DB.get_session() as session:
            updated_operation = OperationsRepository.update(session, data)
            if not updated_operation: raise Exception('Failed to update')

            operation_data = {
                'id': updated_operation.id,
                'name': updated_operation.name,
                'cash_account_id': updated_operation.cash_account_id, 
                'to_cash_account_id': updated_operation.to_cash_account_id,
                'category_id': updated_operation.category_id,
                'amount': float(updated_operation.amount),
                'description': updated_operation.description,
                'type': updated_operation.type.name,
                'created_at': str(updated_operation.created_at)
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
