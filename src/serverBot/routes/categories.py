from fastapi import Query
from fastapi.responses import JSONResponse
from src.db.models import Category
from src.db.index import DB
from src.modules.finance.categories.catogoriesRepository import CategoryCreateDTO, CategoryRepository, CategoryUpdateDTO
from src.modules.finance.operations.operationsRepository import OperationsRepository

from ..index import app

@app.get("/api/categories/all", tags=['Categories'])
async def all(tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            allCategories = CategoryRepository.getAll(session, tg_id)
            print(allCategories[0].base_type.name)
            
            allCategoriesJson = [
                {
                    'id': cat.id,
                    'name': cat.name,
                    'base_type': cat.base_type.name if cat.base_type else 'none',
                    'created_at': str(cat.created_at),
                }
                for cat in allCategories 
            ]

            return JSONResponse(
                status_code=200,
                content={"success": True, 'all': allCategoriesJson},
            )
            
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/categories/overview", tags=['Categories'])
async def getOverview(tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            allCategories = CategoryRepository.getAll(session, tg_id)
            
            total_overview = []

            for cat in allCategories: 
                print(cat.id, cat.account_id, cat.name)
                cat_overview = CategoryRepository.getCategoryOverview(session, tg_id, cat.id)

                total_income = float(cat_overview["total_income"])
                total_expenses = float(cat_overview["total_expenses"])

                total_overview.append({
                    'id': cat.id,
                    'name': cat.name,
                    'overview': {
                        "total_income": total_income,
                        "total_expenses": total_expenses,
                        "balance": float(total_income - total_expenses),
                    }
                })

            return JSONResponse(
                status_code=200,
                content={"success": True, 'total_overview': total_overview},
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.get("/api/categories/{id}/overview", tags=['Categories'])
async def getCategoryOverview(id: int, tg_id: int = Query(None)):
    try:
        with DB.get_session() as session:
            categoryOverview = CategoryRepository.getCategoryOverview(session, tg_id, id)
            print(categoryOverview)

            return JSONResponse(
                status_code=200,
                content={"overview": categoryOverview},
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
    
@app.post("/api/categories/create", tags=['Categories'])
async def createCategory(data: CategoryCreateDTO):
    try:
        with DB.get_session() as session:
            category = CategoryRepository.create(session, data)
            category_data = {
                'name': category.name,
                'base_type': category.base_type.name,
                'account_id': category.account_id
            }
            return JSONResponse(
                status_code=201,
                content={"success": False, 'new_category': category_data}
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )


@app.patch("/api/categories/update", tags=['Categories'])
async def updateCategory(data: CategoryUpdateDTO):
    try:
        with DB.get_session() as session:
            updatedCategory = CategoryRepository.update(session, data)
            print(updatedCategory.base_type.name)
            categoryData = {
                'category_id': updatedCategory.id,
                'name': updatedCategory.name,
                'account_id':  updatedCategory.account_id,
                'base_type': updatedCategory.base_type.name,
            }
            print(categoryData)
            return JSONResponse(
                status_code=500,
                content={"success": False, "category": categoryData}
            )
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.delete("/api/categories/delete", tags=['Categories'])
async def delete(cat_id: str = Query(None)):
    try:
        with DB.get_session() as session:
            deleted = CategoryRepository.delete(session, cat_id)
            if not deleted:
                raise Exception(f'Failed to delete {cat_id}')
            return JSONResponse(
                status_code=200,
                content={"success": True}
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )