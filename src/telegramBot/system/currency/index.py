import asyncio
import schedule
from src.modules.currency.index import CurrencyEnum, CurrencyManager
from src.modules.currency.currencyRepository import CurrencyRepository
from src.db.index import DB
from sqlalchemy.exc import SQLAlchemyError

class CurrencySystem:
    def __init__(self):
      self._loop = asyncio.new_event_loop()
      self._fetch_interval = 7
      self._setup_scheduler()

    def _setup_scheduler(self):
      schedule.every(self._fetch_interval).days.do(self._startFetching_sync)

    def _startFetching_sync(self):
      asyncio.set_event_loop(self._loop)
      self._loop.run_until_complete(self.updateAllApi())

    def updateAllApi(self):
      self.updateCurrencies()
      self.updateRates()

    def updateRates(self):
      for api in CurrencyEnum.get_list():
        self.updateApiRates(api)

    def updateCurrencies(self):
      for api in CurrencyEnum.get_list():
        self.updateApiCurrencies(api)

    def getApiStatus(self, api):
      return CurrencyManager.get_status(api)

    def updateApiCurrencies(self, api):
      with DB.get_session() as session:
        apiCurrencies = CurrencyManager.get_all(api)
        currenciesKeys = list(dict(apiCurrencies).keys())
        for currency in currenciesKeys:
          try:
            data = apiCurrencies[currency]
            symbol = data['symbol']
            name = data['name']
            CurrencyRepository.get_or_create_currency(session, symbol, name, name, symbol)
          except SQLAlchemyError as e:
            print(e)
        session.commit()

    def updateApiRates(self, api):
      with DB.get_session() as session:
        apiRates = CurrencyManager.get_rates(api)
        apiRatesKeys = list(dict(apiRates).keys())
        for currency in apiRatesKeys:
          try:
            data = apiRates[currency]
            base = data['base']
            rates = data['data']
            CurrencyRepository.sync_currency_rates(session, base, rates)
          except SQLAlchemyError as e:
            print(e)
        session.commit()
    
CurrencySys = CurrencySystem()