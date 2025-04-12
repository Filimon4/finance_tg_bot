import asyncio
import schedule
from src.modules.currency.currencyRepository import CurrencyRepository
from src.db.index import DB
from src.modules.currency.index import CurrencyAPI
from sqlalchemy.exc import SQLAlchemyError

class CurrencySystem:
    api = [CurrencyAPI('currencyapi')]

    def __init__(self):
      self._loop = asyncio.new_event_loop()
      self._fetch_interval = 1
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
      with DB.get_session() as session:
        for api in self.api:
          apiRates = api.get_rates()
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

    def updateCurrencies(self):
      with DB.get_session() as session:
        for api in self.api:
          apiCurrencies = api.get_all()
          currenciesKeys = list(dict(apiCurrencies).keys())
          for currency in currenciesKeys:
            try:
              data = apiCurrencies[currency]
              code = data['code']
              name = data['name']
              symbol = data['symbol']
              symbol_native = data['symbol_native']
              CurrencyRepository.get_or_create_currency(session, code, name, symbol, symbol_native)
            except SQLAlchemyError as e:
              print(e)
        session.commit()
    
CurrencySys = CurrencySystem()