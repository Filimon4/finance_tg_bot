from fastapi.responses import JSONResponse
from src.modules.finance.currencies.currenciesRespository import CurrenciesRepository
from src.db.index import DB
from ..index import app

@app.get("/api/currencies/all", tags=['Currencies'])
async def getAll():
  try:
    with DB.get_session() as session:
      allCurrencies = CurrenciesRepository.getAll(session)
      
      allCurrenciesJSON = [
        {
          "id": cur.id,
          "code": cur.code,
          "name": cur.name,
          "symbol": cur.symbol,
          "symbol_native": cur.symbol_native,
          "created_at": str(cur.created_at),
        }
        for cur in allCurrencies
      ]

      return JSONResponse(
        status_code=200,
        content={"success": True, 'all': allCurrenciesJSON}
      )
    
  except Exception as e:
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(e)}
    )